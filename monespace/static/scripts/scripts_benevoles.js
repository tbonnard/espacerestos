document.addEventListener("DOMContentLoaded", function () {


  let active_button= document.querySelectorAll('.button_active_status');
  let form_status_button= document.querySelectorAll('.button_form_status');
  let form_status= document.querySelectorAll('.form_status');

  form_status.forEach(i => {
    i.style.display = 'none';
  })

  form_status_button.forEach(i => {
    i.addEventListener('click', () => {
      form_status.forEach(j => {
        if (i.dataset.user==j.dataset.user && j.style.display == 'block') {
          j.style.display = 'none';
        } else  if (i.dataset.user==j.dataset.user && j.style.display == 'none') {
          j.style.display = 'block';
        }
      })
    })
  })

});
