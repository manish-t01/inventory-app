package com.multistore.inventory.controller;

import com.multistore.inventory.entity.Store;
import com.multistore.inventory.service.StoreService;
import com.multistore.inventory.dto.StoreDTO;
import org.springframework.http.ResponseEntity;
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
    public List<Store> getAllStores() {
        return storeService.getAllStores();
    }
    
    @PutMapping("/{id}")
    public ResponseEntity<?> updateStore(@PathVariable Long id, @RequestBody StoreDTO dto) {
        try {
            Store updated = storeService.updateStore(id, dto.getName());
            return ResponseEntity.ok(updated);
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(e.getMessage());
        }
    }
}
