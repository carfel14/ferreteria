const nuevoCampo = 7;
const valorNuevo = 1;

for (let entrada in product_list) {
    product_list[entrada][nuevoCampo] = valorNuevo;
}

addItemListener();

// Agregar items al carro
function addItemListener() {
    const elementosGenerados = document.getElementsByClassName('btn-add-to-cart');

    for (var i = 0; i < elementosGenerados.length; i++) {
        (function(index) {
            elementosGenerados[index].onclick = function() {
                // Agregar
                addItem(index);
            };
        })(i);
    }
}

function addItem(index) {
    const selectedItem = product_list[index];
    const existingItem = cart_data.find(item => item[0] === selectedItem[0]);

    if (existingItem) {
        // Si el producto ya existe, incrementar la cantidad
        existingItem[7]++;
    } else {
        cart_data.push(product_list[index]);
    }

    updateCart();
    openCart();
}


function saveCartToLocalStorage() {
    localStorage.setItem('cartData', JSON.stringify(cart_data));
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

