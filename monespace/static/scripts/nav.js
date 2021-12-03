document.addEventListener("DOMContentLoaded", function () {

  // check width of the window and based on that hide the menu
      if (screen.availWidth < 751) {
          ToggleMenu();
      }

      // function to hide/unhide the menu-sidebar
      function ToggleMenu() {
          document.querySelector('.sidebar').classList.toggle("sidebarTransform");
      }

    // click on the menu icon toggle the sidebar-menu
  document.querySelector('#menu').addEventListener('click', function () {
      ToggleMenu();
  });


  if (document.querySelector('#event_link_date')) {
    let numWeeks = 8;
    let now = new Date();
    now.setDate(now.getDate() + numWeeks * 7);
    event_link = document.querySelector('#event_link_date');
    event_link_original = event_link.href
    date_to = now.toISOString().split('T')[0];
    event_link.href = event_link_original+date_to;
  }


  function check_active_url(i) {
    console.log(i);
    let path = window.location.pathname;
    console.log(path);
    let menu_path = i.dataset.path;
    console.log(menu_path);

    if ( path.toLowerCase() == menu_path.toLowerCase()) {
      i.className = "item_nav item_nav_active";
    }
  }

   let side_menu = document.querySelectorAll(".item_nav");
   side_menu.forEach( i => {
     check_active_url(i);
   })


});
