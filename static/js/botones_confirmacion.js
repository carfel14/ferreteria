// Obtener todos los contenedores de cantidad
const cantidadContainers = document.querySelectorAll('.cantidad-container');

// Recorrer cada contenedor y agregar los event listeners
cantidadContainers.forEach(cantidadContainer => {
  const btnAumentar = cantidadContainer.querySelector('.aumentar');
  const btnDisminuir = cantidadContainer.querySelector('.disminuir');
  const inputCantidad = cantidadContainer.querySelector('.input-cantidad');

  btnAumentar.addEventListener('click', () => {
    // Obtener el valor actual y convertirlo a número
    let cantidad = parseInt(inputCantidad.value);

    // Incrementar la cantidad
    cantidad++;

    // Actualizar el valor del input
    inputCantidad.value = cantidad;
  });

  btnDisminuir.addEventListener('click', () => {
    // Obtener el valor actual y convertirlo a número
    let cantidad = parseInt(inputCantidad.value);

    // Verificar que la cantidad no sea menor a 1
    if (cantidad > 1) {
      // Disminuir la cantidad
      cantidad--;

      // Actualizar el valor del input
      inputCantidad.value = cantidad;
    }
  });
});