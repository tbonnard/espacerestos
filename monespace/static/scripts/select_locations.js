document.addEventListener("DOMContentLoaded", function () {

  let tr_td_row = document.querySelectorAll('.tr_td_row');

  tr_td_row.forEach(i => {
    i.style.display = 'none';
  })

  let locationCheckBox = document.querySelectorAll('.locations_checkbox');

  locationCheckBox.forEach(j => {
    j.addEventListener('change', () => {
      tr_td_row.forEach(z => {
        if (j.checked) {
          if (z.dataset.loc == j.value) {
            z.style.display = 'contents';
          }
        } else {
          if (z.dataset.loc == j.value) {
            z.style.display = 'none';
          }
        }

      })
    })
  })


  function get_event_location() {
    const request = new Request(
                      `${window.location.origin}/get_event_location/`,
                  );
    const response = fetch(request, {
      method:'GET',
      mode: 'same-origin'
    })
    .then(response => response.json())
    .then(data => {
      data.forEach(i => {
        // console.log(i);
        locationCheckBox.forEach(j => {
          if (j.value == i.location.id) {
          } else {
            j.style.display = 'none';
          }
        })
      })
    })

  }

  get_event_location();


});
