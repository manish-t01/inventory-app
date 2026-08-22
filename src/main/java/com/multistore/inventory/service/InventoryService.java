package com.multistore.inventory.service;

import com.multistore.inventory.dto.DailyRecordDTO;
import com.multistore.inventory.dto.DailyRecordItemDTO;
import com.multistore.inventory.entity.*;
import com.multistore.inventory.repository.*;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

@Service
public class InventoryService {
    
    private final StoreRepository storeRepository;
    private final ProductVariantRepository productVariantRepository;
    private final DailyRecordRepository dailyRecordRepository;
    private final DailyRecordItemRepository dailyRecordItemRepository;
    private final InventoryTransactionRepository inventoryTransactionRepository;
    private final SaleRepository saleRepository;

    public InventoryService(StoreRepository storeRepository,
                            ProductVariantRepository productVariantRepository,
                            DailyRecordRepository dailyRecordRepository,
                            DailyRecordItemRepository dailyRecordItemRepository,
                            InventoryTransactionRepository inventoryTransactionRepository,
                            SaleRepository saleRepository) {
        this.storeRepository = storeRepository;
        this.productVariantRepository = productVariantRepository;
        this.dailyRecordRepository = dailyRecordRepository;
        this.dailyRecordItemRepository = dailyRecordItemRepository;
        this.inventoryTransactionRepository = inventoryTransactionRepository;
        this.saleRepository = saleRepository;
    }

    public Integer getSuggestedOpeningStock(Long storeId, Long variantId, LocalDate date) {
        Optional<DailyRecordItem> previousRecord = dailyRecordItemRepository
            .findTopByStoreIdAndProductVariantIdAndRecordDateLessThanOrderByRecordDateDesc(storeId, variantId, date);
        return previousRecord.map(DailyRecordItem::getClosingStock).orElse(0);
    }

    public List<DailyRecord> getAllDailyRecords() {
        return dailyRecordRepository.findAll();
    }

    public DailyRecord getDailyRecord(Long id) {
        return dailyRecordRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Daily record not found"));
    }

    public List<DailyRecordItem> getDailyRecordItems(Long recordId) {
        return dailyRecordItemRepository.findByDailyRecordId(recordId);
    }

    @Transactional
    public DailyRecord saveDailyRecord(DailyRecordDTO dto) {
        Store store = storeRepository.findById(dto.getStoreId())
                .orElseThrow(() -> new RuntimeException("Store not found"));
                
        Optional<DailyRecord> existing = dailyRecordRepository.findByStoreIdAndRecordDate(store.getId(), dto.getRecordDate());
        if (existing.isPresent()) {
            throw new RuntimeException("A daily record already exists for this store on this date.");
        }
        
        DailyRecord record = new DailyRecord();
        record.setStore(store);
        record.setRecordDate(dto.getRecordDate());
        record.setNotes(dto.getNotes());
        record = dailyRecordRepository.save(record);

        for (DailyRecordItemDTO itemDto : dto.getItems()) {
            processItem(store, record, itemDto);
        }
        
        return record;
    }

    @Transactional
    public DailyRecord updateDailyRecord(Long id, DailyRecordDTO dto) {
        DailyRecord record = dailyRecordRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Daily record not found"));
        
        Store store = storeRepository.findById(dto.getStoreId())
                .orElseThrow(() -> new RuntimeException("Store not found"));
                
        Optional<DailyRecord> existingDateCheck = dailyRecordRepository.findByStoreIdAndRecordDate(store.getId(), dto.getRecordDate());
        if (existingDateCheck.isPresent() && !existingDateCheck.get().getId().equals(id)) {
            throw new RuntimeException("A daily record already exists for this store on this date.");
        }

        record.setStore(store);
        record.setRecordDate(dto.getRecordDate());
        record.setNotes(dto.getNotes());
        record = dailyRecordRepository.save(record);

        List<DailyRecordItem> existingItems = dailyRecordItemRepository.findByDailyRecordId(record.getId());
        
        List<Long> incomingVariantIds = dto.getItems().stream()
            .map(DailyRecordItemDTO::getProductVariantId)
            .collect(Collectors.toList());

        for (DailyRecordItem oldItem : existingItems) {
            if (!incomingVariantIds.contains(oldItem.getProductVariant().getId())) {
                deleteLedgerEntries(record.getId(), oldItem.getProductVariant().getId());
                dailyRecordItemRepository.delete(oldItem);
            }
        }

        for (DailyRecordItemDTO itemDto : dto.getItems()) {
            deleteLedgerEntries(record.getId(), itemDto.getProductVariantId());
            dailyRecordItemRepository.deleteByDailyRecordIdAndProductVariantId(record.getId(), itemDto.getProductVariantId());
            processItem(store, record, itemDto);
        }

        return record;
    }

    private void deleteLedgerEntries(Long recordId, Long variantId) {
        String reference = "DAILY_RECORD_" + recordId;
        inventoryTransactionRepository.deleteByReferenceIdAndProductVariantId(reference, variantId);
        saleRepository.deleteBySourceAndProductVariantId(reference, variantId);
    }

    private void processItem(Store store, DailyRecord record, DailyRecordItemDTO itemDto) {
        ProductVariant variant = productVariantRepository.findById(itemDto.getProductVariantId())
                .orElseThrow(() -> new RuntimeException("Product Variant not found"));

        int opening = itemDto.getOpeningStock() != null ? itemDto.getOpeningStock() : 0;
        int received = itemDto.getStockReceived() != null ? itemDto.getStockReceived() : 0;
        int sold = itemDto.getSoldQuantity() != null ? itemDto.getSoldQuantity() : 0;
        BigDecimal price = itemDto.getSellingPrice();
        
        if (opening < 0 || received < 0 || sold < 0) {
            throw new RuntimeException("Quantities cannot be negative");
        }
        if (price == null || price.compareTo(BigDecimal.ZERO) < 0) {
            throw new RuntimeException("Invalid price");
        }

        int totalAvailable = opening + received;
        if (sold > totalAvailable) {
            throw new RuntimeException("Sold quantity exceeds available stock for product variant " + variant.getId());
        }

        int closing = totalAvailable - sold;
        BigDecimal amount = price.multiply(BigDecimal.valueOf(sold));

        DailyRecordItem item = new DailyRecordItem();
        item.setDailyRecord(record);
        item.setProductVariant(variant);
        item.setOpeningStock(opening);
        item.setStockReceived(received);
        item.setSoldQuantity(sold);
        item.setSellingPrice(price);
        item.setTotalAvailable(totalAvailable);
        item.setClosingStock(closing);
        item.setSalesAmount(amount);
        
        dailyRecordItemRepository.save(item);

        // Recreate Transactions Safely
        String reference = "DAILY_RECORD_" + record.getId();

        InventoryTransaction tOpen = new InventoryTransaction();
        tOpen.setStore(store);
        tOpen.setProductVariant(variant);
        tOpen.setTransactionDate(record.getRecordDate());
        tOpen.setType(TransactionType.OPENING);
        tOpen.setQuantity(opening);
        tOpen.setReferenceId(reference);
        inventoryTransactionRepository.save(tOpen);
        
        if (received > 0) {
            InventoryTransaction tRecv = new InventoryTransaction();
            tRecv.setStore(store);
            tRecv.setProductVariant(variant);
            tRecv.setTransactionDate(record.getRecordDate());
            tRecv.setType(TransactionType.RECEIVED);
            tRecv.setQuantity(received);
            tRecv.setReferenceId(reference);
            inventoryTransactionRepository.save(tRecv);
        }
        
        if (sold > 0) {
            InventoryTransaction tSale = new InventoryTransaction();
            tSale.setStore(store);
            tSale.setProductVariant(variant);
            tSale.setTransactionDate(record.getRecordDate());
            tSale.setType(TransactionType.SALE);
            tSale.setQuantity(-sold);
            tSale.setReferenceId(reference);
            inventoryTransactionRepository.save(tSale);
            
            Sale sale = new Sale();
            sale.setStore(store);
            sale.setProductVariant(variant);
            sale.setSaleDate(record.getRecordDate());
            sale.setQuantity(sold);
            sale.setSellingPrice(price);
            sale.setAmount(amount);
            sale.setSource(reference);
            saleRepository.save(sale);
        }
    }

    @Transactional
    public void deleteDailyRecord(Long id) {
        DailyRecord record = dailyRecordRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Daily record not found"));

        dailyRecordItemRepository.deleteByDailyRecordId(id);

        String reference = "DAILY_RECORD_" + id;
        inventoryTransactionRepository.deleteByReferenceId(reference);
        saleRepository.deleteBySource(reference);

        dailyRecordRepository.delete(record);
    }
}
