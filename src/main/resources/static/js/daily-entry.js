let allProducts = [];
let allVariants = {};
let editId = null;

document.addEventListener('DOMContentLoaded', async () => {
    // Check for Edit Mode
    const urlParams = new URLSearchParams(window.location.search);
    editId = urlParams.get('editId');
    
    if (editId) {
        document.getElementById('pageTitle').textContent = "Edit Daily Record";
    }
    
    // 1. Load Stores
    const storeSelect = document.getElementById('storeSelect');
    const stores = await fetchStores();
    stores.forEach(store => {
        const option = document.createElement('option');
        option.value = store.id;
        option.textContent = store.name;
        storeSelect.appendChild(option);
    });

    document.getElementById('recordDate').valueAsDate = new Date();
    
    // 2. Image upload preview
    const imageUpload = document.getElementById('imageUpload');
    imageUpload.addEventListener('change', function(e) {
        if(e.target.files && e.target.files[0]) {
            const reader = new FileReader();
            reader.onload = function(evt) {
                document.getElementById('uploadedImage').src = evt.target.result;
                document.getElementById('uploadedImage').style.display = 'block';
                document.getElementById('noImageText').style.display = 'none';
            }
            reader.readAsDataURL(e.target.files[0]);
        }
    });

    // 3. Load Products for dropdown
    allProducts = await fetchProducts();
    const productSelect = document.getElementById('productSelect');
    allProducts.filter(p => p.active !== false).forEach(p => {
        const opt = document.createElement('option');
        opt.value = p.id;
        opt.textContent = p.name;
        productSelect.appendChild(opt);
    });

    // 4. Handle Product Selection change to load sizes
    productSelect.addEventListener('change', async (e) => {
        const productId = e.target.value;
        const variantSelect = document.getElementById('variantSelect');
        variantSelect.innerHTML = '<option value="">-- Choose Size --</option>';
        if (productId) {
            const res = await fetch(`/api/products/${productId}/variants`);
            const variants = await res.json();
            allVariants[productId] = variants;
            variants.filter(v => v.active !== false).forEach(v => {
                const opt = document.createElement('option');
                opt.value = v.id;
                opt.textContent = v.size + ' (₹' + v.sellingPrice + ')';
                opt.dataset.price = v.sellingPrice;
                opt.dataset.productName = allProducts.find(p => p.id == productId).name;
                opt.dataset.size = v.size;
                variantSelect.appendChild(opt);
            });
        }
    });
    
    if (editId) {
        await loadExistingRecord(editId);
    }
});

let rowIndex = 0;

async function loadExistingRecord(id) {
    try {
        const res = await fetch(`/api/daily-records/${id}`);
        if(!res.ok) throw new Error("Failed to load record");
        const record = await res.json();
        
        document.getElementById('storeSelect').value = record.storeId;
        document.getElementById('recordDate').value = record.recordDate;
        
        if (record.sourceImagePath) {
            document.getElementById('uploadedImage').src = '/' + record.sourceImagePath;
            document.getElementById('uploadedImage').style.display = 'block';
            document.getElementById('noImageText').style.display = 'none';
        }

        const tbody = document.querySelector('#entryTable tbody');
        for (const item of record.items) {
            let pName = "Unknown";
            let sName = "Unknown";
            
            // Try to find names from pre-loaded products (hacky for MVP but works)
            for(const p of allProducts) {
                const vRes = await fetch(`/api/products/${p.id}/variants`);
                const vs = await vRes.json();
                const found = vs.find(v => v.id === item.productVariantId);
                if(found) {
                    pName = p.name;
                    sName = found.size;
                    break;
                }
            }

            const tr = document.createElement('tr');
            tr.id = `row-${rowIndex}`;
            tr.dataset.variantId = item.productVariantId;
            tr.dataset.suggestedOpening = item.openingStock;
            
            tr.innerHTML = `
                <td>${pName}</td>
                <td>${sName}</td>
                <td>
                    <input type="number" class="opening" value="${item.openingStock}" min="0" oninput="calculateRow(${rowIndex}); checkOpening(${rowIndex});">
                    <span class="warning-icon" style="color:orange;display:none;" title="Differs from previous closing">⚠</span>
                </td>
                <td><input type="number" class="received" value="${item.stockReceived}" min="0" oninput="calculateRow(${rowIndex})"></td>
                <td class="total">0</td>
                <td><input type="number" class="sold" value="${item.soldQuantity}" min="0" oninput="calculateRow(${rowIndex})"></td>
                <td class="closing">0</td>
                <td><input type="number" class="price" value="${item.sellingPrice}" min="0" oninput="calculateRow(${rowIndex})"></td>
                <td class="amount">0</td>
                <td><button onclick="removeRow(${rowIndex})">Delete</button></td>
            `;
            tbody.appendChild(tr);
            calculateRow(rowIndex);
            rowIndex++;
        }
    } catch(e) {
        console.error(e);
        alert("Error loading record for editing");
    }
}

async function addRowFromSelect() {
    const variantSelect = document.getElementById('variantSelect');
    const storeSelect = document.getElementById('storeSelect');
    const recordDate = document.getElementById('recordDate').value;
    const selectedOption = variantSelect.options[variantSelect.selectedIndex];
    
    if (!selectedOption.value || !storeSelect.value || !recordDate) {
        alert("Please select Store, Date, Product and Size.");
        return;
    }
    
    const variantId = selectedOption.value;
    const productName = selectedOption.dataset.productName;
    const size = selectedOption.dataset.size;
    const price = selectedOption.dataset.price;
    const storeId = storeSelect.value;
    
    // Fetch suggested opening stock
    let suggestedOpening = 0;
    try {
        const res = await fetch(`/api/daily-records/suggest-opening?storeId=${storeId}&variantId=${variantId}&date=${recordDate}`);
        if(res.ok) {
            suggestedOpening = await res.json();
        }
    } catch(e) {
        console.error("Error fetching opening stock", e);
    }
    
    const tbody = document.querySelector('#entryTable tbody');
    const tr = document.createElement('tr');
    tr.id = `row-${rowIndex}`;
    tr.dataset.variantId = variantId;
    tr.dataset.suggestedOpening = suggestedOpening;
    
    tr.innerHTML = `
        <td>${productName}</td>
        <td>${size}</td>
        <td>
            <input type="number" class="opening" value="${suggestedOpening}" min="0" oninput="calculateRow(${rowIndex}); checkOpening(${rowIndex});">
            <span class="warning-icon" style="color:orange;display:none;" title="Differs from previous closing">⚠</span>
        </td>
        <td><input type="number" class="received" value="0" min="0" oninput="calculateRow(${rowIndex})"></td>
        <td class="total">${suggestedOpening}</td>
        <td><input type="number" class="sold" value="0" min="0" oninput="calculateRow(${rowIndex})"></td>
        <td class="closing">${suggestedOpening}</td>
        <td><input type="number" class="price" value="${price}" min="0" oninput="calculateRow(${rowIndex})"></td>
        <td class="amount">0</td>
        <td><button onclick="removeRow(${rowIndex})">Delete</button></td>
    `;
    
    tbody.appendChild(tr);
    tr.querySelector('.opening').focus();
    rowIndex++;
}

function removeRow(id) {
    document.getElementById(`row-${id}`).remove();
}

function checkOpening(id) {
    const row = document.getElementById(`row-${id}`);
    const opening = parseFloat(row.querySelector('.opening').value) || 0;
    const suggested = parseFloat(row.dataset.suggestedOpening) || 0;
    const warnIcon = row.querySelector('.warning-icon');
    
    if (opening !== suggested) {
        warnIcon.style.display = 'inline';
    } else {
        warnIcon.style.display = 'none';
    }
}

function calculateRow(id) {
    const row = document.getElementById(`row-${id}`);
    const opening = parseFloat(row.querySelector('.opening').value) || 0;
    const received = parseFloat(row.querySelector('.received').value) || 0;
    const sold = parseFloat(row.querySelector('.sold').value) || 0;
    const price = parseFloat(row.querySelector('.price').value) || 0;
    
    const total = opening + received;
    const closing = total - sold;
    const amount = sold * price;
    
    row.querySelector('.total').textContent = total;
    
    const closingEl = row.querySelector('.closing');
    closingEl.textContent = closing;
    if (closing < 0) {
        closingEl.style.color = 'red';
        closingEl.style.fontWeight = 'bold';
    } else {
        closingEl.style.color = 'black';
        closingEl.style.fontWeight = 'normal';
    }
    
    row.querySelector('.amount').textContent = amount;
}

async function saveRecord() {
    const storeId = document.getElementById('storeSelect').value;
    const recordDate = document.getElementById('recordDate').value;
    const imageUpload = document.getElementById('imageUpload');
    const msgEl = document.getElementById('saveMessage');
    const saveBtn = document.getElementById('saveBtn');
    
    if (!storeId || !recordDate) {
        msgEl.textContent = "Please select Store and Date.";
        msgEl.className = "error";
        return;
    }

    const items = [];
    const rows = document.querySelectorAll('#entryTable tbody tr');
    
    if (rows.length === 0) {
        msgEl.textContent = "Please add at least one product to the entry.";
        msgEl.className = "error";
        return;
    }
    
    let hasError = false;
    
    rows.forEach(row => {
        const variantId = row.dataset.variantId;
        const opening = parseInt(row.querySelector('.opening').value) || 0;
        const received = parseInt(row.querySelector('.received').value) || 0;
        const sold = parseInt(row.querySelector('.sold').value) || 0;
        const price = parseFloat(row.querySelector('.price').value) || 0;
        const total = opening + received;
        
        if(opening < 0 || received < 0 || sold < 0 || price < 0 || sold > total) {
            hasError = true;
        }
        
        items.push({
            productVariantId: parseInt(variantId),
            openingStock: opening,
            stockReceived: received,
            soldQuantity: sold,
            sellingPrice: price
        });
    });

    if (hasError) {
        msgEl.textContent = "Invalid values found (negative numbers or sold > total).";
        msgEl.className = "error";
        return;
    }

    const payload = {
        storeId: parseInt(storeId),
        recordDate: recordDate,
        notes: "",
        items: items
    };

    msgEl.textContent = "Saving...";
    msgEl.className = "";
    saveBtn.disabled = true;

    try {
        let response;
        if (editId) {
            response = await fetch(`/api/daily-records/${editId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
        } else {
            response = await fetch('/api/daily-records', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
        }

        if (response.ok) {
            const savedRecord = await response.json();
            
            // Now upload image if present
            if(imageUpload.files && imageUpload.files[0]) {
                const formData = new FormData();
                formData.append("file", imageUpload.files[0]);
                
                await fetch(`/api/daily-records/${savedRecord.id}/image`, {
                    method: 'POST',
                    body: formData
                });
            }
            
            msgEl.textContent = "Record and Image saved successfully!";
            msgEl.style.color = "green";
            
            if(!editId) {
                // Clear table only if new
                document.querySelector('#entryTable tbody').innerHTML = '';
                rowIndex = 0;
                document.getElementById('uploadedImage').style.display = 'none';
                document.getElementById('noImageText').style.display = 'block';
                imageUpload.value = "";
            } else {
                setTimeout(() => { window.location.href = 'daily-records.html'; }, 1000);
            }
        } else {
            const err = await response.text();
            msgEl.textContent = "Error: " + err;
            msgEl.style.color = "red";
        }
    } catch (error) {
        msgEl.textContent = "Network Error.";
        msgEl.style.color = "red";
    } finally {
        saveBtn.disabled = false;
    }
}
