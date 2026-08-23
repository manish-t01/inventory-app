import os

base_dir = r"D:\Coding\github\Projects\Rohit's Work\inventory-app\src\main\resources\static"

os.makedirs(os.path.join(base_dir, "css"), exist_ok=True)
os.makedirs(os.path.join(base_dir, "js"), exist_ok=True)

htmls = {
    "index.html": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Inventory Dashboard</title>
    <link rel="stylesheet" href="css/style.css">
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
        <h1>Dashboard</h1>
        <div class="cards">
            <div class="card">
                <h3>Total Sales</h3>
                <p id="totalSales">0</p>
            </div>
            <div class="card">
                <h3>Units Sold</h3>
                <p id="unitsSold">0</p>
            </div>
        </div>
    </div>
    <script src="js/app.js"></script>
</body>
</html>
""",
    "daily-entry.html": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Daily Entry</title>
    <link rel="stylesheet" href="css/style.css">
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
        
        <button onclick="addRow()">Add Row</button>
        <button onclick="saveRecord()">Save Record</button>
    </div>
    <script src="js/app.js"></script>
    <script src="js/daily-entry.js"></script>
</body>
</html>
""",
    "products.html": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Products</title>
    <link rel="stylesheet" href="css/style.css">
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
        <h1>Products</h1>
        <!-- Product management UI goes here -->
    </div>
    <script src="js/app.js"></script>
</body>
</html>
""",
    "reports.html": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Reports</title>
    <link rel="stylesheet" href="css/style.css">
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
        <h1>Reports</h1>
        <!-- Reports UI goes here -->
    </div>
    <script src="js/app.js"></script>
</body>
</html>
""",
    "css/style.css": """body {
    font-family: Arial, sans-serif;
    margin: 0;
    display: flex;
}

.sidebar {
    width: 200px;
    background-color: #2c3e50;
    color: white;
    height: 100vh;
    padding: 20px;
}

.sidebar ul {
    list-style: none;
    padding: 0;
}

.sidebar ul li {
    margin-bottom: 15px;
}

.sidebar ul li a {
    color: white;
    text-decoration: none;
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
    background: #ecf0f1;
    padding: 20px;
    border-radius: 5px;
    width: 150px;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
    margin-bottom: 20px;
}

table, th, td {
    border: 1px solid #bdc3c7;
}

th, td {
    padding: 10px;
    text-align: left;
}

.entry-header {
    display: flex;
    gap: 20px;
    margin-bottom: 20px;
}

input[type="number"] {
    width: 60px;
}
""",
    "js/app.js": """// Common JavaScript functions
async function fetchStores() {
    const res = await fetch('/api/stores');
    return await res.json();
}

async function fetchProducts() {
    const res = await fetch('/api/products');
    return await res.json();
}
""",
    "js/daily-entry.js": """document.addEventListener('DOMContentLoaded', async () => {
    const storeSelect = document.getElementById('storeSelect');
    const stores = await fetchStores();
    stores.forEach(store => {
        const option = document.createElement('option');
        option.value = store.id;
        option.textContent = store.name;
        storeSelect.appendChild(option);
    });

    document.getElementById('recordDate').valueAsDate = new Date();
    addRow();
});

let rowIndex = 0;

function addRow() {
    const tbody = document.querySelector('#entryTable tbody');
    const tr = document.createElement('tr');
    tr.id = `row-${rowIndex}`;
    
    tr.innerHTML = `
        <td><input type="text" placeholder="Product"></td>
        <td><input type="text" placeholder="Size"></td>
        <td><input type="number" class="opening" value="0" oninput="calculateRow(${rowIndex})"></td>
        <td><input type="number" class="received" value="0" oninput="calculateRow(${rowIndex})"></td>
        <td class="total">0</td>
        <td><input type="number" class="sold" value="0" oninput="calculateRow(${rowIndex})"></td>
        <td class="closing">0</td>
        <td><input type="number" class="price" value="0" oninput="calculateRow(${rowIndex})"></td>
        <td class="amount">0</td>
        <td><button onclick="removeRow(${rowIndex})">Delete</button></td>
    `;
    
    tbody.appendChild(tr);
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
    row.querySelector('.closing').textContent = closing;
    row.querySelector('.amount').textContent = amount;
}

async function saveRecord() {
    const storeId = document.getElementById('storeSelect').value;
    const recordDate = document.getElementById('recordDate').value;
    
    const items = [];
    const rows = document.querySelectorAll('#entryTable tbody tr');
    // Note: For a real app, productVariantId needs to be fetched from a dropdown. 
    // This is a simplified version just to show the UI workflow.
    
    alert('Saving functionality to be fully connected to backend variant IDs.');
}
"""
}

for name, content in htmls.items():
    with open(os.path.join(base_dir, name), "w", encoding="utf-8") as f:
        f.write(content)

print("Frontend files created successfully.")
