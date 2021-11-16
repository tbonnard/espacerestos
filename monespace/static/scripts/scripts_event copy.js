document.addEventListener("DOMContentLoaded", function () {


async function api_call(url, parent_event, date) {
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  const request = new Request(
                    `${window.location.origin}/${url}`,
                    {headers: {'X-CSRFToken': csrftoken}}
                );
  const response = await fetch(request, {
    method:'POST',
    mode: 'same-origin',
    body: JSON.stringify({
            parent_event: parent_event,
            event_date: date,
        }),
  })
  .then(response => response.json())
  .then(data => console.log(data))

  document.querySelectorAll(".attendees_declines").forEach(e => e.parentNode.removeChild(e));
  all_attendees_user();

  }


  function all_attendees_user() {
    fetch(`${window.location.origin}/api_get_all_attendees_user/`)
    .then(response => response.json())
    .then(data => {

      let attendees = document.querySelectorAll('.attendees');
      attendees.forEach(i => {

        let eventid = i.dataset.eventid;
        let date = i.dataset.date;
        for (const j in data) {

          if (data[j].parent_event == eventid && data[j].event_date == date) {
            let div = document.createElement('div');
            div.className = 'attendees_declines';
            i.append(div);
            let p = document.createElement('p');
            div.append(p);
            let button = document.createElement('button');
            div.append(button);
            p.innerHTML = 'Inscrit';
            button.textContent = 'Annuler';
            button.id = `${eventid}_${date}`
            button.className="button_attendee_decline";
            button.addEventListener('click', (e) => {
              e.preventDefault();
              console.log(div.id);
              api_call('api_decline_event/', eventid, date);
            })
          }
        }
      })

      attendees.forEach(i => {
        let eventid = i.dataset.eventid;
        let date = i.dataset.date;
        if (i.children.length == 0 ) {
          let div = document.createElement('div');
          div.className = 'attendees_declines';
          i.append(div);
          let p = document.createElement('p');
          div.append(p);
          let button = document.createElement('button');
          div.append(button);
          p.innerHTML = 'Non inscrit';
          button.textContent = 'Rejoindre le groupe';
          button.className="button_attendee_decline";
          button.addEventListener('click', (e) => {
            e.preventDefault();
            api_call('api_attend_event/', eventid, date);
          })
        }
      })

    })

  };

all_attendees_user();

});
