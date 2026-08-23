import os

base_dir = r"D:\Coding\github\Projects\Rohit's Work\inventory-app\src\main\java\com\multistore\inventory"

services = {
    "InventoryService.java": """package com.multistore.inventory.service;

import com.multistore.inventory.dto.DailyRecordDTO;
import com.multistore.inventory.dto.DailyRecordItemDTO;
import com.multistore.inventory.entity.*;
import com.multistore.inventory.repository.*;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.Optional;

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

    @Transactional
    public DailyRecord saveDailyRecord(DailyRecordDTO dto) {
        Store store = storeRepository.findById(dto.getStoreId())
                .orElseThrow(() -> new RuntimeException("Store not found"));
                
        Optional<DailyRecord> existing = dailyRecordRepository.findByStoreIdAndRecordDate(store.getId(), dto.getRecordDate());
        DailyRecord record;
        if (existing.isPresent()) {
            record = existing.get();
            // In a real app we'd carefully reconcile items. For simplicity in MVP, we just overwrite notes if present.
            // A full edit implementation requires checking diffs, reversing previous transactions, and inserting new ones.
            // To keep it safe, if editing is allowed via this endpoint, we could delete old items and transactions and recreate.
            // But for now, we assume this is a new record creation logic and we block duplicates as per user request if not an explicit edit.
            throw new RuntimeException("A daily record already exists for this store on this date.");
        } else {
            record = new DailyRecord();
            record.setStore(store);
            record.setRecordDate(dto.getRecordDate());
            record.setNotes(dto.getNotes());
            record = dailyRecordRepository.save(record);
        }

        for (DailyRecordItemDTO itemDto : dto.getItems()) {
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

            // Transactions
            InventoryTransaction tOpen = new InventoryTransaction();
            tOpen.setStore(store);
            tOpen.setProductVariant(variant);
            tOpen.setTransactionDate(dto.getRecordDate());
            tOpen.setType(TransactionType.OPENING);
            tOpen.setQuantity(opening);
            tOpen.setReferenceId("DAILY_RECORD_" + record.getId());
            inventoryTransactionRepository.save(tOpen);
            
            if (received > 0) {
                InventoryTransaction tRecv = new InventoryTransaction();
                tRecv.setStore(store);
                tRecv.setProductVariant(variant);
                tRecv.setTransactionDate(dto.getRecordDate());
                tRecv.setType(TransactionType.RECEIVED);
                tRecv.setQuantity(received);
                tRecv.setReferenceId("DAILY_RECORD_" + record.getId());
                inventoryTransactionRepository.save(tRecv);
            }
            
            if (sold > 0) {
                InventoryTransaction tSale = new InventoryTransaction();
                tSale.setStore(store);
                tSale.setProductVariant(variant);
                tSale.setTransactionDate(dto.getRecordDate());
                tSale.setType(TransactionType.SALE);
                tSale.setQuantity(-sold);
                tSale.setReferenceId("DAILY_RECORD_" + record.getId());
                inventoryTransactionRepository.save(tSale);
                
                Sale sale = new Sale();
                sale.setStore(store);
                sale.setProductVariant(variant);
                sale.setSaleDate(dto.getRecordDate());
                sale.setQuantity(sold);
                sale.setSellingPrice(price);
                sale.setAmount(amount);
                sale.setSource("DAILY_RECORD_" + record.getId());
                saleRepository.save(sale);
            }
        }
        
        return record;
    }
}
""",
    "FileStorageService.java": """package com.multistore.inventory.service;

import com.multistore.inventory.entity.DailyRecord;
import com.multistore.inventory.repository.DailyRecordRepository;
import org.springframework.stereotype.Service;
import org.springframework.util.StringUtils;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.util.UUID;

@Service
public class FileStorageService {

    private final Path fileStorageLocation;
    private final DailyRecordRepository dailyRecordRepository;

    public FileStorageService(DailyRecordRepository dailyRecordRepository) {
        this.dailyRecordRepository = dailyRecordRepository;
        this.fileStorageLocation = Paths.get("uploads/daily-records").toAbsolutePath().normalize();

        try {
            Files.createDirectories(this.fileStorageLocation);
        } catch (Exception ex) {
            throw new RuntimeException("Could not create the directory where the uploaded files will be stored.", ex);
        }
    }

    public String storeFile(Long dailyRecordId, MultipartFile file) {
        String originalFileName = StringUtils.cleanPath(file.getOriginalFilename());
        
        try {
            if (originalFileName.contains("..")) {
                throw new RuntimeException("Sorry! Filename contains invalid path sequence " + originalFileName);
            }
            
            String extension = "";
            int i = originalFileName.lastIndexOf('.');
            if (i > 0) {
                extension = originalFileName.substring(i);
            }
            
            if (!extension.equalsIgnoreCase(".jpg") && !extension.equalsIgnoreCase(".jpeg") && !extension.equalsIgnoreCase(".png")) {
                throw new RuntimeException("Only JPG and PNG images are allowed.");
            }

            String newFileName = "store-record-" + dailyRecordId + "-" + UUID.randomUUID().toString() + extension;
            Path targetLocation = this.fileStorageLocation.resolve(newFileName);
            Files.copy(file.getInputStream(), targetLocation, StandardCopyOption.REPLACE_EXISTING);

            DailyRecord record = dailyRecordRepository.findById(dailyRecordId)
                .orElseThrow(() -> new RuntimeException("Daily record not found"));
            
            record.setSourceImagePath("uploads/daily-records/" + newFileName);
            dailyRecordRepository.save(record);

            return newFileName;
        } catch (IOException ex) {
            throw new RuntimeException("Could not store file " + originalFileName + ". Please try again!", ex);
        }
    }
}
"""
}

for name, content in services.items():
    with open(os.path.join(base_dir, "service", name), "w", encoding="utf-8") as f:
        f.write(content)

controllers = {
    "InventoryController.java": """package com.multistore.inventory.controller;

import com.multistore.inventory.dto.DailyRecordDTO;
import com.multistore.inventory.entity.DailyRecord;
import com.multistore.inventory.service.InventoryService;
import com.multistore.inventory.service.FileStorageService;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.time.LocalDate;

@RestController
@RequestMapping("/api/daily-records")
public class InventoryController {
    
    private final InventoryService inventoryService;
    private final FileStorageService fileStorageService;

    public InventoryController(InventoryService inventoryService, FileStorageService fileStorageService) {
        this.inventoryService = inventoryService;
        this.fileStorageService = fileStorageService;
    }

    @PostMapping
    public ResponseEntity<?> saveDailyRecord(@RequestBody DailyRecordDTO dto) {
        try {
            DailyRecord record = inventoryService.saveDailyRecord(dto);
            return ResponseEntity.ok(record);
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(e.getMessage());
        }
    }
    
    @GetMapping("/suggest-opening")
    public ResponseEntity<?> getSuggestedOpeningStock(
            @RequestParam Long storeId,
            @RequestParam Long variantId,
            @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate date) {
        try {
            Integer opening = inventoryService.getSuggestedOpeningStock(storeId, variantId, date);
            return ResponseEntity.ok(opening);
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(0);
        }
    }
    
    @PostMapping("/{id}/image")
    public ResponseEntity<?> uploadImage(@PathVariable Long id, @RequestParam("file") MultipartFile file) {
        try {
            String fileName = fileStorageService.storeFile(id, file);
            return ResponseEntity.ok(fileName);
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(e.getMessage());
        }
    }
}
"""
}

for name, content in controllers.items():
    with open(os.path.join(base_dir, "controller", name), "w", encoding="utf-8") as f:
        f.write(content)

print("Services Part 5 and File Upload API generated successfully.")
