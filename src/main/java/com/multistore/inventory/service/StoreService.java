package com.multistore.inventory.service;

import com.multistore.inventory.entity.Store;
import com.multistore.inventory.repository.StoreRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.multistore.inventory.repository.DailyRecordRepository;
import com.multistore.inventory.repository.DailyRecordItemRepository;
import com.multistore.inventory.repository.InventoryTransactionRepository;
import com.multistore.inventory.repository.PurchaseRepository;
import com.multistore.inventory.repository.SaleRepository;
import com.multistore.inventory.repository.ExpenseRepository;
import com.multistore.inventory.repository.StockAdjustmentRepository;
import com.multistore.inventory.entity.DailyRecord;

import java.util.List;

@Service
public class StoreService {
    private final StoreRepository storeRepository;
    private final DailyRecordRepository dailyRecordRepository;
    private final DailyRecordItemRepository dailyRecordItemRepository;
    private final InventoryTransactionRepository inventoryTransactionRepository;
    private final PurchaseRepository purchaseRepository;
    private final SaleRepository saleRepository;
    private final ExpenseRepository expenseRepository;
    private final StockAdjustmentRepository stockAdjustmentRepository;

    public StoreService(StoreRepository storeRepository,
                        DailyRecordRepository dailyRecordRepository,
                        DailyRecordItemRepository dailyRecordItemRepository,
                        InventoryTransactionRepository inventoryTransactionRepository,
                        PurchaseRepository purchaseRepository,
                        SaleRepository saleRepository,
                        ExpenseRepository expenseRepository,
                        StockAdjustmentRepository stockAdjustmentRepository) {
        this.storeRepository = storeRepository;
        this.dailyRecordRepository = dailyRecordRepository;
        this.dailyRecordItemRepository = dailyRecordItemRepository;
        this.inventoryTransactionRepository = inventoryTransactionRepository;
        this.purchaseRepository = purchaseRepository;
        this.saleRepository = saleRepository;
        this.expenseRepository = expenseRepository;
        this.stockAdjustmentRepository = stockAdjustmentRepository;
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

    @Transactional
    public Store createStore(String name) {
        if (name == null || name.trim().isEmpty()) {
            throw new RuntimeException("Store name cannot be empty");
        }
        Store store = new Store();
        store.setName(name.trim());
        return storeRepository.save(store);
    }

    @Transactional
    public void deleteStore(Long storeId) {
        Store store = storeRepository.findById(storeId)
            .orElseThrow(() -> new RuntimeException("Store not found"));

        // 1 & 2. Delete DailyRecordItems and DailyRecords
        List<DailyRecord> records = dailyRecordRepository.findByStoreId(storeId);
        for (DailyRecord record : records) {
            dailyRecordItemRepository.deleteByDailyRecordId(record.getId());
        }
        dailyRecordRepository.deleteByStoreId(storeId);

        // 3. Delete InventoryTransactions
        inventoryTransactionRepository.deleteByStoreId(storeId);

        // 4. Delete Purchases
        purchaseRepository.deleteByStoreId(storeId);

        // 5. Delete Sales
        saleRepository.deleteByStoreId(storeId);

        // 6. Delete Expenses
        expenseRepository.deleteByStoreId(storeId);

        // 7. Delete StockAdjustments
        stockAdjustmentRepository.deleteByStoreId(storeId);

        // 8. Delete Store
        storeRepository.delete(store);
    }
}
