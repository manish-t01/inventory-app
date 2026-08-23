import os

base_dir = r"D:\Coding\github\Projects\Rohit's Work\inventory-app\src\main\java\com\multistore\inventory"

services = {
    "ReportService.java": """package com.multistore.inventory.service;

import com.multistore.inventory.entity.DailyRecord;
import com.multistore.inventory.entity.DailyRecordItem;
import com.multistore.inventory.repository.DailyRecordRepository;
import com.multistore.inventory.repository.DailyRecordItemRepository;
import com.multistore.inventory.dto.ReportDailyDTO;
import com.multistore.inventory.dto.DailyRecordItemDTO;
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
            // In a full implementation, we'd add fields like product name, size, total, closing, amount to the DTO
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
}
"""
}

for name, content in services.items():
    with open(os.path.join(base_dir, "service", name), "w", encoding="utf-8") as f:
        f.write(content)

controllers = {
    "ReportController.java": """package com.multistore.inventory.controller;

import com.multistore.inventory.dto.ReportDailyDTO;
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
}
"""
}

for name, content in controllers.items():
    with open(os.path.join(base_dir, "controller", name), "w", encoding="utf-8") as f:
        f.write(content)

print("Report backend Part 3 generated successfully.")
