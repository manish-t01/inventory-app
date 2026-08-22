package com.multistore.inventory.dto;
import java.math.BigDecimal;
public class ProductVariantDTO {
    private Long id;
    private Long productId;
    private String size;
    private BigDecimal sellingPrice;
    private BigDecimal costPrice;
    private Integer minimumStock;
    private boolean active;
    // Getters and Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public Long getProductId() { return productId; }
    public void setProductId(Long productId) { this.productId = productId; }
    public String getSize() { return size; }
    public void setSize(String size) { this.size = size; }
    public BigDecimal getSellingPrice() { return sellingPrice; }
    public void setSellingPrice(BigDecimal sellingPrice) { this.sellingPrice = sellingPrice; }
    public BigDecimal getCostPrice() { return costPrice; }
    public void setCostPrice(BigDecimal costPrice) { this.costPrice = costPrice; }
    public Integer getMinimumStock() { return minimumStock; }
    public void setMinimumStock(Integer minimumStock) { this.minimumStock = minimumStock; }
    public boolean isActive() { return active; }
    public void setActive(boolean active) { this.active = active; }
}
