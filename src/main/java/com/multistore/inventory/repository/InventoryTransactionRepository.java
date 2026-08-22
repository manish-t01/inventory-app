package com.multistore.inventory.repository;
import com.multistore.inventory.entity.InventoryTransaction;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface InventoryTransactionRepository extends JpaRepository<InventoryTransaction, Long> {
    void deleteByReferenceIdAndProductVariantId(String referenceId, Long productVariantId);
    void deleteByReferenceId(String referenceId);
    void deleteByStoreId(Long storeId);
}
