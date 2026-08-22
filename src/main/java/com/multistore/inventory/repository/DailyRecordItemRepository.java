package com.multistore.inventory.repository;
import com.multistore.inventory.entity.DailyRecordItem;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;
import java.time.LocalDate;
import java.util.List;
import java.util.Optional;

@Repository
public interface DailyRecordItemRepository extends JpaRepository<DailyRecordItem, Long> {
    List<DailyRecordItem> findByDailyRecordId(Long dailyRecordId);
    
    @Query("SELECT i FROM DailyRecordItem i JOIN i.dailyRecord r WHERE r.store.id = :storeId AND i.productVariant.id = :variantId AND r.recordDate < :date ORDER BY r.recordDate DESC LIMIT 1")
    Optional<DailyRecordItem> findTopByStoreIdAndProductVariantIdAndRecordDateLessThanOrderByRecordDateDesc(
        @Param("storeId") Long storeId, 
        @Param("variantId") Long variantId, 
        @Param("date") LocalDate date
    );
    void deleteByDailyRecordIdAndProductVariantId(Long dailyRecordId, Long productVariantId);
    void deleteByDailyRecordId(Long dailyRecordId);
}
