package com.multistore.inventory.service;

import com.multistore.inventory.dto.ReportResponseDTO;
import com.multistore.inventory.dto.StoreReportDTO;
import org.springframework.stereotype.Service;
import java.io.PrintWriter;

@Service
public class CsvService {
    public void generateCsv(PrintWriter writer, ReportResponseDTO data) {
        writer.println("Store,Opening Stock,Received,Units Sold,Closing Stock,Total Sales");
        for (StoreReportDTO store : data.getStoreReports()) {
            writer.printf("%s,%d,%d,%d,%d,%s%n",
                store.getStoreName().replace(",", ""),
                store.getOpeningStock(),
                store.getStockReceived(),
                store.getUnitsSold(),
                store.getClosingStock(),
                store.getTotalSales().toString());
        }
        writer.println();
        writer.println("GRAND TOTALS,,," + data.getGrandTotalUnitsSold() + ",," + data.getGrandTotalSales());
    }
}
