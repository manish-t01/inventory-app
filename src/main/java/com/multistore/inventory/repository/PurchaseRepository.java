package com.multistore.inventory.repository;
import com.multistore.inventory.entity.Purchase;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface PurchaseRepository extends JpaRepository<Purchase, Long> {
    void deleteByStoreId(Long storeId);
}
