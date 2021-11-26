document.addEventListener("DOMContentLoaded", function () {


  let confirm_button = document.querySelector('#confirm');
  confirm_button.style.display = 'none';

  let url = new URL(window.location.href);
  let params = new URLSearchParams(url.search);
  let param_from_value = params.get('date');

  let form_event_rec = document.querySelector('#form_rec');
  let eventid = form_event_rec.dataset.eventid;
  let yes_all = document.querySelector('#yes');
  let no_only = document.querySelector('#no');

  yes_all.addEventListener('click', () => {
    form_event_rec.action = `${window.location.origin}/event_edit/${eventid}`;
    confirm_button.style.display = 'block';
  });
  no_only.addEventListener('click', () => {
    form_event_rec.action = `${window.location.origin}/event_edit_one/${eventid}?date=${param_from_value}`;
    confirm_button.style.display = 'block';
  });




});
