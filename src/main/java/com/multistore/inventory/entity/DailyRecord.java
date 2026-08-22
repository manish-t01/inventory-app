package com.multistore.inventory.entity;
import jakarta.persistence.*;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.List;
import java.util.ArrayList;

@Entity
@Table(name = "daily_records")
public class DailyRecord {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "store_id", nullable = false)
    private Store store;

    @Column(nullable = false)
    private LocalDate recordDate;

    @Column(columnDefinition = "TEXT")
    private String notes;

    private String sourceImagePath;

    @OneToMany(mappedBy = "dailyRecord", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<DailyRecordImage> additionalImages = new ArrayList<>();

    @Column(updatable = false)
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;

    @PrePersist
    protected void onCreate() {
        createdAt = LocalDateTime.now();
        updatedAt = LocalDateTime.now();
    }

    @PreUpdate
    protected void onUpdate() {
        updatedAt = LocalDateTime.now();
    }

    // Getters and Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public Store getStore() { return store; }
    public void setStore(Store store) { this.store = store; }
    public LocalDate getRecordDate() { return recordDate; }
    public void setRecordDate(LocalDate recordDate) { this.recordDate = recordDate; }
    public String getNotes() { return notes; }
    public void setNotes(String notes) { this.notes = notes; }
    public String getSourceImagePath() { return sourceImagePath; }
    public void setSourceImagePath(String sourceImagePath) { this.sourceImagePath = sourceImagePath; }
    public List<DailyRecordImage> getAdditionalImages() { return additionalImages; }
    public void setAdditionalImages(List<DailyRecordImage> additionalImages) { this.additionalImages = additionalImages; }
    public LocalDateTime getCreatedAt() { return createdAt; }
    public LocalDateTime getUpdatedAt() { return updatedAt; }
}
