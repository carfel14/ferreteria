$(document).ready(function() {
  $(".product-image-container").mouseenter(function() {
    $(".zoom-image-container").fadeIn(300);
  });

  $(".product-image-container").mouseleave(function() {
    $(".zoom-image-container").fadeOut(300);
  });

  $(".product-image-container").mousemove(function(e) {
    var containerWidth = $(this).width();
    var containerHeight = $(this).height();
    var x = e.pageX - $(this).offset().left;
    var y = e.pageY - $(this).offset().top;

    var zoomFactor = 2; // Factor de aumento de zoom

    var imageWidth = $(this).find("img").width();
    var imageHeight = $(this).find("img").height();

    var posX = -((x / containerWidth) * (imageWidth * zoomFactor) - $(".zoom-image-container").width() / 2);
    var posY = -((y / containerHeight) * (imageHeight * zoomFactor) - $(".zoom-image-container").height() / 2);

    // Comprobar si el mouse está en las esquinas del contenedor
    if (x <= 0 || x >= containerWidth || y <= 0 || y >= containerHeight) {
      $(".zoom-image-container").hide();
    } else {
      $(".zoom-image-container").show();
      $(".zoom-image-container img").css({
        top: posY + "px",
        left: posX + "px",
        transform: "scale(" + zoomFactor + ")"
      });
    }
  });
});

  // Obtener los elementos del DOM
const decreaseButton = document.querySelector('.quantity-decrease');
const increaseButton = document.querySelector('.quantity-increase');
const quantityInput = document.querySelector('.quantity-input');

// Agregar un evento al botón de decremento
decreaseButton.addEventListener('click', function() {
  if (quantityInput.value > 1) {
    quantityInput.value--;
  }
});

// Agregar un evento al botón de incremento
increaseButton.addEventListener('click', function() {
  quantityInput.value++;
});
