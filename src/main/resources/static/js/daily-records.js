let deleteRecordId = null;

document.addEventListener('DOMContentLoaded', async () => {
    await loadDailyRecords();
});

async function loadDailyRecords() {
    const tbody = document.querySelector('#recordsTable tbody');
    tbody.innerHTML = ''; // clear existing
    try {
        const res = await fetch('/api/daily-records');
        const records = await res.json();
        records.sort((a,b) => new Date(b.recordDate) - new Date(a.recordDate));
        records.forEach(r => {
            const tr = document.createElement('tr');
            tr.id = `record-row-${r.id}`;
            tr.innerHTML = `
                <td>${r.id}</td>
                <td>${formatDate(r.recordDate)}</td>
                <td>${r.store.name}</td>
                <td>Locked</td>
                <td>
                    <button class="btn-primary" onclick="window.location.href='daily-entry.html?editId=${r.id}'">Edit</button>
                    <button class="btn-secondary" onclick="printRecord(${r.id})">Print Record</button>
                    <button class="btn-danger" onclick="confirmDeleteRecord(${r.id}, '${formatDate(r.recordDate)}', '${r.store.name.replace(/'/g, "\\'")}')">Delete</button>
                </td>
            `;
            tbody.appendChild(tr);
        });
    } catch(e) {
        console.error("Failed to load records", e);
    }
}

function printRecord(recordId) {
    window.open(`daily-record-print.html?id=${recordId}`, '_blank');
}

function confirmDeleteRecord(recordId, date, storeName) {
    deleteRecordId = recordId;
    const modalText = document.getElementById('deleteModalText');
    modalText.innerHTML = `This action will delete the Daily Record for <strong>${date}</strong> from <strong>${storeName}</strong>.<br><br>It will also delete all products, images, inventory transactions, and sales data associated with this record.<br><br>This action cannot be undone.`;
    
    const modal = document.getElementById('deleteModal');
    modal.hidden = false;
    modal.style.display = 'flex';
}

function closeDeleteModal() {
    deleteRecordId = null;
    const modal = document.getElementById('deleteModal');
    modal.hidden = true;
    modal.style.display = 'none';
}

window.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        const modal = document.getElementById('deleteModal');
        if (modal && !modal.hidden) {
            closeDeleteModal();
        }
    }
});

async function executeDeleteRecord() {
    if (!deleteRecordId) return;
    
    const confirmBtn = document.getElementById('confirmDeleteBtn');
    confirmBtn.disabled = true;
    confirmBtn.textContent = 'Deleting...';
    
    try {
        const res = await fetch(`/api/daily-records/${deleteRecordId}`, {
            method: 'DELETE'
        });
        
        if (res.ok) {
            const row = document.getElementById(`record-row-${deleteRecordId}`);
            if (row) row.remove();
            
            closeDeleteModal();
            alert("Daily record deleted successfully.");
        } else {
            const data = await res.json();
            alert(data.message || "Unable to delete the daily record. Please try again.");
            console.error("Delete failed:", data);
        }
    } catch (e) {
        alert("Network failure or Server error. Unable to delete the daily record. Please try again.");
        console.error("Error executing delete:", e);
    } finally {
        confirmBtn.disabled = false;
        confirmBtn.textContent = 'Delete Record';
        closeDeleteModal();
    }
}
