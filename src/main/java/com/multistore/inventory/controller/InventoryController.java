package com.multistore.inventory.controller;

import com.multistore.inventory.dto.DailyRecordDTO;
import com.multistore.inventory.dto.DailyRecordItemDTO;
import com.multistore.inventory.entity.DailyRecord;
import com.multistore.inventory.entity.DailyRecordImage;
import com.multistore.inventory.entity.DailyRecordItem;
import com.multistore.inventory.service.InventoryService;
import com.multistore.inventory.service.FileStorageService;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.time.LocalDate;
import java.util.List;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/api/daily-records")
public class InventoryController {
    
    private final InventoryService inventoryService;
    private final FileStorageService fileStorageService;

    public InventoryController(InventoryService inventoryService, FileStorageService fileStorageService) {
        this.inventoryService = inventoryService;
        this.fileStorageService = fileStorageService;
    }
    
    @GetMapping
    public ResponseEntity<List<DailyRecord>> getAllRecords() {
        return ResponseEntity.ok(inventoryService.getAllDailyRecords());
    }

    @GetMapping("/{id}")
    public ResponseEntity<?> getRecord(@PathVariable Long id) {
        try {
            DailyRecord record = inventoryService.getDailyRecord(id);
            List<DailyRecordItem> items = inventoryService.getDailyRecordItems(id);
            
            DailyRecordDTO dto = new DailyRecordDTO();
            dto.setStoreId(record.getStore().getId());
            dto.setRecordDate(record.getRecordDate());
            dto.setNotes(record.getNotes());
            // Map image to frontend
            // using notes temporarily or a new field, but we can return record directly and then items
            
            // To be robust, let's return a custom object
            return ResponseEntity.ok(new RecordResponse(record, items));
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(e.getMessage());
        }
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
    
    @PutMapping("/{id}")
    public ResponseEntity<?> updateDailyRecord(@PathVariable Long id, @RequestBody DailyRecordDTO dto) {
        try {
            DailyRecord record = inventoryService.updateDailyRecord(id, dto);
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
    
    @PostMapping("/{id}/images")
    public ResponseEntity<?> uploadImages(@PathVariable Long id, @RequestParam("files") MultipartFile[] files) {
        try {
            List<String> fileNames = fileStorageService.storeFiles(id, files);
            return ResponseEntity.ok(fileNames);
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(e.getMessage());
        }
    }

    @DeleteMapping("/{id}/image/{imageId}")
    public ResponseEntity<?> deleteImage(@PathVariable Long id, @PathVariable String imageId) {
        try {
            fileStorageService.deleteImage(id, imageId);
            return ResponseEntity.ok("Deleted");
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(e.getMessage());
        }
    }
    
    public static class RecordResponse {
        public Long id;
        public Long storeId;
        public LocalDate recordDate;
        public String notes;
        public String sourceImagePath;
        public List<ImageDTO> additionalImages;
        public List<DailyRecordItemDTO> items;

        public static class ImageDTO {
            public Long id;
            public String imagePath;
            public ImageDTO(Long id, String imagePath) {
                this.id = id;
                this.imagePath = imagePath;
            }
        }

        public RecordResponse(DailyRecord record, List<DailyRecordItem> itemsList) {
            this.id = record.getId();
            this.storeId = record.getStore().getId();
            this.recordDate = record.getRecordDate();
            this.notes = record.getNotes();
            this.sourceImagePath = record.getSourceImagePath();
            if (record.getAdditionalImages() != null) {
                this.additionalImages = record.getAdditionalImages().stream()
                        .map(img -> new ImageDTO(img.getId(), img.getImagePath()))
                        .collect(Collectors.toList());
            }
            this.items = itemsList.stream().map(item -> {
                DailyRecordItemDTO dto = new DailyRecordItemDTO();
                dto.setProductVariantId(item.getProductVariant().getId());
                dto.setOpeningStock(item.getOpeningStock());
                dto.setStockReceived(item.getStockReceived());
                dto.setSoldQuantity(item.getSoldQuantity());
                dto.setSellingPrice(item.getSellingPrice());
                return dto;
            }).collect(Collectors.toList());
        }
    }
}
