package com.multistore.inventory.service;

import com.lowagie.text.*;
import com.lowagie.text.pdf.PdfPCell;
import com.lowagie.text.pdf.PdfPTable;
import com.lowagie.text.pdf.PdfWriter;
import com.multistore.inventory.dto.ReportResponseDTO;
import com.multistore.inventory.dto.StoreReportDTO;
import org.springframework.stereotype.Service;

import java.io.ByteArrayOutputStream;
import java.time.LocalDate;

@Service
public class PdfService {

    public byte[] generateReportPdf(String reportType, String period, ReportResponseDTO data) throws Exception {
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        Document document = new Document(PageSize.A4.rotate());
        PdfWriter.getInstance(document, out);

        document.open();

        Font titleFont = FontFactory.getFont(FontFactory.HELVETICA_BOLD, 18);
        Font subtitleFont = FontFactory.getFont(FontFactory.HELVETICA, 12);
        Font tableHeaderFont = FontFactory.getFont(FontFactory.HELVETICA_BOLD, 10);
        Font tableBodyFont = FontFactory.getFont(FontFactory.HELVETICA, 10);

        Paragraph title = new Paragraph("INVENTORY REPORT - " + reportType.toUpperCase(), titleFont);
        title.setAlignment(Element.ALIGN_CENTER);
        document.add(title);
        
        Paragraph periodPara = new Paragraph("Period: " + period, subtitleFont);
        periodPara.setAlignment(Element.ALIGN_CENTER);
        periodPara.setSpacingAfter(20);
        document.add(periodPara);

        for (StoreReportDTO store : data.getStoreReports()) {
            Paragraph storeName = new Paragraph("Store: " + store.getStoreName(), FontFactory.getFont(FontFactory.HELVETICA_BOLD, 14));
            storeName.setSpacingAfter(10);
            document.add(storeName);

            PdfPTable table = new PdfPTable(5);
            table.setWidthPercentage(100);

            addCell(table, "Opening Stock", tableHeaderFont);
            addCell(table, "Received", tableHeaderFont);
            addCell(table, "Units Sold", tableHeaderFont);
            addCell(table, "Closing Stock", tableHeaderFont);
            addCell(table, "Total Sales", tableHeaderFont);

            addCell(table, String.valueOf(store.getOpeningStock()), tableBodyFont);
            addCell(table, String.valueOf(store.getStockReceived()), tableBodyFont);
            addCell(table, String.valueOf(store.getUnitsSold()), tableBodyFont);
            addCell(table, String.valueOf(store.getClosingStock()), tableBodyFont);
            addCell(table, "Rs " + store.getTotalSales().toString(), tableBodyFont);

            document.add(table);
            document.add(new Paragraph(" "));
        }

        Paragraph grandTotals = new Paragraph("GRAND TOTALS", FontFactory.getFont(FontFactory.HELVETICA_BOLD, 14));
        grandTotals.setSpacingBefore(10);
        grandTotals.setSpacingAfter(10);
        document.add(grandTotals);

        PdfPTable totalTable = new PdfPTable(2);
        totalTable.setWidthPercentage(50);
        totalTable.setHorizontalAlignment(Element.ALIGN_LEFT);
        
        addCell(totalTable, "Combined Units Sold", tableHeaderFont);
        addCell(totalTable, "Combined Sales", tableHeaderFont);
        addCell(totalTable, String.valueOf(data.getGrandTotalUnitsSold()), tableBodyFont);
        addCell(totalTable, "Rs " + data.getGrandTotalSales().toString(), tableBodyFont);

        document.add(totalTable);

        java.time.format.DateTimeFormatter dtf = java.time.format.DateTimeFormatter.ofPattern("dd-MM-yyyy");
        Paragraph generatedDate = new Paragraph("Generated on: " + LocalDate.now().format(dtf), FontFactory.getFont(FontFactory.HELVETICA_OBLIQUE, 8));
        generatedDate.setAlignment(Element.ALIGN_RIGHT);
        document.add(generatedDate);

        document.close();
        return out.toByteArray();
    }

    private void addCell(PdfPTable table, String text, Font font) {
        PdfPCell cell = new PdfPCell(new Phrase(text, font));
        cell.setPadding(5);
        table.addCell(cell);
    }
}
