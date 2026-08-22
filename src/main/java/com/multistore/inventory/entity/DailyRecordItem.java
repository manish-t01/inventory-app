package com.multistore.inventory.entity;
import jakarta.persistence.*;
import java.math.BigDecimal;
import java.time.LocalDateTime;

@Entity
@Table(name = "daily_record_items")
public class DailyRecordItem {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "daily_record_id", nullable = false)
    private DailyRecord dailyRecord;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "product_variant_id", nullable = false)
    private ProductVariant productVariant;

    private Integer openingStock;
    private Integer stockReceived;
    private Integer totalAvailable;
    private Integer soldQuantity;
    private Integer closingStock;
    private BigDecimal sellingPrice;
    private BigDecimal salesAmount;
    
    @Column(updatable = false)
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;

    @PrePersist
    protected void onCreate() {
        createdAt = LocalDateTime.now();
        updatedAt = LocalDateTime.now();
    }

    @PreUpdate
    protected void onUpdate() {
        updatedAt = LocalDateTime.now();
    }

    // Getters and Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public DailyRecord getDailyRecord() { return dailyRecord; }
    public void setDailyRecord(DailyRecord dailyRecord) { this.dailyRecord = dailyRecord; }
    public ProductVariant getProductVariant() { return productVariant; }
    public void setProductVariant(ProductVariant productVariant) { this.productVariant = productVariant; }
    public Integer getOpeningStock() { return openingStock; }
    public void setOpeningStock(Integer openingStock) { this.openingStock = openingStock; }
    public Integer getStockReceived() { return stockReceived; }
    public void setStockReceived(Integer stockReceived) { this.stockReceived = stockReceived; }
    public Integer getTotalAvailable() { return totalAvailable; }
    public void setTotalAvailable(Integer totalAvailable) { this.totalAvailable = totalAvailable; }
    public Integer getSoldQuantity() { return soldQuantity; }
    public void setSoldQuantity(Integer soldQuantity) { this.soldQuantity = soldQuantity; }
    public Integer getClosingStock() { return closingStock; }
    public void setClosingStock(Integer closingStock) { this.closingStock = closingStock; }
    public BigDecimal getSellingPrice() { return sellingPrice; }
    public void setSellingPrice(BigDecimal sellingPrice) { this.sellingPrice = sellingPrice; }
    public BigDecimal getSalesAmount() { return salesAmount; }
    public void setSalesAmount(BigDecimal salesAmount) { this.salesAmount = salesAmount; }
    public LocalDateTime getCreatedAt() { return createdAt; }
    public LocalDateTime getUpdatedAt() { return updatedAt; }
}
