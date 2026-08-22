package com.multistore.inventory.dto;
import java.math.BigDecimal;
public class StoreReportDTO {
    private String storeName;
    private Integer openingStock;
    private Integer stockReceived;
    private Integer unitsSold;
    private Integer closingStock;
    private BigDecimal totalSales;
    // Getters and Setters
    public String getStoreName() { return storeName; }
    public void setStoreName(String storeName) { this.storeName = storeName; }
    public Integer getOpeningStock() { return openingStock; }
    public void setOpeningStock(Integer openingStock) { this.openingStock = openingStock; }
    public Integer getStockReceived() { return stockReceived; }
    public void setStockReceived(Integer stockReceived) { this.stockReceived = stockReceived; }
    public Integer getUnitsSold() { return unitsSold; }
    public void setUnitsSold(Integer unitsSold) { this.unitsSold = unitsSold; }
    public Integer getClosingStock() { return closingStock; }
    public void setClosingStock(Integer closingStock) { this.closingStock = closingStock; }
    public BigDecimal getTotalSales() { return totalSales; }
    public void setTotalSales(BigDecimal totalSales) { this.totalSales = totalSales; }
}
