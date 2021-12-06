document.addEventListener("DOMContentLoaded", function () {

  let profile = document.querySelector('#profile');
  let locations = document.querySelector('#locations');

  locations.style.display = 'none';

  let profileMenu = document.querySelector('#profile_menu');
  let locationsMenu = document.querySelector('#locations_menu');

  profileMenu.addEventListener('click', () => {
    profile.style.display = 'block';
    locations.style.display = 'none';
  })

  locationsMenu.addEventListener('click', () => {
    profile.style.display = 'none';
    locations.style.display = 'block';
  })


});
