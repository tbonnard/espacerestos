document.addEventListener("DOMContentLoaded", function () {

  let tr_td_row = document.querySelectorAll('.tr_td_row');

  tr_td_row.forEach(i => {
    i.style.display = 'none';
  })

  let locationCheckBox = document.querySelectorAll('.locations_checkbox');
  let locationsName = document.querySelectorAll('.locations_name');

  locationCheckBox.forEach(j => {
    j.addEventListener('change', () => {
      tr_td_row.forEach(z => {
        if (j.checked) {
          if (z.dataset.loc == j.value) {
            z.style.display = 'contents';
            locationsName.forEach(c => {
              if (c.dataset.loc == j.value) {
                c.dataset.state='opened';
              }
            })
          }
        } else {
          if (z.dataset.loc == j.value) {
            z.style.display = 'none';
            locationsName.forEach(c => {
              if (c.dataset.loc == j.value) {
                c.dataset.state='closed';
              }
            })
          }
        }

      })
    })
  })

  locationsName.forEach(j => {
    j.addEventListener('click', () => {
      tr_td_row.forEach(z => {
        if (j.dataset.state=='closed') {
          if (z.dataset.loc == j.dataset.loc) {
            z.style.display = 'contents';
            j.dataset.state='opened';
            locationCheckBox.forEach(c => {
              if (c.value == j.dataset.loc) {
                c.checked=true;
              }
            })
          }
        } else {
          if (z.dataset.loc == j.dataset.loc) {
            z.style.display = 'none';
            j.dataset.state='closed';
            locationCheckBox.forEach(c => {
              if (c.value == j.dataset.loc) {
                c.checked=false;
              }
            })
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
        locationsName.forEach(y => {
          if (y.dataset.loc == i.location.id) {
          } else {
            y.style.pointerEvents="none";
            y.style.cursor="default";
            y.style.color='#222222';
          }
        })
      })
    })

  }

  get_event_location();


});
