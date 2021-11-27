document.addEventListener("DOMContentLoaded", function () {


//DATES TIME MANAGEMENT
  let startDateInput = document.querySelector('#id_start_date');
  let endDateInput = document.querySelector('#id_end_date');
  let timeFromInput = document.querySelector('#id_time_from');
  let timeToInput = document.querySelector('#id_time_to');
  let fullDay = document.querySelector('#id_is_full_day');
  let timeFromInputInitial = timeFromInput.value;
  let timeToInputInitial = timeToInput.value;


  function updateEndDate() {
    endDateInput.value = startDateInput.value;
  }

  function updateToTime() {
    timeToInput.value = timeFromInput.value;
  }

  startDateInput.addEventListener('change', () => {
    updateEndDate();
  })

  endDateInput.addEventListener('change', () => {
    if (endDateInput.value == '') { updateEndDate(); }
  })

  timeFromInput.addEventListener('change', () => {
    updateToTime();
  })

  fullDay.addEventListener('click', () => {
    if (fullDay.checked) {
      timeFromInput.value = "00:00:00";
      timeToInput.value = "23:59:59";
    } else {
      timeFromInput.value = timeFromInputInitial;
      timeToInput.value = timeToInputInitial;
    }

  })

  updateEndDate();


// RECURRING MANAGEMENT
  function toggle_rec_form (is_rec, is_rec_form) {
    if (is_rec.checked) {
      is_rec_form.style.display = 'block';
      }
    else {
          is_rec_form.style.display = 'none';
        }
      }

    function manageEndDateRecurring (is_rec, endDateInput) {
      if (is_rec.checked) {endDateInput.disabled = true;}
      else {endDateInput.disabled = false;}
    }

  if ( document.querySelector('#id_is_recurring') && document.querySelector('#recurring') ) {
    let is_rec = document.querySelector('#id_is_recurring');
    let is_rec_form = document.querySelector('#recurring');


    is_rec.addEventListener('click', () => {
        toggle_rec_form(is_rec, is_rec_form);
        manageEndDateRecurring(is_rec, endDateInput);
    });

    if (document.querySelector('#id_separation_count').value =='') {
      document.querySelector('#id_separation_count').value =1;
    }


    toggle_rec_form(is_rec, is_rec_form);
    manageEndDateRecurring(is_rec, endDateInput);
  }



});
