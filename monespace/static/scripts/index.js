document.addEventListener("DOMContentLoaded", function () {

  let events14Days = document.querySelector('#events_14_days');
  let messages = document.querySelector('#messages');

  let events14DaysMenu = document.querySelector('#events_14_days_menu');
  let messagesMenu = document.querySelector('#messages_menu');

if (document.querySelector('#events_manager_menu')) {
  let eventsManager = document.querySelector('#events_manager');
  let eventsManagerMenu = document.querySelector('#events_manager_menu');
  eventsManager.style.display = 'block';
  events14Days.style.display = 'none';
  messages.style.display = 'none';
  eventsManagerMenu.className = "sub_nav_hor active";
  events14DaysMenu.className = "sub_nav_hor";

  eventsManagerMenu.addEventListener('click', () => {
    events14Days.style.display = 'none';
    messages.style.display = 'none';
    eventsManager.style.display = 'block';
  })

  events14DaysMenu.addEventListener('click', () => {
    events14Days.style.display = 'block';
    messages.style.display = 'none';
    eventsManager.style.display = 'none';
  })

  messagesMenu.addEventListener('click', () => {
    events14Days.style.display = 'none';
    messages.style.display = 'block';
    eventsManager.style.display = 'none';
  })


} else {
  events14Days.style.display = 'block';
  messages.style.display = 'none';

  events14DaysMenu.addEventListener('click', () => {
    events14Days.style.display = 'block';
    messages.style.display = 'none';
  })

  messagesMenu.addEventListener('click', () => {
    events14Days.style.display = 'none';
    messages.style.display = 'block';
  })

  }



});
