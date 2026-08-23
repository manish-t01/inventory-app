import os

base_dir = r"D:\Coding\github\Projects\Rohit's Work\inventory-app\src\main\resources\static"

htmls = {
    "daily-entry.html": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Daily Entry - Inventory</title>
    <link rel="stylesheet" href="css/style.css">
    <style>
        .split-view {
            display: flex;
            gap: 20px;
        }
        .image-panel {
            flex: 1;
            border: 1px solid #ccc;
            padding: 10px;
            background: #f9f9f9;
        }
        .data-panel {
            flex: 2;
        }
        #uploadedImage {
            max-width: 100%;
            display: none;
        }
    </style>
</head>
<body>
    <div class="sidebar">
        <h2>Multi-Store</h2>
        <ul>
            <li><a href="index.html">Dashboard</a></li>
            <li><a href="daily-entry.html">Daily Entry</a></li>
            <li><a href="products.html">Products</a></li>
            <li><a href="reports.html">Reports</a></li>
        </ul>
    </div>
    <div class="main-content">
        <h1>Daily Entry</h1>
        <div class="entry-header">
            <div>
                <label>Store:</label>
                <select id="storeSelect"></select>
            </div>
            <div>
                <label>Date:</label>
                <input type="date" id="recordDate">
            </div>
            <div>
                <label>Source Image:</label>
                <input type="file" id="imageUpload" accept="image/jpeg, image/png">
            </div>
        </div>
        
        <div class="split-view">
            <div class="image-panel">
                <h3>Source Image</h3>
                <img id="uploadedImage" src="" alt="Uploaded Record">
                <p id="noImageText">No image uploaded.</p>
            </div>
            
            <div class="data-panel">
                <div style="margin-bottom:10px;">
                    <label>Select Product:</label>
                    <select id="productSelect">
                        <option value="">-- Choose Product --</option>
                    </select>
                    <select id="variantSelect">
                        <option value="">-- Choose Size --</option>
                    </select>
                    <button onclick="addRowFromSelect()">Add to Entry</button>
                </div>

                <table id="entryTable">
                    <thead>
                        <tr>
                            <th>Product</th>
                            <th>Size</th>
                            <th>Opening</th>
                            <th>Received</th>
                            <th>Total</th>
                            <th>Sold</th>
                            <th>Closing</th>
                            <th>Price</th>
                            <th>Amount</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        <!-- Rows added dynamically -->
                    </tbody>
                </table>
                <br>
                <button onclick="saveRecord()" class="btn-primary">Save Record</button>
                <div id="saveMessage" style="margin-top:10px; color: green; font-weight: bold;"></div>
            </div>
        </div>
    </div>
    <script src="js/app.js"></script>
    <script src="js/daily-entry.js"></script>
</body>
</html>
""",
    "css/style.css": """body {
    font-family: Arial, sans-serif;
    margin: 0;
    display: flex;
    background-color: #f4f7f6;
}

.sidebar {
    width: 200px;
    background-color: #2c3e50;
    color: white;
    height: 100vh;
    padding: 20px;
    box-shadow: 2px 0 5px rgba(0,0,0,0.1);
}

.sidebar h2 { margin-top: 0; }

.sidebar ul {
    list-style: none;
    padding: 0;
}

.sidebar ul li {
    margin-bottom: 15px;
}

.sidebar ul li a {
    color: #ecf0f1;
    text-decoration: none;
    font-size: 16px;
}

.sidebar ul li a:hover {
    text-decoration: underline;
}

.main-content {
    flex-grow: 1;
    padding: 20px;
}

.cards {
    display: flex;
    gap: 20px;
}

.card {
    background: white;
    padding: 20px;
    border-radius: 8px;
    width: 150px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    text-align: center;
}

.card h3 {
    margin: 0 0 10px 0;
    color: #7f8c8d;
    font-size: 14px;
}

.card p {
    margin: 0;
    font-size: 24px;
    font-weight: bold;
    color: #2c3e50;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 10px;
    background: white;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

table, th, td {
    border: 1px solid #ddd;
}

th, td {
    padding: 10px;
    text-align: left;
}

th { background-color: #f8f9fa; }

.entry-header {
    display: flex;
    gap: 20px;
    margin-bottom: 20px;
    background: white;
    padding: 15px;
    border-radius: 8px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

input[type="number"] {
    width: 70px;
    padding: 5px;
}

button {
    padding: 8px 12px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    background-color: #95a5a6;
    color: white;
}
button:hover { background-color: #7f8c8d; }

.btn-primary {
    background-color: #3498db;
    font-size: 16px;
    padding: 10px 20px;
}
.btn-primary:hover { background-color: #2980b9; }

.error { color: red; }
""",
    "js/daily-entry.js": """let allProducts = [];
let allVariants = {};

document.addEventListener('DOMContentLoaded', async () => {
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
    allProducts.forEach(p => {
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
            variants.forEach(v => {
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
});

let rowIndex = 0;

function addRowFromSelect() {
    const variantSelect = document.getElementById('variantSelect');
    const selectedOption = variantSelect.options[variantSelect.selectedIndex];
    
    if (!selectedOption.value) {
        alert("Please select a product and size.");
        return;
    }
    
    const variantId = selectedOption.value;
    const productName = selectedOption.dataset.productName;
    const size = selectedOption.dataset.size;
    const price = selectedOption.dataset.price;
    
    const tbody = document.querySelector('#entryTable tbody');
    const tr = document.createElement('tr');
    tr.id = `row-${rowIndex}`;
    tr.dataset.variantId = variantId;
    
    tr.innerHTML = `
        <td>${productName}</td>
        <td>${size}</td>
        <td><input type="number" class="opening" value="0" min="0" oninput="calculateRow(${rowIndex})"></td>
        <td><input type="number" class="received" value="0" min="0" oninput="calculateRow(${rowIndex})"></td>
        <td class="total">0</td>
        <td><input type="number" class="sold" value="0" min="0" oninput="calculateRow(${rowIndex})"></td>
        <td class="closing">0</td>
        <td><input type="number" class="price" value="${price}" min="0" oninput="calculateRow(${rowIndex})"></td>
        <td class="amount">0</td>
        <td><button onclick="removeRow(${rowIndex})">Delete</button></td>
    `;
    
    tbody.appendChild(tr);
    
    // Automatically focus on opening stock
    tr.querySelector('.opening').focus();
    
    rowIndex++;
}

function removeRow(id) {
    document.getElementById(`row-${id}`).remove();
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
    const msgEl = document.getElementById('saveMessage');
    
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
        
        if(opening < 0 || received < 0 || sold < 0 || price < 0) {
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
        msgEl.textContent = "Negative values are not allowed.";
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

    try {
        const response = await fetch('/api/daily-records', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (response.ok) {
            msgEl.textContent = "Record saved successfully!";
            msgEl.style.color = "green";
            // Clear table
            document.querySelector('#entryTable tbody').innerHTML = '';
            rowIndex = 0;
        } else {
            const err = await response.text();
            msgEl.textContent = "Error: " + err;
            msgEl.style.color = "red";
        }
    } catch (error) {
        msgEl.textContent = "Network Error.";
        msgEl.style.color = "red";
    }
}
"""
}

for name, content in htmls.items():
    with open(os.path.join(base_dir, name), "w", encoding="utf-8") as f:
        f.write(content)

print("Frontend Part 2 generated successfully.")
