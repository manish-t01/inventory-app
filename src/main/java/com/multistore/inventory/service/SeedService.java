package com.multistore.inventory.service;

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
