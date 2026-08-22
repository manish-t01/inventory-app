// Common JavaScript functions
async function fetchStores() {
    const res = await fetch('/api/stores');
    return await res.json();
}

async function fetchProducts() {
    const res = await fetch('/api/products');
    return await res.json();
}
