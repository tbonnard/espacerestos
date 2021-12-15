document.addEventListener("DOMContentLoaded", function () {


  // check width of the window and based on that hide the menu
      if (window.innerWidth < 990) {
          ToggleMenu();
      }

      // function to hide/unhide the menu-sidebar
      function ToggleMenu() {
          document.querySelector('.sidebar').classList.toggle("sidebarTransform");
          document.querySelector('#menu_icon_image').classList.toggle("logo_img_menu");
      }

    // click on the menu icon toggle the sidebar-menu
  document.querySelector('#menu').addEventListener('click', function () {
      ToggleMenu();
  });



  let subMenuDivIcon = document.querySelector('.sub_menu_icon');
  let topBarMenu = document.querySelector('.top_bar_menu');
  let subMenuIcon = document.querySelector('#sub_menu_icon');

  if (window.location.pathname.includes('event/liste/')) {
    subMenuDivIcon.style.visibility = 'hidden';
  }

  function ToggleSubMenu() {
      document.querySelector('.top_bar_menu').classList.toggle("sidebarTransform_top_bar_menu");
  }

  if (window.innerWidth < 990) {
      ToggleSubMenu();
  }

  window.addEventListener('resize', function(event){
    if (window.innerWidth < 990) {
      ToggleMenu();
      ToggleSubMenu();
    }
  });


  subMenuDivIcon.addEventListener('click',() => {
    ToggleSubMenu();
    if (subMenuIcon.dataset.state == 'to_visible') {
      subMenuIcon.dataset.state = 'to_hidden';
      subMenuIcon.className = "fas fa-chevron-circle-up";
    } else {
      subMenuIcon.dataset.state = 'to_visible';
      subMenuIcon.className = "fas fa-chevron-circle-down";
    }

  })





  function check_active_url(i) {
    // console.log(i);
    let path = window.location.pathname.split('/')[1].toLowerCase();
    // console.log(path);
    let menu_path = i.dataset.path.toLowerCase();
    // console.log(menu_path);

      if ( path == menu_path ) {
      i.className = "item_nav item_nav_active";
    }
  }

   let side_menu = document.querySelectorAll(".item_nav");
   side_menu.forEach( i => {
     check_active_url(i);
   })


   if (document.querySelector('#event_link_date')) {
     let numWeeks = 8;
     let now = new Date();
     now.setDate(now.getDate() + numWeeks * 7);
     event_link = document.querySelector('#event_link_date');
     event_link_original = event_link.href
     date_to = now.toISOString().split('T')[0];
     event_link.href = event_link_original+date_to;
   }


});
