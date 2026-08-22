let currentProducts = [];
let currentVariants = [];
let activeProductId = null;
let editProductId = null;
let editVariantId = null;

document.addEventListener('DOMContentLoaded', () => {
    loadProducts();
});

async function loadProducts() {
    try {
        currentProducts = await fetchProducts();
        renderProductsTable();
    } catch(e) {
        document.querySelector('#productsTable tbody').innerHTML = '<tr><td colspan="5" class="error-msg">Failed to load products.</td></tr>';
    }
}

function renderProductsTable() {
    const tbody = document.querySelector('#productsTable tbody');
    const searchTerm = document.getElementById('productSearch').value.toLowerCase();
    
    const filtered = currentProducts.filter(p => p.name.toLowerCase().includes(searchTerm));
    
    if (filtered.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" style="text-align:center; padding: 20px;">No products found. <br><button onclick="openProductModal()" style="margin-top:10px;">+ Add your first product</button></td></tr>';
        return;
    }
    
    tbody.innerHTML = '';
    filtered.forEach(p => {
        const tr = document.createElement('tr');
        const badge = p.active ? '<span class="badge-active">ACTIVE</span>' : '<span class="badge-inactive">INACTIVE</span>';
        
        tr.innerHTML = `
            <td>${p.id}</td>
            <td>${p.name}</td>
            <td>${p.category || '-'}</td>
            <td>${badge}</td>
            <td>
                <button onclick="openProductModal(${p.id})">Edit</button>
                <button class="btn-primary" onclick="openVariantsModal(${p.id}, '${p.name.replace(/'/g, "\'")}')">Manage Variants</button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

function filterProducts() {
    renderProductsTable();
}

function openProductModal(id = null) {
    editProductId = id;
    const modal = document.getElementById('productModal');
    const title = document.getElementById('productModalTitle');
    const msg = document.getElementById('messageBox');
    const statusGrp = document.getElementById('prodStatusGroup');
    
    msg.innerHTML = '';
    
    if (id) {
        const p = currentProducts.find(x => x.id === id);
        title.textContent = 'Edit Product';
        document.getElementById('prodName').value = p.name;
        document.getElementById('prodCategory').value = p.category || '';
        document.getElementById('prodActive').value = p.active ? "true" : "false";
        statusGrp.style.display = 'block';
    } else {
        title.textContent = 'Add Product';
        document.getElementById('prodName').value = '';
        document.getElementById('prodCategory').value = '';
        statusGrp.style.display = 'none';
    }
    
    modal.style.display = 'block';
}

function closeProductModal() {
    document.getElementById('productModal').style.display = 'none';
}

async function saveProduct() {
    const name = document.getElementById('prodName').value.trim();
    const category = document.getElementById('prodCategory').value.trim();
    const active = document.getElementById('prodActive').value === 'true';
    const msg = document.getElementById('messageBox');
    const btn = document.getElementById('saveProdBtn');
    
    if (!name) {
        msg.innerHTML = '<span class="error-msg">Product name is required.</span>';
        return;
    }
    
    btn.disabled = true;
    msg.innerHTML = 'Saving...';
    
    const payload = { name, category, active: editProductId ? active : true };
    
    try {
        const url = editProductId ? `/api/products/${editProductId}` : '/api/products';
        const method = editProductId ? 'PUT' : 'POST';
        
        const res = await fetch(url, {
            method,
            headers: {'Content-Type':'application/json'},
            body: JSON.stringify(payload)
        });
        
        if (res.ok) {
            msg.innerHTML = '<span class="success-msg">Product saved successfully!</span>';
            await loadProducts();
            setTimeout(closeProductModal, 1000);
        } else {
            msg.innerHTML = '<span class="error-msg">Error: ' + await res.text() + '</span>';
        }
    } catch(e) {
        msg.innerHTML = '<span class="error-msg">Network error.</span>';
    } finally {
        btn.disabled = false;
    }
}

async function openVariantsModal(productId, productName) {
    activeProductId = productId;
    document.getElementById('variantModalProductName').textContent = productName;
    document.getElementById('variantModal').style.display = 'block';
    resetVariantForm();
    await loadVariants();
}

function closeVariantModal() {
    document.getElementById('variantModal').style.display = 'none';
}

async function loadVariants() {
    const tbody = document.querySelector('#variantsTable tbody');
    tbody.innerHTML = '<tr><td colspan="5">Loading variants...</td></tr>';
    try {
        const res = await fetch(`/api/products/${activeProductId}/variants`);
        currentVariants = await res.json();
        renderVariantsTable();
    } catch(e) {
        tbody.innerHTML = '<tr><td colspan="5" class="error-msg">Failed to load variants.</td></tr>';
    }
}

function renderVariantsTable() {
    const tbody = document.querySelector('#variantsTable tbody');
    if (currentVariants.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" style="text-align:center;">No variants found.</td></tr>';
        return;
    }
    
    tbody.innerHTML = '';
    currentVariants.forEach(v => {
        const tr = document.createElement('tr');
        const badge = v.active ? '<span class="badge-active">ACTIVE</span>' : '<span class="badge-inactive">INACTIVE</span>';
        const actionText = v.active ? 'Deactivate' : 'Activate';
        
        tr.innerHTML = `
            <td>${v.id}</td>
            <td>${v.size}</td>
            <td>₹${v.sellingPrice}</td>
            <td>${badge}</td>
            <td>
                <button onclick="editVariant(${v.id})">Edit</button>
                <button onclick="toggleVariantStatus(${v.id}, ${!v.active})">${actionText}</button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

function resetVariantForm() {
    editVariantId = null;
    document.getElementById('variantFormTitle').textContent = 'Add Variant';
    document.getElementById('varSize').value = '';
    document.getElementById('varPrice').value = '';
    document.getElementById('varStatusGroup').style.display = 'none';
    document.getElementById('cancelVarEditBtn').style.display = 'none';
    document.getElementById('variantMessageBox').innerHTML = '';
}

function editVariant(id) {
    const v = currentVariants.find(x => x.id === id);
    editVariantId = id;
    document.getElementById('variantFormTitle').textContent = 'Edit Variant';
    document.getElementById('varSize').value = v.size;
    document.getElementById('varPrice').value = v.sellingPrice;
    document.getElementById('varActive').value = v.active ? "true" : "false";
    document.getElementById('varStatusGroup').style.display = 'block';
    document.getElementById('cancelVarEditBtn').style.display = 'inline-block';
    document.getElementById('variantMessageBox').innerHTML = '';
}

async function toggleVariantStatus(id, newStatus) {
    const v = currentVariants.find(x => x.id === id);
    const confirmMsg = newStatus ? 'Are you sure you want to activate this variant?' : 'Are you sure you want to deactivate this variant?';
    if (!confirm(confirmMsg)) return;
    
    const payload = { size: v.size, sellingPrice: v.sellingPrice, active: newStatus };
    try {
        const res = await fetch(`/api/products/${activeProductId}/variants/${id}`, {
            method: 'PUT',
            headers: {'Content-Type':'application/json'},
            body: JSON.stringify(payload)
        });
        if(res.ok) await loadVariants();
        else alert('Error: ' + await res.text());
    } catch(e) {
        alert('Network error.');
    }
}

async function saveVariant() {
    const size = document.getElementById('varSize').value.trim();
    const priceStr = document.getElementById('varPrice').value;
    const active = document.getElementById('varActive').value === 'true';
    const msg = document.getElementById('variantMessageBox');
    const btn = document.getElementById('saveVarBtn');
    
    if (!size) {
        msg.innerHTML = '<span class="error-msg">Size is required.</span>';
        return;
    }
    if (!priceStr || parseFloat(priceStr) < 0) {
        msg.innerHTML = '<span class="error-msg">Valid selling price is required.</span>';
        return;
    }
    
    btn.disabled = true;
    msg.innerHTML = 'Saving...';
    
    const payload = { size, sellingPrice: parseFloat(priceStr), active: editVariantId ? active : true };
    
    try {
        const url = editVariantId ? `/api/products/${activeProductId}/variants/${editVariantId}` : `/api/products/${activeProductId}/variants`;
        const method = editVariantId ? 'PUT' : 'POST';
        
        const res = await fetch(url, {
            method,
            headers: {'Content-Type':'application/json'},
            body: JSON.stringify(payload)
        });
        
        if (res.ok) {
            msg.innerHTML = '<span class="success-msg">Variant saved successfully!</span>';
            await loadVariants();
            setTimeout(resetVariantForm, 1000);
        } else {
            msg.innerHTML = '<span class="error-msg">Error: ' + await res.text() + '</span>';
        }
    } catch(e) {
        msg.innerHTML = '<span class="error-msg">Network error.</span>';
    } finally {
        btn.disabled = false;
    }
}

window.onclick = function(event) {
    if (event.target == document.getElementById('productModal')) closeProductModal();
    if (event.target == document.getElementById('variantModal')) closeVariantModal();
}
