package com.multistore.inventory.repository;
import com.multistore.inventory.entity.DailyRecord;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.time.LocalDate;
import java.util.Optional;
import java.util.List;

@Repository
public interface DailyRecordRepository extends JpaRepository<DailyRecord, Long> {
    Optional<DailyRecord> findByStoreIdAndRecordDate(Long storeId, LocalDate recordDate);
    List<DailyRecord> findByStoreIdAndRecordDateBetweenOrderByRecordDateAsc(Long storeId, LocalDate startDate, LocalDate endDate);
    List<DailyRecord> findByStoreId(Long storeId);
    void deleteByStoreId(Long storeId);
}
