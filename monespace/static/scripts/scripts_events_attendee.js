document.addEventListener("DOMContentLoaded", function () {


function api_call_attend_decline(eventid, date, type) {
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  const request = new Request(
                    `${window.location.origin}/api_attend_decline_event/`,
                    {headers: {'X-CSRFToken': csrftoken}}
                );
  const response = fetch(request, {
    method:'POST',
    mode: 'same-origin',
    body: JSON.stringify({
            parent_event: eventid,
            event_date: date,
            type: type
        }),
  })
  .then(response => response.json())
  .then(data => {
    document.querySelectorAll(`#div_${eventid}${date}`).forEach(e => e.parentNode.removeChild(e));
    get_specific_attendees(eventid, date);
  })

  }



  function create_elements_attendees(parentDiv, eventid, date, pInner, buttonText, type) {
    let div = document.createElement('div');
    div.className = 'attendees_declines';
    div.id = `div_${eventid}${date}`
    parentDiv.append(div);
    let p = document.createElement('p');
    div.append(p);
    let button = document.createElement('button');
    div.append(button);
    p.innerHTML = pInner;
    button.innerHTML = buttonText;
    button.id = `${eventid}_${date}`;
    if (type == "decline") {
      button.className="button_attendee_decline button_inversed";
    } else {
      button.className="button_attendee_decline";
    }
    button.addEventListener('click', (e) => {
      e.preventDefault();
      api_call_attend_decline(eventid, date, type);
    })
  }


  function get_number_attendees(eventid, date) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const request = new Request(
                      `${window.location.origin}/api_get_count_specific_attendees/`,
                      {headers: {'X-CSRFToken': csrftoken}}
                  );
    const response = fetch(request, {
      method:'POST',
      mode: 'same-origin',
      body: JSON.stringify({
              parent_event: eventid,
              event_date: date,
          }),
    })
    .then(response => response.json())
    .then(data => {
      console.log(data[0])
      let span_number_attendees = document.querySelector(`#attend_event_number_${eventid}${date}`);
      if (data[0] > 1 ) {
        text_attendees_number = `${data} présences confirmées`
      } else if (data[0] > 0 ) {
        text_attendees_number = `${data} présence confirmée`
      } else {
        text_attendees_number = "0 présence confirmée"
      }
      span_number_attendees.innerHTML = text_attendees_number;
    })

  }

  let attendees_number_event = document.querySelectorAll(`.attend_event_number`);
  attendees_number_event.forEach( i => {
    get_number_attendees(i.dataset.eventid, i.dataset.date);
  })



  function get_specific_attendees (eventid, date) {
    fetch(`${window.location.origin}/api_get_specific_attendees/?parent_event=${eventid}&event_date=${date}`)
    .then(response => response.json())
    .then(data => {

      let div_attendees = document.querySelector(`#parent_${eventid}${date}`);
      for (const j in data) {
        if (data[j].parent_event == eventid && data[j].event_date == date) {
          create_elements_attendees(div_attendees, eventid, date, '', '<i class="fas fa-check-square icon_attend"></i>Annuler ma présence', 'decline');
          get_number_attendees(eventid, date);
        }
      }

      if (div_attendees.children.length == 0 ) {
        create_elements_attendees(div_attendees, eventid, date, '', '<i class="far fa-square icon_attend"></i>Confirmer ma présence', 'attend');
        get_number_attendees(eventid, date);
      }

    })

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
            create_elements_attendees(i, eventid, date, '', '<i class="fas fa-check-square icon_attend"></i>Annuler ma présence', 'decline');
          }
        }
      })

      attendees.forEach(i => {
        let eventid = i.dataset.eventid;
        let date = i.dataset.date;
        if (i.children.length == 0 ) {
          create_elements_attendees(i, eventid, date, '', '<i class="far fa-square icon_attend"></i>Confirmer ma présence', 'attend');
        }
      })

    })

  };

all_attendees_user();

});
