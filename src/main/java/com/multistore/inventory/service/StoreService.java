package com.multistore.inventory.service;

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
    
    public Store updateStore(Long id, String newName) {
        if (newName == null || newName.trim().isEmpty()) {
            throw new RuntimeException("Store name cannot be empty");
        }
        Store store = storeRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Store not found"));
        store.setName(newName.trim());
        return storeRepository.save(store);
    }
}
