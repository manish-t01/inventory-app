package com.multistore.inventory.controller;

import com.multistore.inventory.dto.ReportResponseDTO;
import com.multistore.inventory.service.ReportService;
import com.multistore.inventory.service.PdfService;
import com.multistore.inventory.service.CsvService;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import jakarta.servlet.http.HttpServletResponse;

import java.time.LocalDate;

@RestController
@RequestMapping("/api/reports")
public class ReportController {
    private final ReportService reportService;
    private final PdfService pdfService;
    private final CsvService csvService;

    public ReportController(ReportService reportService, PdfService pdfService, CsvService csvService) {
        this.reportService = reportService;
        this.pdfService = pdfService;
        this.csvService = csvService;
    }

    @GetMapping("/period")
    public ResponseEntity<ReportResponseDTO> getPeriodReport(
            @RequestParam(required = false) Long storeId,
            @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate startDate,
            @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate endDate) {
        return ResponseEntity.ok(reportService.getPeriodReport(storeId, startDate, endDate));
    }

    @GetMapping("/period/pdf")
    public ResponseEntity<byte[]> getPeriodReportPdf(
            @RequestParam(required = false) Long storeId,
            @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate startDate,
            @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate endDate,
            @RequestParam String reportType) {
        try {
            ReportResponseDTO data = reportService.getPeriodReport(storeId, startDate, endDate);
            byte[] pdfBytes = pdfService.generateReportPdf(reportType, startDate + " to " + endDate, data);
            
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_PDF);
            String filename = "inventory-" + reportType.toLowerCase() + "-" + LocalDate.now() + ".pdf";
            headers.setContentDispositionFormData("filename", filename);
            headers.setCacheControl("must-revalidate, post-check=0, pre-check=0");
            
            return ResponseEntity.ok().headers(headers).body(pdfBytes);
        } catch (Exception e) {
            return ResponseEntity.internalServerError().build();
        }
    }

    @GetMapping("/period/csv")
    public void getPeriodReportCsv(
            @RequestParam(required = false) Long storeId,
            @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate startDate,
            @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate endDate,
            HttpServletResponse response) {
        try {
            ReportResponseDTO data = reportService.getPeriodReport(storeId, startDate, endDate);
            response.setContentType("text/csv");
            response.setHeader("Content-Disposition", "attachment; filename=\"inventory-report-" + LocalDate.now() + ".csv\"");
            csvService.generateCsv(response.getWriter(), data);
        } catch (Exception e) {
            response.setStatus(500);
        }
    }
}
