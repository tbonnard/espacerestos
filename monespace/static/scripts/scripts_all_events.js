document.addEventListener("DOMContentLoaded", function () {

  let date_from_select= document.querySelector('#date_from');
  let date_to_select = document.querySelector('#date_to');
  let form_action = document.querySelector('#form_search_dates');

  let url = new URL(window.location.href);
  let params = new URLSearchParams(url.search);
  let param_from_value = params.get('from');
  let param_to_value = params.get('to');

  date_from_select.value = param_from_value ;
  date_to_select.value = param_to_value ;


  function diff_dates () {
    let date_from = document.querySelector('#date_from').value;
    let date_to = document.querySelector('#date_to').value;
    // dt1 = new Date(date_from);
    // dt2 = new Date(date_to);
    // diff_dates_result= Math.floor((Date.UTC(dt2.getFullYear(), dt2.getMonth(), dt2.getDate()) - Date.UTC(dt1.getFullYear(), dt1.getMonth(), dt1.getDate()) ) /(1000 * 60 * 60 * 24));
    form_action.href = `${window.location.origin}/events/?from=${date_from}&to=${date_to}`
    }

  date_from_select.addEventListener('change', () => {
    diff_dates()
  })

  date_to_select.addEventListener('change', () => {
    diff_dates()
  })

  window.history.replaceState(null, 'Recherche Mon Espace', '/events');

});
