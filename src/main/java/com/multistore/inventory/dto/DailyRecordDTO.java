package com.multistore.inventory.dto;

import java.time.LocalDate;
import java.util.List;

public class DailyRecordDTO {
    private Long storeId;
    private LocalDate recordDate;
    private String notes;
    private List<DailyRecordItemDTO> items;

    // Getters and Setters
    public Long getStoreId() { return storeId; }
    public void setStoreId(Long storeId) { this.storeId = storeId; }
    public LocalDate getRecordDate() { return recordDate; }
    public void setRecordDate(LocalDate recordDate) { this.recordDate = recordDate; }
    public String getNotes() { return notes; }
    public void setNotes(String notes) { this.notes = notes; }
    public List<DailyRecordItemDTO> getItems() { return items; }
    public void setItems(List<DailyRecordItemDTO> items) { this.items = items; }
}
