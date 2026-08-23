// Common JavaScript functions
function formatDate(dateString) {
    if (!dateString) return dateString;
    const parts = dateString.split('-');
    if (parts.length === 3 && parts[0].length === 4) {
        return `${parts[2]}-${parts[1]}-${parts[0]}`;
    }
    return dateString;
}

async function fetchStores() {
    const res = await fetch('/api/stores');
    return await res.json();
}

async function fetchProducts() {
    const res = await fetch('/api/products');
    return await res.json();
}
