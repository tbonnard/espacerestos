document.addEventListener("DOMContentLoaded", function () {

  let distribDetailsMenu = document.querySelector('#distrib_details_menu');
  let distribBenevolesMenu = document.querySelector('#distrib_benevoles_menu');

  let distribDetails = document.querySelector('.distrib_global');
  let distribBenevoles = document.querySelector('#distrib_benevoles');

  distribDetails.style.display = 'none';

  distribDetailsMenu.addEventListener('click', () => {
    distribDetails.style.display = 'block';
    distribBenevoles.style.display = 'none';
  })

  distribBenevolesMenu.addEventListener('click', () => {
    distribDetails.style.display = 'none';
    distribBenevoles.style.display = 'block';
  })



});
