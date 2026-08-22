package com.multistore.inventory.dto;

import java.math.BigDecimal;

public class DailyRecordItemDTO {
    private Long productVariantId;
    private Integer openingStock;
    private Integer stockReceived;
    private Integer soldQuantity;
    private BigDecimal sellingPrice;
    
    // Getters and Setters
    public Long getProductVariantId() { return productVariantId; }
    public void setProductVariantId(Long productVariantId) { this.productVariantId = productVariantId; }
    public Integer getOpeningStock() { return openingStock; }
    public void setOpeningStock(Integer openingStock) { this.openingStock = openingStock; }
    public Integer getStockReceived() { return stockReceived; }
    public void setStockReceived(Integer stockReceived) { this.stockReceived = stockReceived; }
    public Integer getSoldQuantity() { return soldQuantity; }
    public void setSoldQuantity(Integer soldQuantity) { this.soldQuantity = soldQuantity; }
    public BigDecimal getSellingPrice() { return sellingPrice; }
    public void setSellingPrice(BigDecimal sellingPrice) { this.sellingPrice = sellingPrice; }
}
