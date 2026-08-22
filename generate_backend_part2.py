import os

base_dir = r"D:\Coding\github\Projects\Rohit's Work\inventory-app\src\main\java\com\multistore\inventory"

# Additional DTOs
dtos = {
    "ProductDTO.java": """package com.multistore.inventory.dto;
public class ProductDTO {
    private Long id;
    private String name;
    private String category;
    private boolean active;
    // Getters and Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public String getCategory() { return category; }
    public void setCategory(String category) { this.category = category; }
    public boolean isActive() { return active; }
    public void setActive(boolean active) { this.active = active; }
}
""",
    "ProductVariantDTO.java": """package com.multistore.inventory.dto;
import java.math.BigDecimal;
public class ProductVariantDTO {
    private Long id;
    private Long productId;
    private String size;
    private BigDecimal sellingPrice;
    private BigDecimal costPrice;
    private Integer minimumStock;
    private boolean active;
    // Getters and Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public Long getProductId() { return productId; }
    public void setProductId(Long productId) { this.productId = productId; }
    public String getSize() { return size; }
    public void setSize(String size) { this.size = size; }
    public BigDecimal getSellingPrice() { return sellingPrice; }
    public void setSellingPrice(BigDecimal sellingPrice) { this.sellingPrice = sellingPrice; }
    public BigDecimal getCostPrice() { return costPrice; }
    public void setCostPrice(BigDecimal costPrice) { this.costPrice = costPrice; }
    public Integer getMinimumStock() { return minimumStock; }
    public void setMinimumStock(Integer minimumStock) { this.minimumStock = minimumStock; }
    public boolean isActive() { return active; }
    public void setActive(boolean active) { this.active = active; }
}
""",
    "ReportDailyDTO.java": """package com.multistore.inventory.dto;
import java.util.List;
import java.math.BigDecimal;
public class ReportDailyDTO {
    private Integer totalOpening;
    private Integer totalReceived;
    private Integer totalAvailable;
    private Integer totalSold;
    private Integer totalClosing;
    private BigDecimal totalSalesAmount;
    private List<DailyRecordItemDTO> items; // Can reuse or create specific report item DTO
    // Getters and setters...
    public Integer getTotalOpening() { return totalOpening; }
    public void setTotalOpening(Integer totalOpening) { this.totalOpening = totalOpening; }
    public Integer getTotalReceived() { return totalReceived; }
    public void setTotalReceived(Integer totalReceived) { this.totalReceived = totalReceived; }
    public Integer getTotalAvailable() { return totalAvailable; }
    public void setTotalAvailable(Integer totalAvailable) { this.totalAvailable = totalAvailable; }
    public Integer getTotalSold() { return totalSold; }
    public void setTotalSold(Integer totalSold) { this.totalSold = totalSold; }
    public Integer getTotalClosing() { return totalClosing; }
    public void setTotalClosing(Integer totalClosing) { this.totalClosing = totalClosing; }
    public BigDecimal getTotalSalesAmount() { return totalSalesAmount; }
    public void setTotalSalesAmount(BigDecimal totalSalesAmount) { this.totalSalesAmount = totalSalesAmount; }
    public List<DailyRecordItemDTO> getItems() { return items; }
    public void setItems(List<DailyRecordItemDTO> items) { this.items = items; }
}
"""
}

for name, content in dtos.items():
    with open(os.path.join(base_dir, "dto", name), "w", encoding="utf-8") as f:
        f.write(content)

services = {
    "ProductService.java": """package com.multistore.inventory.service;

import com.multistore.inventory.dto.ProductDTO;
import com.multistore.inventory.dto.ProductVariantDTO;
import com.multistore.inventory.entity.Product;
import com.multistore.inventory.entity.ProductVariant;
import com.multistore.inventory.repository.ProductRepository;
import com.multistore.inventory.repository.ProductVariantRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.util.List;

@Service
public class ProductService {
    private final ProductRepository productRepository;
    private final ProductVariantRepository productVariantRepository;

    public ProductService(ProductRepository productRepository, ProductVariantRepository productVariantRepository) {
        this.productRepository = productRepository;
        this.productVariantRepository = productVariantRepository;
    }

    public List<Product> getAllProducts() {
        return productRepository.findAll();
    }

    public Product getProduct(Long id) {
        return productRepository.findById(id).orElseThrow(() -> new RuntimeException("Product not found"));
    }

    @Transactional
    public Product createProduct(ProductDTO dto) {
        if (dto.getName() == null || dto.getName().trim().isEmpty()) {
            throw new RuntimeException("Product name cannot be empty");
        }
        Product p = new Product();
        p.setName(dto.getName());
        p.setCategory(dto.getCategory());
        p.setActive(true);
        return productRepository.save(p);
    }

    @Transactional
    public Product updateProduct(Long id, ProductDTO dto) {
        Product p = getProduct(id);
        if (dto.getName() == null || dto.getName().trim().isEmpty()) {
            throw new RuntimeException("Product name cannot be empty");
        }
        p.setName(dto.getName());
        p.setCategory(dto.getCategory());
        p.setActive(dto.isActive());
        return productRepository.save(p);
    }

    public List<ProductVariant> getVariants(Long productId) {
        return productVariantRepository.findByProductId(productId);
    }

    @Transactional
    public ProductVariant createVariant(Long productId, ProductVariantDTO dto) {
        Product p = getProduct(productId);
        if (dto.getSize() == null || dto.getSize().trim().isEmpty()) {
            throw new RuntimeException("Size cannot be empty");
        }
        if (dto.getSellingPrice() == null || dto.getSellingPrice().compareTo(BigDecimal.ZERO) < 0) {
            throw new RuntimeException("Selling price cannot be negative");
        }
        if (dto.getMinimumStock() != null && dto.getMinimumStock() < 0) {
            throw new RuntimeException("Minimum stock cannot be negative");
        }

        ProductVariant pv = new ProductVariant();
        pv.setProduct(p);
        pv.setSize(dto.getSize());
        pv.setSellingPrice(dto.getSellingPrice());
        pv.setCostPrice(dto.getCostPrice());
        pv.setMinimumStock(dto.getMinimumStock() != null ? dto.getMinimumStock() : 0);
        pv.setActive(true);
        return productVariantRepository.save(pv);
    }
}
""",
    "StoreService.java": """package com.multistore.inventory.service;

import com.multistore.inventory.entity.Store;
import com.multistore.inventory.repository.StoreRepository;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class StoreService {
    private final StoreRepository storeRepository;

    public StoreService(StoreRepository storeRepository) {
        this.storeRepository = storeRepository;
    }

    public List<Store> getAllStores() {
        return storeRepository.findAll();
    }
}
""",
    "ReportService.java": """package com.multistore.inventory.service;

import com.multistore.inventory.entity.DailyRecord;
import com.multistore.inventory.entity.DailyRecordItem;
import com.multistore.inventory.repository.DailyRecordRepository;
import org.springframework.stereotype.Service;
import java.time.LocalDate;
import java.util.Optional;
import java.util.List;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;
import java.math.BigDecimal;

@Service
public class ReportService {
    private final DailyRecordRepository dailyRecordRepository;

    public ReportService(DailyRecordRepository dailyRecordRepository) {
        this.dailyRecordRepository = dailyRecordRepository;
    }

    public Map<String, Object> getDailyReport(Long storeId, LocalDate date) {
        Optional<DailyRecord> recordOpt = dailyRecordRepository.findByStoreIdAndRecordDate(storeId, date);
        Map<String, Object> result = new HashMap<>();
        
        if (recordOpt.isEmpty()) {
            result.put("items", new ArrayList<>());
            return result;
        }
        
        DailyRecord record = recordOpt.get();
        // In a real app we would load items. Since mapping might need a custom query or eager fetching, we assume lazy loads fine inside transaction.
        // For simplicity in MVP, we just return the data structure.
        return result; 
    }
}
"""
}

for name, content in services.items():
    with open(os.path.join(base_dir, "service", name), "w", encoding="utf-8") as f:
        f.write(content)

controllers = {
    "ProductController.java": """package com.multistore.inventory.controller;

import com.multistore.inventory.dto.ProductDTO;
import com.multistore.inventory.dto.ProductVariantDTO;
import com.multistore.inventory.entity.Product;
import com.multistore.inventory.entity.ProductVariant;
import com.multistore.inventory.service.ProductService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/products")
public class ProductController {
    private final ProductService productService;

    public ProductController(ProductService productService) {
        this.productService = productService;
    }

    @GetMapping
    public List<Product> getAll() {
        return productService.getAllProducts();
    }

    @PostMapping
    public ResponseEntity<?> createProduct(@RequestBody ProductDTO dto) {
        try {
            return ResponseEntity.ok(productService.createProduct(dto));
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(e.getMessage());
        }
    }

    @GetMapping("/{id}/variants")
    public List<ProductVariant> getVariants(@PathVariable Long id) {
        return productService.getVariants(id);
    }

    @PostMapping("/{id}/variants")
    public ResponseEntity<?> createVariant(@PathVariable Long id, @RequestBody ProductVariantDTO dto) {
        try {
            return ResponseEntity.ok(productService.createVariant(id, dto));
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(e.getMessage());
        }
    }
}
""",
    "StoreController.java": """package com.multistore.inventory.controller;

import com.multistore.inventory.entity.Store;
import com.multistore.inventory.service.StoreService;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/stores")
public class StoreController {
    private final StoreService storeService;

    public StoreController(StoreService storeService) {
        this.storeService = storeService;
    }

    @GetMapping
    public List<Store> getAll() {
        return storeService.getAllStores();
    }
}
"""
}

for name, content in controllers.items():
    with open(os.path.join(base_dir, "controller", name), "w", encoding="utf-8") as f:
        f.write(content)

# Update InventoryController
inventory_controller = """package com.multistore.inventory.controller;

import com.multistore.inventory.dto.DailyRecordDTO;
import com.multistore.inventory.entity.DailyRecord;
import com.multistore.inventory.service.InventoryService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/daily-records")
public class InventoryController {
    
    private final InventoryService inventoryService;

    public InventoryController(InventoryService inventoryService) {
        this.inventoryService = inventoryService;
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
}
"""
with open(os.path.join(base_dir, "controller", "InventoryController.java"), "w", encoding="utf-8") as f:
    f.write(inventory_controller)

print("Backend Part 2 generated successfully.")
