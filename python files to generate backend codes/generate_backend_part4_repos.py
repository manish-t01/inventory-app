import os

base_dir = r"D:\Coding\github\Projects\Rohit's Work\inventory-app\src\main\java\com\multistore\inventory"

# Additional Repository Methods
repos = {
    "DailyRecordRepository.java": """package com.multistore.inventory.repository;
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
}
""",
    "DailyRecordItemRepository.java": """package com.multistore.inventory.repository;
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
}
"""
}

for name, content in repos.items():
    with open(os.path.join(base_dir, "repository", name), "w", encoding="utf-8") as f:
        f.write(content)

# File Upload Configuration
config = {
    "WebConfig.java": """package com.multistore.inventory.config;

import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.ResourceHandlerRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

import java.nio.file.Path;
import java.nio.file.Paths;

@Configuration
public class WebConfig implements WebMvcConfigurer {
    @Override
    public void addResourceHandlers(ResourceHandlerRegistry registry) {
        Path uploadDir = Paths.get("uploads/daily-records");
        String uploadPath = uploadDir.toFile().getAbsolutePath();
        registry.addResourceHandler("/uploads/daily-records/**")
                .addResourceLocations("file:/" + uploadPath + "/");
    }
}
"""
}
os.makedirs(os.path.join(base_dir, "config"), exist_ok=True)
for name, content in config.items():
    with open(os.path.join(base_dir, "config", name), "w", encoding="utf-8") as f:
        f.write(content)

print("Repos and Config generated.")
