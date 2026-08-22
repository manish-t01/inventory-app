package com.multistore.inventory.controller;

import com.multistore.inventory.dto.ProductDTO;
import com.multistore.inventory.dto.ProductVariantDTO;
import com.multistore.inventory.entity.Product;
import com.multistore.inventory.entity.ProductVariant;
import com.multistore.inventory.service.ProductService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/products")
public class ProductController {
    private final ProductService productService;

    public ProductController(ProductService productService) {
        this.productService = productService;
    }
    
    @PutMapping("/{id}")
    public ResponseEntity<?> updateProduct(@PathVariable Long id, @RequestBody ProductDTO dto) {
        try {
            return ResponseEntity.ok(productService.updateProduct(id, dto));
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(e.getMessage());
        }
    }

    @PutMapping("/{productId}/variants/{variantId}")
    public ResponseEntity<?> updateVariant(@PathVariable Long productId, @PathVariable Long variantId, @RequestBody ProductVariantDTO dto) {
        try {
            return ResponseEntity.ok(productService.updateVariant(variantId, dto));
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(e.getMessage());
        }
    }
    @GetMapping
    public List<Product> getAll() {
        return productService.getAllProducts();
    }

    @PostMapping
    public ResponseEntity<?> createProduct(@RequestBody ProductDTO dto) {
        try {
            return ResponseEntity.ok(productService.createProduct(dto));
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(e.getMessage());
        }
    }

    @GetMapping("/{id}/variants")
    public List<ProductVariant> getVariants(@PathVariable Long id) {
        return productService.getVariants(id);
    }

    @PostMapping("/{id}/variants")
    public ResponseEntity<?> createVariant(@PathVariable Long id, @RequestBody ProductVariantDTO dto) {
        try {
            return ResponseEntity.ok(productService.createVariant(id, dto));
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(e.getMessage());
        }
    }
}
