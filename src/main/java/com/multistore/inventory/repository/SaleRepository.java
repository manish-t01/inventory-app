package com.multistore.inventory.repository;
import com.multistore.inventory.entity.Sale;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface SaleRepository extends JpaRepository<Sale, Long> {
    void deleteBySourceAndProductVariantId(String source, Long productVariantId);
    void deleteByStoreId(Long storeId);
}
