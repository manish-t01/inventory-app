package com.multistore.inventory.service;

import com.multistore.inventory.entity.DailyRecord;
import com.multistore.inventory.entity.DailyRecordImage;
import com.multistore.inventory.repository.DailyRecordRepository;
import com.multistore.inventory.repository.DailyRecordImageRepository;
import org.springframework.stereotype.Service;
import org.springframework.util.StringUtils;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

@Service
public class FileStorageService {

    private final Path fileStorageLocation;
    private final DailyRecordRepository dailyRecordRepository;
    private final DailyRecordImageRepository dailyRecordImageRepository;

    public FileStorageService(DailyRecordRepository dailyRecordRepository, DailyRecordImageRepository dailyRecordImageRepository) {
        this.dailyRecordRepository = dailyRecordRepository;
        this.dailyRecordImageRepository = dailyRecordImageRepository;
        this.fileStorageLocation = Paths.get("uploads/daily-records").toAbsolutePath().normalize();

        try {
            Files.createDirectories(this.fileStorageLocation);
        } catch (Exception ex) {
            throw new RuntimeException("Could not create the directory where the uploaded files will be stored.", ex);
        }
    }

    public String storeFile(Long dailyRecordId, MultipartFile file) {
        return storeSingleFile(dailyRecordId, file, true);
    }

    public List<String> storeFiles(Long dailyRecordId, MultipartFile[] files) {
        List<String> fileNames = new ArrayList<>();
        for (MultipartFile file : files) {
            if (!file.isEmpty()) {
                fileNames.add(storeSingleFile(dailyRecordId, file, false));
            }
        }
        return fileNames;
    }

    private String storeSingleFile(Long dailyRecordId, MultipartFile file, boolean isLegacy) {
        String originalFileName = StringUtils.cleanPath(file.getOriginalFilename());
        
        try {
            if (originalFileName.contains("..")) {
                throw new RuntimeException("Sorry! Filename contains invalid path sequence " + originalFileName);
            }
            
            String extension = "";
            int i = originalFileName.lastIndexOf('.');
            if (i > 0) {
                extension = originalFileName.substring(i);
            }
            
            if (!extension.equalsIgnoreCase(".jpg") && !extension.equalsIgnoreCase(".jpeg") && !extension.equalsIgnoreCase(".png")) {
                throw new RuntimeException("Only JPG and PNG images are allowed.");
            }

            String newFileName = "store-record-" + dailyRecordId + "-" + UUID.randomUUID().toString() + extension;
            Path targetLocation = this.fileStorageLocation.resolve(newFileName);
            Files.copy(file.getInputStream(), targetLocation, StandardCopyOption.REPLACE_EXISTING);

            String imagePath = "uploads/daily-records/" + newFileName;

            DailyRecord record = dailyRecordRepository.findById(dailyRecordId)
                .orElseThrow(() -> new RuntimeException("Daily record not found"));
            
            if (isLegacy) {
                record.setSourceImagePath(imagePath);
                dailyRecordRepository.save(record);
            } else {
                DailyRecordImage image = new DailyRecordImage();
                image.setDailyRecord(record);
                image.setImagePath(imagePath);
                dailyRecordImageRepository.save(image);
            }

            return newFileName;
        } catch (IOException ex) {
            throw new RuntimeException("Could not store file " + originalFileName + ". Please try again!", ex);
        }
    }

    public void deleteImage(Long dailyRecordId, String imageId) {
        DailyRecord record = dailyRecordRepository.findById(dailyRecordId)
                .orElseThrow(() -> new RuntimeException("Daily record not found"));

        if ("legacy".equals(imageId)) {
            String path = record.getSourceImagePath();
            if (path != null) {
                deletePhysicalFile(path);
                record.setSourceImagePath(null);
                dailyRecordRepository.save(record);
            }
        } else {
            Long imgId = Long.parseLong(imageId);
            DailyRecordImage image = dailyRecordImageRepository.findById(imgId)
                    .orElseThrow(() -> new RuntimeException("Image not found"));
            
            if (!image.getDailyRecord().getId().equals(dailyRecordId)) {
                throw new RuntimeException("Image does not belong to this record");
            }
            
            deletePhysicalFile(image.getImagePath());
            dailyRecordImageRepository.delete(image);
        }
    }

    private void deletePhysicalFile(String imagePath) {
        try {
            // imagePath is "uploads/daily-records/filename.jpg"
            // We need to resolve against the project root or similar. 
            // fileStorageLocation is "uploads/daily-records" absolute path.
            String fileName = Paths.get(imagePath).getFileName().toString();
            Path filePath = this.fileStorageLocation.resolve(fileName).normalize();
            Files.deleteIfExists(filePath);
        } catch (Exception e) {
            // Log and ignore to prevent crashes if file doesn't exist
            System.err.println("Failed to delete physical file: " + imagePath);
        }
    }
}
