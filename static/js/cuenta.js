document.addEventListener('DOMContentLoaded', function() {
   const accountIcon = document.querySelector('.account-icon');
   const loginFormContainer = document.querySelector('.login-form-container');
   const loginForm = document.querySelector('.login-form');
   const closeButton = document.querySelector('#closeButton');

   let isLoginFormVisible = false;

   // Verificar si hay un mensaje de error en el formulario
   const errorMessage = document.querySelector('.error');
   if (errorMessage) {
     loginFormContainer.style.display = 'block';
     isLoginFormVisible = true;
   }

   accountIcon.addEventListener('click', function() {
      if (!isLoginFormVisible) {
         loginFormContainer.style.display = 'block';
         isLoginFormVisible = true;
      } else {
         loginFormContainer.style.display = 'none';
         loginForm.reset();
         isLoginFormVisible = false;
      }
   });

   closeButton.addEventListener('click', function() {
      loginFormContainer.style.display = 'none';
      isLoginFormVisible = false;
   });
 });


document.addEventListener("DOMContentLoaded", function() {
   var categoriesButton = document.querySelector(".dropbtn");
   var categoriesDropdown = document.querySelector(".categories-dropdown");

   categoriesButton.addEventListener("click", function() {
      if (categoriesDropdown.style.display === "block") {
         categoriesDropdown.style.display = "none";
      } else {
         categoriesDropdown.style.display = "block";
      }
   });
});
