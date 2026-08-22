package com.multistore.inventory.dto;
import java.util.List;
import java.math.BigDecimal;
public class ReportDailyDTO {
    private Integer totalOpening;
    private Integer totalReceived;
    private Integer totalAvailable;
    private Integer totalSold;
    private Integer totalClosing;
    private BigDecimal totalSalesAmount;
    private List<DailyRecordItemDTO> items; // Can reuse or create specific report item DTO
    // Getters and setters...
    public Integer getTotalOpening() { return totalOpening; }
    public void setTotalOpening(Integer totalOpening) { this.totalOpening = totalOpening; }
    public Integer getTotalReceived() { return totalReceived; }
    public void setTotalReceived(Integer totalReceived) { this.totalReceived = totalReceived; }
    public Integer getTotalAvailable() { return totalAvailable; }
    public void setTotalAvailable(Integer totalAvailable) { this.totalAvailable = totalAvailable; }
    public Integer getTotalSold() { return totalSold; }
    public void setTotalSold(Integer totalSold) { this.totalSold = totalSold; }
    public Integer getTotalClosing() { return totalClosing; }
    public void setTotalClosing(Integer totalClosing) { this.totalClosing = totalClosing; }
    public BigDecimal getTotalSalesAmount() { return totalSalesAmount; }
    public void setTotalSalesAmount(BigDecimal totalSalesAmount) { this.totalSalesAmount = totalSalesAmount; }
    public List<DailyRecordItemDTO> getItems() { return items; }
    public void setItems(List<DailyRecordItemDTO> items) { this.items = items; }
}
