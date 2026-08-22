package com.multistore.inventory.service;

import com.multistore.inventory.dto.ProductDTO;
import com.multistore.inventory.dto.ProductVariantDTO;
import com.multistore.inventory.entity.Product;
import com.multistore.inventory.entity.ProductVariant;
import com.multistore.inventory.repository.ProductRepository;
import com.multistore.inventory.repository.ProductVariantRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.util.List;

@Service
public class ProductService {
    private final ProductRepository productRepository;
    private final ProductVariantRepository productVariantRepository;

    public ProductService(ProductRepository productRepository, ProductVariantRepository productVariantRepository) {
        this.productRepository = productRepository;
        this.productVariantRepository = productVariantRepository;
    }
    
    @Transactional
    public ProductVariant updateVariant(Long variantId, ProductVariantDTO dto) {
        ProductVariant pv = productVariantRepository.findById(variantId)
            .orElseThrow(() -> new RuntimeException("Variant not found"));
            
        if (dto.getSize() == null || dto.getSize().trim().isEmpty()) {
            throw new RuntimeException("Size cannot be empty");
        }
        if (dto.getSellingPrice() == null || dto.getSellingPrice().compareTo(BigDecimal.ZERO) < 0) {
            throw new RuntimeException("Selling price cannot be negative");
        }
        
        // Check for duplicates
        List<ProductVariant> existing = productVariantRepository.findByProductId(pv.getProduct().getId());
        for (ProductVariant v : existing) {
            if (!v.getId().equals(variantId) && v.getSize().equalsIgnoreCase(dto.getSize().trim())) {
                throw new RuntimeException("Variant size already exists for this product");
            }
        }

        pv.setSize(dto.getSize().trim());
        pv.setSellingPrice(dto.getSellingPrice());
        pv.setActive(dto.isActive());
        
        return productVariantRepository.save(pv);
    }
    public List<Product> getAllProducts() {
        return productRepository.findAll();
    }

    public Product getProduct(Long id) {
        return productRepository.findById(id).orElseThrow(() -> new RuntimeException("Product not found"));
    }

    @Transactional
    public Product createProduct(ProductDTO dto) {
        if (dto.getName() == null || dto.getName().trim().isEmpty()) {
            throw new RuntimeException("Product name cannot be empty");
        }
        Product p = new Product();
        p.setName(dto.getName());
        p.setCategory(dto.getCategory());
        p.setActive(true);
        return productRepository.save(p);
    }

    @Transactional
    public Product updateProduct(Long id, ProductDTO dto) {
        Product p = getProduct(id);
        if (dto.getName() == null || dto.getName().trim().isEmpty()) {
            throw new RuntimeException("Product name cannot be empty");
        }
        p.setName(dto.getName());
        p.setCategory(dto.getCategory());
        p.setActive(dto.isActive());
        return productRepository.save(p);
    }

    public List<ProductVariant> getVariants(Long productId) {
        return productVariantRepository.findByProductId(productId);
    }

    @Transactional
    public ProductVariant createVariant(Long productId, ProductVariantDTO dto) {
        Product p = getProduct(productId);
        if (dto.getSize() == null || dto.getSize().trim().isEmpty()) {
            throw new RuntimeException("Size cannot be empty");
        }
        if (dto.getSellingPrice() == null || dto.getSellingPrice().compareTo(BigDecimal.ZERO) < 0) {
            throw new RuntimeException("Selling price cannot be negative");
        }
        
        List<ProductVariant> existing = productVariantRepository.findByProductId(productId);
        for (ProductVariant v : existing) {
            if (v.getSize().equalsIgnoreCase(dto.getSize().trim())) {
                throw new RuntimeException("Variant size already exists for this product");
            }
        }

        ProductVariant pv = new ProductVariant();
        pv.setProduct(p);
        pv.setSize(dto.getSize().trim());
        pv.setSellingPrice(dto.getSellingPrice());
        pv.setCostPrice(dto.getCostPrice());
        pv.setMinimumStock(dto.getMinimumStock() != null ? dto.getMinimumStock() : 0);
        pv.setActive(true);
        return productVariantRepository.save(pv);
    }
}
