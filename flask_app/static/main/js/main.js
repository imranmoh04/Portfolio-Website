document.addEventListener('DOMContentLoaded', function () {
   console.log("JavaScript Loaded!"); // debugging

   const menuIcon = document.querySelector('.menu-icon'); 
   const navLinks = document.querySelector('.nav-links'); 

   if (!menuIcon || !navLinks) {
       console.error("Menu icon or navigation links not found! Check your HTML.");
       return;
   }

   menuIcon.addEventListener('click', function () {
       console.log("Menu clicked!"); // debugging 
       navLinks.classList.toggle('show'); 
   });
});