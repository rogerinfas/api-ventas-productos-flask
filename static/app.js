let token = localStorage.getItem('jwt_token');

function checkAuth() {
    if (!token) {
        window.location.href = '/login';
    } else {
        loadProducts();
    }
}

document.addEventListener('DOMContentLoaded', () => {
    checkAuth();

    document.getElementById('logoutBtn')?.addEventListener('click', () => {
        token = null;
        localStorage.removeItem('jwt_token');
        window.location.href = '/login';
    });

    document.getElementById('productForm')?.addEventListener('submit', async (e) => {
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
                headers: { 
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
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
                headers: { 
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
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
                'Accept-Language': 'es', // Intentar obtener mensajes en español en caso de error de la API
                'Authorization': `Bearer ${token}`
            }
        });
        if (res.status === 401 || res.status === 422) {
            token = null;
            localStorage.removeItem('jwt_token');
            window.location.href = '/login';
            throw new Error('Unauthorized');
        }
        if (!res.ok) {
            throw new Error(`HTTP error! status: ${res.status}`);
        }
        const products = await res.json();
        
        const tbody = document.querySelector('#productsTable tbody');
        const select = document.getElementById('saleProduct');
        
        tbody.innerHTML = '';
        
        // Mantener la primera opción
        const firstOption = select.options[0];
        select.innerHTML = '';
        select.appendChild(firstOption);

        products.forEach(p => {
            // Agregar a la tabla
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${p.id}</td>
                <td>${p.sku}</td>
                <td>${p.name}</td>
                <td>$${p.price.toFixed(2)}</td>
                <td>${p.stock}</td>
            `;
            tbody.appendChild(tr);

            // Agregar al selector
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
