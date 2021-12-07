document.addEventListener("DOMContentLoaded", function () {

  let eventDetails = document.querySelector('#event_details');
  let attendance = document.querySelector('#attendance');

  attendance.style.display = 'none';

  let eventDetailsMenu = document.querySelector('#eventDetails_menu');
  let attendanceMenu = document.querySelector('#attendance_menu');

  eventDetailsMenu.addEventListener('click', () => {
    eventDetails.style.display = 'block';
    attendance.style.display = 'none';
  })

  attendanceMenu.addEventListener('click', () => {
    eventDetails.style.display = 'none';
    attendance.style.display = 'block';
  })


});
