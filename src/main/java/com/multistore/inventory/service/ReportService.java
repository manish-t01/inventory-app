package com.multistore.inventory.service;

import com.multistore.inventory.entity.DailyRecord;
import com.multistore.inventory.entity.DailyRecordItem;
import com.multistore.inventory.entity.Store;
import com.multistore.inventory.repository.DailyRecordRepository;
import com.multistore.inventory.repository.DailyRecordItemRepository;
import com.multistore.inventory.repository.StoreRepository;
import com.multistore.inventory.dto.*;
import org.springframework.stereotype.Service;

import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;
import java.math.BigDecimal;

@Service
public class ReportService {
    private final DailyRecordRepository dailyRecordRepository;
    private final DailyRecordItemRepository dailyRecordItemRepository;
    private final StoreRepository storeRepository;

    public ReportService(DailyRecordRepository dailyRecordRepository, 
                         DailyRecordItemRepository dailyRecordItemRepository,
                         StoreRepository storeRepository) {
        this.dailyRecordRepository = dailyRecordRepository;
        this.dailyRecordItemRepository = dailyRecordItemRepository;
        this.storeRepository = storeRepository;
    }

    public ReportResponseDTO getPeriodReport(Long storeId, LocalDate startDate, LocalDate endDate) {
        List<Store> storesToProcess = new ArrayList<>();
        if (storeId != null && storeId > 0) {
            storeRepository.findById(storeId).ifPresent(storesToProcess::add);
        } else {
            storesToProcess = storeRepository.findAll();
        }

        ReportResponseDTO response = new ReportResponseDTO();
        List<StoreReportDTO> storeReports = new ArrayList<>();
        int grandSold = 0;
        BigDecimal grandSales = BigDecimal.ZERO;

        for (Store store : storesToProcess) {
            StoreReportDTO storeDto = new StoreReportDTO();
            storeDto.setStoreName(store.getName());
            
            List<DailyRecord> records = dailyRecordRepository
                .findByStoreIdAndRecordDateBetweenOrderByRecordDateAsc(store.getId(), startDate, endDate);
                
            if (records.isEmpty()) {
                storeDto.setOpeningStock(0);
                storeDto.setStockReceived(0);
                storeDto.setUnitsSold(0);
                storeDto.setClosingStock(0);
                storeDto.setTotalSales(BigDecimal.ZERO);
            } else {
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
                
                storeDto.setOpeningStock(periodOpening);
                storeDto.setStockReceived(totalReceived);
                storeDto.setUnitsSold(totalSold);
                storeDto.setClosingStock(periodClosing);
                storeDto.setTotalSales(totalSalesAmount);
            }
            
            storeReports.add(storeDto);
            grandSold += storeDto.getUnitsSold();
            grandSales = grandSales.add(storeDto.getTotalSales());
        }

        response.setStoreReports(storeReports);
        response.setGrandTotalUnitsSold(grandSold);
        response.setGrandTotalSales(grandSales);
        
        return response;
    }
}
