var cart_data = [];

const cartIcon = document.getElementById('cart-icon');
const cart = document.getElementById('sidecartid');
const closeBtn = document.getElementById('close-btn');
const continueBtn = document.getElementById('continue');
const animation = document.querySelector('.animation');
const cartItems = document.querySelector('.cart-items');
const itemsNum = document.getElementById('items-number');
const subtotalPrice = document.getElementById('subtotal-price');

continueBtn.addEventListener('click', closeCart);
cartIcon.addEventListener('click', openCart);
closeBtn.addEventListener('click', closeCart);

document.addEventListener('DOMContentLoaded', function() {
    loadCartFromLocalStorage();
  });

function openCart() {
    cart.classList.add('open');
    animation.style.display = 'block';

    setTimeout(() => {
        animation.classList.add('show');
    }, 0)
}

function closeCart() {
    cart.classList.remove('open');
    animation.classList.remove('show');

    setTimeout(() => {
        animation.style.display = 'none';
    }, 500)
}

function loadCartFromLocalStorage() {
    const cartData = localStorage.getItem('cartData');
    if (cartData) {
        cart_data = JSON.parse(cartData);
        updateCart(); // Actualizar el carrito después de cargar los datos
    }
}

function removeItem(itemId) {
    // Encuentra el índice del elemento en la lista
    const index = cart_data.findIndex(item => item[0] === itemId);

    if (index !== -1) {
        cart_data.splice(index, 1); // Eliminar el elemento del arreglo cart_data
        updateCart(); // Actualizar el carrito después de eliminar el elemento
    }
}

function increaseQty(itemId) {
    // encuentra el item en la lista
    const item = cart_data.find(item => item[0] === itemId);

    if (item && item[7] < item[2]) {
        item[7]++; // Incrementar la cantidad del elemento
        updateCart(); // Actualizar el carrito después de aumentar la cantidad
    }
}

// Decrementar cantidad
function decreaseQty(itemId) {
    // encuentra el item en la lista
    const item = cart_data.find(item => item[0] === itemId);

    if (item && item[7] > 1) {
        item[7]--; // Incrementar la cantidad del elemento
        updateCart(); // Actualizar el carrito después de aumentar la cantidad
    }
}

//Calcular número de items
function calcItemsNum() {
    let itemsCount = 0

    cart_data.forEach((item) => (itemsCount += item[7]))

    itemsNum.innerHTML = itemsCount
}

//Calcular precio subtotal
function subtotalCount() {
    let subtotal = 0

    cart_data.forEach((item) => (subtotal += item[3] * item[7]))

    subtotalPrice.innerHTML = subtotal
}

function saveCartToLocalStorage() {
    localStorage.setItem('cartData', JSON.stringify(cart_data));
    }

// Render items del carro
function renderCartItems() {
    // Borrar el contenido
    cartItems.innerHTML = '';
    // Renderizar según la lista
    cart_data.forEach(item => {
        const cartItem = document.createElement('div');
        cartItem.classList.add('cart-item');
        cartItem.innerHTML = `
            <div class="remove-item" onclick="removeItem(${item[0]})">
                <span>&times;</span>
            </div>
            <div class="item-img">
                <img src="${item[6]}" alt="">
            </div>
            <div class="item-details">
                <p>${item[1]}</p>
                <strong>C$${item[3]}</strong>
                <div class="qty">
                    <span onclick="decreaseQty(${item[0]})">-</span>
                    <strong>${item[7]}</strong>
                    <span onclick="increaseQty(${item[0]})">+</span>
                </div>
            </div>
        `;
        cartItems.appendChild(cartItem);
    });
}


// Actualizar render carrito
function updateCart() {
    // Rerender con datos actualizados
    renderCartItems();
    // Actualizar número
    calcItemsNum();
    // Actualizar subtitak
    subtotalCount();
    // Guardar carrito en las cookies
    saveCartToLocalStorage()
}



