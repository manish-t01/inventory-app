package com.multistore.inventory.dto;
import java.math.BigDecimal;
import java.util.List;
public class ReportResponseDTO {
    private List<StoreReportDTO> storeReports;
    private Integer grandTotalUnitsSold;
    private BigDecimal grandTotalSales;
    
    // Getters and Setters
    public List<StoreReportDTO> getStoreReports() { return storeReports; }
    public void setStoreReports(List<StoreReportDTO> storeReports) { this.storeReports = storeReports; }
    public Integer getGrandTotalUnitsSold() { return grandTotalUnitsSold; }
    public void setGrandTotalUnitsSold(Integer grandTotalUnitsSold) { this.grandTotalUnitsSold = grandTotalUnitsSold; }
    public BigDecimal getGrandTotalSales() { return grandTotalSales; }
    public void setGrandTotalSales(BigDecimal grandTotalSales) { this.grandTotalSales = grandTotalSales; }
}
