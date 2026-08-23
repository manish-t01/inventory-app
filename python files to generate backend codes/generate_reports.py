import os

base_dir = r"D:\Coding\github\Projects\Rohit's Work\inventory-app\src\main\java\com\multistore\inventory"

dtos = {
    "ReportAggregatedDTO.java": """package com.multistore.inventory.dto;

import java.math.BigDecimal;

public class ReportAggregatedDTO {
    private Integer openingStock;
    private Integer stockReceived;
    private Integer unitsSold;
    private Integer closingStock;
    private BigDecimal totalSales;

    // Getters and Setters
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
"""
}

for name, content in dtos.items():
    with open(os.path.join(base_dir, "dto", name), "w", encoding="utf-8") as f:
        f.write(content)

services = {
    "ReportService.java": """package com.multistore.inventory.service;

import com.multistore.inventory.entity.DailyRecord;
import com.multistore.inventory.entity.DailyRecordItem;
import com.multistore.inventory.repository.DailyRecordRepository;
import com.multistore.inventory.repository.DailyRecordItemRepository;
import com.multistore.inventory.dto.ReportDailyDTO;
import com.multistore.inventory.dto.DailyRecordItemDTO;
import com.multistore.inventory.dto.ReportAggregatedDTO;
import org.springframework.stereotype.Service;

import java.time.LocalDate;
import java.util.Optional;
import java.util.List;
import java.util.ArrayList;
import java.math.BigDecimal;

@Service
public class ReportService {
    private final DailyRecordRepository dailyRecordRepository;
    private final DailyRecordItemRepository dailyRecordItemRepository;

    public ReportService(DailyRecordRepository dailyRecordRepository, DailyRecordItemRepository dailyRecordItemRepository) {
        this.dailyRecordRepository = dailyRecordRepository;
        this.dailyRecordItemRepository = dailyRecordItemRepository;
    }

    public ReportDailyDTO getDailyReport(Long storeId, LocalDate date) {
        ReportDailyDTO report = new ReportDailyDTO();
        report.setItems(new ArrayList<>());
        
        Optional<DailyRecord> recordOpt = dailyRecordRepository.findByStoreIdAndRecordDate(storeId, date);
        if (recordOpt.isEmpty()) {
            return report;
        }
        
        DailyRecord record = recordOpt.get();
        List<DailyRecordItem> items = dailyRecordItemRepository.findByDailyRecordId(record.getId());
        
        int totalOpening = 0;
        int totalReceived = 0;
        int totalAvailable = 0;
        int totalSold = 0;
        int totalClosing = 0;
        BigDecimal totalSalesAmount = BigDecimal.ZERO;
        
        List<DailyRecordItemDTO> itemDTOs = new ArrayList<>();
        
        for (DailyRecordItem item : items) {
            totalOpening += item.getOpeningStock();
            totalReceived += item.getStockReceived();
            totalAvailable += item.getTotalAvailable();
            totalSold += item.getSoldQuantity();
            totalClosing += item.getClosingStock();
            totalSalesAmount = totalSalesAmount.add(item.getSalesAmount());
            
            DailyRecordItemDTO dto = new DailyRecordItemDTO();
            dto.setProductVariantId(item.getProductVariant().getId());
            dto.setOpeningStock(item.getOpeningStock());
            dto.setStockReceived(item.getStockReceived());
            dto.setSoldQuantity(item.getSoldQuantity());
            dto.setSellingPrice(item.getSellingPrice());
            itemDTOs.add(dto);
        }
        
        report.setTotalOpening(totalOpening);
        report.setTotalReceived(totalReceived);
        report.setTotalAvailable(totalAvailable);
        report.setTotalSold(totalSold);
        report.setTotalClosing(totalClosing);
        report.setTotalSalesAmount(totalSalesAmount);
        report.setItems(itemDTOs);
        
        return report;
    }

    public ReportAggregatedDTO getAggregatedReport(Long storeId, LocalDate startDate, LocalDate endDate) {
        ReportAggregatedDTO report = new ReportAggregatedDTO();
        List<DailyRecord> records = dailyRecordRepository.findByStoreIdAndRecordDateBetweenOrderByRecordDateAsc(storeId, startDate, endDate);
        
        if (records.isEmpty()) {
            report.setOpeningStock(0);
            report.setStockReceived(0);
            report.setUnitsSold(0);
            report.setClosingStock(0);
            report.setTotalSales(BigDecimal.ZERO);
            return report;
        }

        // Logic for opening stock from FIRST record, closing from LAST record
        DailyRecord firstRecord = records.get(0);
        DailyRecord lastRecord = records.get(records.size() - 1);
        
        List<DailyRecordItem> firstItems = dailyRecordItemRepository.findByDailyRecordId(firstRecord.getId());
        int periodOpening = firstItems.stream().mapToInt(DailyRecordItem::getOpeningStock).sum();
        
        List<DailyRecordItem> lastItems = dailyRecordItemRepository.findByDailyRecordId(lastRecord.getId());
        int periodClosing = lastItems.stream().mapToInt(DailyRecordItem::getClosingStock).sum();
        
        int totalReceived = 0;
        int totalSold = 0;
        BigDecimal totalSalesAmount = BigDecimal.ZERO;
        
        for (DailyRecord record : records) {
            List<DailyRecordItem> items = dailyRecordItemRepository.findByDailyRecordId(record.getId());
            for(DailyRecordItem item : items) {
                totalReceived += item.getStockReceived();
                totalSold += item.getSoldQuantity();
                totalSalesAmount = totalSalesAmount.add(item.getSalesAmount());
            }
        }
        
        report.setOpeningStock(periodOpening);
        report.setStockReceived(totalReceived);
        report.setUnitsSold(totalSold);
        report.setClosingStock(periodClosing);
        report.setTotalSales(totalSalesAmount);
        
        return report;
    }
}
"""
}

for name, content in services.items():
    with open(os.path.join(base_dir, "service", name), "w", encoding="utf-8") as f:
        f.write(content)

controllers = {
    "ReportController.java": """package com.multistore.inventory.controller;

import com.multistore.inventory.dto.ReportDailyDTO;
import com.multistore.inventory.dto.ReportAggregatedDTO;
import com.multistore.inventory.service.ReportService;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDate;

@RestController
@RequestMapping("/api/reports")
public class ReportController {
    private final ReportService reportService;

    public ReportController(ReportService reportService) {
        this.reportService = reportService;
    }

    @GetMapping("/daily")
    public ResponseEntity<ReportDailyDTO> getDailyReport(
            @RequestParam Long storeId,
            @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate date) {
        
        ReportDailyDTO report = reportService.getDailyReport(storeId, date);
        return ResponseEntity.ok(report);
    }
    
    @GetMapping("/weekly")
    public ResponseEntity<ReportAggregatedDTO> getWeeklyReport(
            @RequestParam Long storeId,
            @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate startDate,
            @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate endDate) {
        
        ReportAggregatedDTO report = reportService.getAggregatedReport(storeId, startDate, endDate);
        return ResponseEntity.ok(report);
    }

    @GetMapping("/monthly")
    public ResponseEntity<ReportAggregatedDTO> getMonthlyReport(
            @RequestParam Long storeId,
            @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate startDate,
            @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate endDate) {
        
        ReportAggregatedDTO report = reportService.getAggregatedReport(storeId, startDate, endDate);
        return ResponseEntity.ok(report);
    }

    @GetMapping("/yearly")
    public ResponseEntity<ReportAggregatedDTO> getYearlyReport(
            @RequestParam Long storeId,
            @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate startDate,
            @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate endDate) {
        
        ReportAggregatedDTO report = reportService.getAggregatedReport(storeId, startDate, endDate);
        return ResponseEntity.ok(report);
    }
}
"""
}

for name, content in controllers.items():
    with open(os.path.join(base_dir, "controller", name), "w", encoding="utf-8") as f:
        f.write(content)

print("Report logic generated successfully.")
