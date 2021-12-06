document.addEventListener("DOMContentLoaded", function () {

if (document.querySelectorAll('.sub_nav_hor')) {

  let subMenus = document.querySelectorAll('.sub_nav_hor');

  subMenus.forEach( i => {
    i.addEventListener('click', () => {
      currentActive = document.querySelectorAll('.sub_nav_hor.active');
      i.className += " active";
      currentActive[0].className = "sub_nav_hor";
    })
  })
}


});
