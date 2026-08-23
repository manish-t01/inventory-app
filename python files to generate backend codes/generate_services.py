import os

base_dir = r"D:\Coding\github\Projects\Rohit's Work\inventory-app\src\main\java\com\multistore\inventory"

dirs = ["dto", "service", "controller"]
for d in dirs:
    os.makedirs(os.path.join(base_dir, d), exist_ok=True)

dtos = {
    "DailyRecordDTO.java": """package com.multistore.inventory.dto;

import java.time.LocalDate;
import java.util.List;

public class DailyRecordDTO {
    private Long storeId;
    private LocalDate recordDate;
    private String notes;
    private List<DailyRecordItemDTO> items;

    // Getters and Setters
    public Long getStoreId() { return storeId; }
    public void setStoreId(Long storeId) { this.storeId = storeId; }
    public LocalDate getRecordDate() { return recordDate; }
    public void setRecordDate(LocalDate recordDate) { this.recordDate = recordDate; }
    public String getNotes() { return notes; }
    public void setNotes(String notes) { this.notes = notes; }
    public List<DailyRecordItemDTO> getItems() { return items; }
    public void setItems(List<DailyRecordItemDTO> items) { this.items = items; }
}
""",
    "DailyRecordItemDTO.java": """package com.multistore.inventory.dto;

import java.math.BigDecimal;

public class DailyRecordItemDTO {
    private Long productVariantId;
    private Integer openingStock;
    private Integer stockReceived;
    private Integer soldQuantity;
    private BigDecimal sellingPrice;
    
    // Getters and Setters
    public Long getProductVariantId() { return productVariantId; }
    public void setProductVariantId(Long productVariantId) { this.productVariantId = productVariantId; }
    public Integer getOpeningStock() { return openingStock; }
    public void setOpeningStock(Integer openingStock) { this.openingStock = openingStock; }
    public Integer getStockReceived() { return stockReceived; }
    public void setStockReceived(Integer stockReceived) { this.stockReceived = stockReceived; }
    public Integer getSoldQuantity() { return soldQuantity; }
    public void setSoldQuantity(Integer soldQuantity) { this.soldQuantity = soldQuantity; }
    public BigDecimal getSellingPrice() { return sellingPrice; }
    public void setSellingPrice(BigDecimal sellingPrice) { this.sellingPrice = sellingPrice; }
}
"""
}

for name, content in dtos.items():
    with open(os.path.join(base_dir, "dto", name), "w", encoding="utf-8") as f:
        f.write(content)

services = {
    "InventoryService.java": """package com.multistore.inventory.service;

import com.multistore.inventory.dto.DailyRecordDTO;
import com.multistore.inventory.dto.DailyRecordItemDTO;
import com.multistore.inventory.entity.*;
import com.multistore.inventory.repository.*;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.util.Optional;
import java.util.List;

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

    @Transactional
    public DailyRecord saveDailyRecord(DailyRecordDTO dto) {
        Store store = storeRepository.findById(dto.getStoreId())
                .orElseThrow(() -> new RuntimeException("Store not found"));
                
        // Check if record already exists
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
            ProductVariant variant = productVariantRepository.findById(itemDto.getProductVariantId())
                    .orElseThrow(() -> new RuntimeException("Product Variant not found"));

            // Validations
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

            // Create Inventory Transactions
            // 1. Opening
            InventoryTransaction tOpen = new InventoryTransaction();
            tOpen.setStore(store);
            tOpen.setProductVariant(variant);
            tOpen.setTransactionDate(dto.getRecordDate());
            tOpen.setType(TransactionType.OPENING);
            tOpen.setQuantity(opening);
            tOpen.setReferenceId("DAILY_RECORD_" + record.getId());
            inventoryTransactionRepository.save(tOpen);
            
            // 2. Received (if any)
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
            
            // 3. Sale (if any)
            if (sold > 0) {
                InventoryTransaction tSale = new InventoryTransaction();
                tSale.setStore(store);
                tSale.setProductVariant(variant);
                tSale.setTransactionDate(dto.getRecordDate());
                tSale.setType(TransactionType.SALE);
                tSale.setQuantity(-sold);
                tSale.setReferenceId("DAILY_RECORD_" + record.getId());
                inventoryTransactionRepository.save(tSale);
                
                // Also create Sale record
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
    "SeedService.java": """package com.multistore.inventory.service;

import com.multistore.inventory.entity.Store;
import com.multistore.inventory.repository.StoreRepository;
import jakarta.annotation.PostConstruct;
import org.springframework.stereotype.Service;

@Service
public class SeedService {

    private final StoreRepository storeRepository;

    public SeedService(StoreRepository storeRepository) {
        this.storeRepository = storeRepository;
    }

    @PostConstruct
    public void seedData() {
        if (storeRepository.count() == 0) {
            for (int i = 1; i <= 4; i++) {
                Store store = new Store();
                store.setName("Store " + i);
                storeRepository.save(store);
            }
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
import com.multistore.inventory.entity.Product;
import com.multistore.inventory.entity.Store;
import com.multistore.inventory.repository.ProductRepository;
import com.multistore.inventory.repository.StoreRepository;
import com.multistore.inventory.service.InventoryService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api")
public class InventoryController {
    
    private final StoreRepository storeRepository;
    private final ProductRepository productRepository;
    private final InventoryService inventoryService;

    public InventoryController(StoreRepository storeRepository, 
                               ProductRepository productRepository,
                               InventoryService inventoryService) {
        this.storeRepository = storeRepository;
        this.productRepository = productRepository;
        this.inventoryService = inventoryService;
    }

    @GetMapping("/stores")
    public List<Store> getStores() {
        return storeRepository.findAll();
    }
    
    @GetMapping("/products")
    public List<Product> getProducts() {
        return productRepository.findAll();
    }

    @PostMapping("/daily-records")
    public ResponseEntity<?> saveDailyRecord(@RequestBody DailyRecordDTO dto) {
        try {
            DailyRecord record = inventoryService.saveDailyRecord(dto);
            return ResponseEntity.ok(record);
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

print("DTOs, Services, and Controllers created successfully.")
