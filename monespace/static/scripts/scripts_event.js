document.addEventListener("DOMContentLoaded", function () {


  let is_rec = document.querySelector('#id_is_recurring');
  let is_rec_form = document.querySelector('#recurring');

  toggle_rec_form();


  function toggle_rec_form () {
    if (is_rec.checked) {
      is_rec_form.style.display = 'block';
      }
    else {
          is_rec_form.style.display = 'none';
        }
      }


  is_rec.addEventListener('click', () => {
      toggle_rec_form()
  });


  let id_repeat_each_x = document.querySelector('#id_repeat_each_x');
  id_repeat_each_x.addEventListener('change', () => {
    if (id_repeat_each_x.value == "1" ) {
      document.querySelector('#id_day_of_week').style.display='none';
    } else {
      document.querySelector('#id_day_of_week').style.display='block';
    }
  });

if (document.querySelector('#id_separation_count').value =='') {
  document.querySelector('#id_separation_count').value =1;
}


});
