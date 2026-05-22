document.addEventListener('DOMContentLoaded', () => {
    loadProducts();

    document.getElementById('productForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const data = {
            sku: document.getElementById('sku').value,
            name: document.getElementById('name').value,
            price: document.getElementById('price').value,
            stock: document.getElementById('stock').value
        };

        try {
            const res = await fetch('/api/products', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            const result = await res.json();
            
            if (res.ok) {
                showAlert(result.message, 'success');
                document.getElementById('productForm').reset();
                loadProducts();
            } else {
                showAlert(result.error, 'error');
            }
        } catch (err) {
            showAlert('Network error occurred.', 'error');
        }
    });

    document.getElementById('saleForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const data = {
            product_id: document.getElementById('saleProduct').value,
            quantity: document.getElementById('saleQty').value
        };

        try {
            const res = await fetch('/api/sales', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            const result = await res.json();
            
            if (res.ok) {
                showAlert(result.message, 'success');
                document.getElementById('saleForm').reset();
                loadProducts();
            } else {
                showAlert(result.error, 'error');
            }
        } catch (err) {
            showAlert('Network error occurred.', 'error');
        }
    });
});

async function loadProducts() {
    try {
        const res = await fetch('/api/products', {
            headers: {
                'Accept-Language': 'es' // Try to get messages in Spanish if any API error happens during fetch, though this is GET
            }
        });
        const products = await res.json();
        
        const tbody = document.querySelector('#productsTable tbody');
        const select = document.getElementById('saleProduct');
        
        tbody.innerHTML = '';
        
        // Keep the first option
        const firstOption = select.options[0];
        select.innerHTML = '';
        select.appendChild(firstOption);

        products.forEach(p => {
            // Add to table
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${p.id}</td>
                <td>${p.sku}</td>
                <td>${p.name}</td>
                <td>$${p.price.toFixed(2)}</td>
                <td>${p.stock}</td>
            `;
            tbody.appendChild(tr);

            // Add to select
            const option = document.createElement('option');
            option.value = p.id;
            option.textContent = `${p.name} (Stock: ${p.stock})`;
            select.appendChild(option);
        });
    } catch (err) {
        console.error("Failed to load products", err);
    }
}

function showAlert(message, type) {
    const alertDiv = document.getElementById('alertMessage');
    alertDiv.textContent = message;
    alertDiv.className = `alert alert-${type}`;
    alertDiv.style.display = 'block';
    setTimeout(() => {
        alertDiv.style.display = 'none';
    }, 5000);
}
