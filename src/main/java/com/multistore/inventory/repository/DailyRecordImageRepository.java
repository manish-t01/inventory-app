package com.multistore.inventory.repository;

import com.multistore.inventory.entity.DailyRecordImage;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface DailyRecordImageRepository extends JpaRepository<DailyRecordImage, Long> {
    List<DailyRecordImage> findByDailyRecordId(Long dailyRecordId);
}
