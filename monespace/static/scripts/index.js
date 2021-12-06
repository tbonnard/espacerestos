document.addEventListener("DOMContentLoaded", function () {

  let events14Days = document.querySelector('#events_14_days');
  let messages = document.querySelector('#messages');
  let eventsManager = document.querySelector('#events_manager');

  messages.style.display = 'none';
  eventsManager.style.display = 'none';

  let events14DaysMenu = document.querySelector('#events_14_days_menu');
  let messagesMenu = document.querySelector('#messages_menu');
  let eventsManagerMenu = document.querySelector('#events_manager_menu');

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

  eventsManagerMenu.addEventListener('click', () => {
    events14Days.style.display = 'none';
    messages.style.display = 'none';
    eventsManager.style.display = 'block';
  })

});
