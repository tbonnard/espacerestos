document.addEventListener("DOMContentLoaded", function () {

  let subMenus = document.querySelectorAll('.sub_nav_hor');

  subMenus.forEach( i => {
    i.addEventListener('click', () => {
      currentActive = document.querySelectorAll('.sub_nav_hor.active');
      i.className += " active";
      currentActive[0].className = "sub_nav_hor";
    })
  })

});
