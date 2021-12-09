document.addEventListener("DOMContentLoaded", function () {

  let events14Days = document.querySelector('#events_14_days');
  let messages = document.querySelector('#messages');

  let events14DaysMenu = document.querySelector('#events_14_days_menu');
  let messagesMenu = document.querySelector('#messages_menu');

if (document.querySelector('#events_manager_menu')) {
  let eventsManager = document.querySelector('#events_manager');
  let eventsManagerMenu = document.querySelector('#events_manager_menu');

  eventsManager.style.display = 'block';
  events14Days.style.display = 'none';
  messages.style.display = 'none';
  eventsManagerMenu.className = "sub_nav_hor active";
  events14DaysMenu.className = "sub_nav_hor";

  eventsManagerMenu.addEventListener('click', () => {
    events14Days.style.display = 'none';
    messages.style.display = 'none';
    eventsManager.style.display = 'block';
  })

  events14DaysMenu.addEventListener('click', () => {
    events14Days.style.display = 'block';
    messages.style.display = 'none';
    eventsManager.style.display = 'none';
  })

  messagesMenu.addEventListener('click', () => {
    events14Days.style.display = 'none';
    messages.style.display = 'block';
    eventsManager.style.display = 'none';
  })


  let buttonEvenManagerLoad = document.querySelector('#button_event_manager_load');

  const user_id = buttonEvenManagerLoad.dataset.ideventsearch;

  buttonEvenManagerLoad.addEventListener('click', (e) => {
    e.preventDefault();
    let eventManagerDate = document.querySelectorAll('.event_manager_date');
    let fromDate = new Date(eventManagerDate[eventManagerDate.length -1].dataset.event_manager_date+" 00:00:00");
    fromDate.setDate(fromDate.getDate()+2);
    let toDate = new Date(eventManagerDate[eventManagerDate.length -1].dataset.event_manager_date+" 00:00:00");
    toDate.setDate(toDate.getDate()+14);
    let url = `${window.location.origin}/events_list_json/${user_id}?from=${fromDate.toISOString().split('T')[0]}&to=${toDate.toISOString().split('T')[0]}`;
    // console.log(url);
    // console.log(fromDate);
    // console.log(toDate);
    fetch(url)
      .then(response => response.json())
      .then(data => {
        let options = {day: 'numeric', month: 'long', year: 'numeric'}
        // console.log(data);
        data.forEach( i => {
          i[1].forEach(j => {
            // console.log(j);
            let tbody = document.querySelector('#tbody_event_manager');
            let tr = document.createElement('tr');
            let tdDate = document.createElement('td');
            tdDate.className='table_cell';
            let aUrlEvent = document.createElement('a');
            aUrlEvent.className = "event_manager_date";
            aUrlEvent.dataset.event_manager_date = new Date(i[0]+" 00:00:00").toISOString().split('T')[0];
            aUrlEvent.textContent = new Date(i[0]+" 00:00:00").toLocaleDateString('fr-FR', options);
            aUrlEvent.href = `${window.location.origin}/event/${j.id}?date=${i[0]}`;
            let tdName = document.createElement('td');
            tdName.className='table_cell';
            tdName.textContent = j.name;
            let tdTime = document.createElement('td');
            tdTime.className='table_cell';
            tdTime.textContent = `${j.time_from.slice(0, -3)} - ${j.time_to.slice(0, -3)}`;
            let tdBenevoles = document.createElement('td');
            tdBenevoles.className='table_cell';
            tbody.append(tr);
            tr.append(tdDate);
            tdDate.append(aUrlEvent);
            tr.append(tdName);
            tr.append(tdTime);
            tr.append(tdBenevoles);
            })
          })
          eventManagerDate = document.querySelectorAll('.event_manager_date');
      });
  })



} else {
  events14Days.style.display = 'block';
  messages.style.display = 'none';

  events14DaysMenu.addEventListener('click', () => {
    events14Days.style.display = 'block';
    messages.style.display = 'none';
  })

  messagesMenu.addEventListener('click', () => {
    events14Days.style.display = 'none';
    messages.style.display = 'block';
  })

  }



});
