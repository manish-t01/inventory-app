import os

base_dir = r"D:\Coding\github\Projects\Rohit's Work\inventory-app\src\main\java\com\multistore\inventory\repository"

repositories = {
    "StoreRepository.java": """package com.multistore.inventory.repository;
import com.multistore.inventory.entity.Store;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface StoreRepository extends JpaRepository<Store, Long> {
}
""",
    "UserRepository.java": """package com.multistore.inventory.repository;
import com.multistore.inventory.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.Optional;

@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    Optional<User> findByUsername(String username);
}
""",
    "ProductRepository.java": """package com.multistore.inventory.repository;
import com.multistore.inventory.entity.Product;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ProductRepository extends JpaRepository<Product, Long> {
}
""",
    "ProductVariantRepository.java": """package com.multistore.inventory.repository;
import com.multistore.inventory.entity.ProductVariant;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.List;

@Repository
public interface ProductVariantRepository extends JpaRepository<ProductVariant, Long> {
    List<ProductVariant> findByProductId(Long productId);
}
""",
    "DailyRecordRepository.java": """package com.multistore.inventory.repository;
import com.multistore.inventory.entity.DailyRecord;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.time.LocalDate;
import java.util.Optional;

@Repository
public interface DailyRecordRepository extends JpaRepository<DailyRecord, Long> {
    Optional<DailyRecord> findByStoreIdAndRecordDate(Long storeId, LocalDate recordDate);
}
""",
    "DailyRecordItemRepository.java": """package com.multistore.inventory.repository;
import com.multistore.inventory.entity.DailyRecordItem;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.List;

@Repository
public interface DailyRecordItemRepository extends JpaRepository<DailyRecordItem, Long> {
    List<DailyRecordItem> findByDailyRecordId(Long dailyRecordId);
}
""",
    "InventoryTransactionRepository.java": """package com.multistore.inventory.repository;
import com.multistore.inventory.entity.InventoryTransaction;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface InventoryTransactionRepository extends JpaRepository<InventoryTransaction, Long> {
}
""",
    "SaleRepository.java": """package com.multistore.inventory.repository;
import com.multistore.inventory.entity.Sale;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface SaleRepository extends JpaRepository<Sale, Long> {
}
""",
    "PurchaseRepository.java": """package com.multistore.inventory.repository;
import com.multistore.inventory.entity.Purchase;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface PurchaseRepository extends JpaRepository<Purchase, Long> {
}
""",
    "StockAdjustmentRepository.java": """package com.multistore.inventory.repository;
import com.multistore.inventory.entity.StockAdjustment;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface StockAdjustmentRepository extends JpaRepository<StockAdjustment, Long> {
}
""",
    "ExpenseRepository.java": """package com.multistore.inventory.repository;
import com.multistore.inventory.entity.Expense;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ExpenseRepository extends JpaRepository<Expense, Long> {
}
"""
}

for name, content in repositories.items():
    with open(os.path.join(base_dir, name), "w", encoding="utf-8") as f:
        f.write(content)

print("Repositories created successfully.")
