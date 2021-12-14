document.addEventListener("DOMContentLoaded", function () {

  let sendMessagesGlobal = document.querySelector('#send_messages_global');
  let successMessages = document.querySelector('#success_message_result');
  let sendMessagesDiv = document.querySelector('#send_message_div');
  let sendMessagesFormButton = document.querySelector('#send_messages_form_button');


  let event_id = null;
  let event_date = null;
  let group = null;
  let all_site = false;
  let user = null;
  let location = null;
  let descriptionField = document.querySelector('#id_description');
  const borderColor = "#cacaca";

  if (document.querySelector('#id_to_event_group')) {
    groupField = document.querySelector('#id_to_event_group');
   }


   let listFieldsValidation = [descriptionField]
   if (groupField) {
     listFieldsValidation = [descriptionField, groupField]
     }


  let close_message_box = document.querySelector('#close_message_box');

  close_message_box.addEventListener('click',() =>{
    sendMessagesGlobal.style.display = 'none';
    listFieldsValidation.forEach(i => {
        i.style.borderColor = borderColor;
        i.value = null;
    })
  })

  function send_message(event_id, event_date, all_site, user, location, group, description) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const request = new Request(
                      `${window.location.origin}/send_message/`,
                      {headers: {'X-CSRFToken': csrftoken}}
                  );
    const response = fetch(request, {
      method:'POST',
      mode: 'same-origin',
      body: JSON.stringify({
              event: event_id,
              date: event_date,
              all_site: all_site,
              user: user,
              location: location,
              group: group,
              description: description
          }),
    })
    .then(response => response.json())
    .then(data => {
      console.log(data);
    })

    }


  sendMessagesFormButton.addEventListener('click', (e) => {
    let description = descriptionField.value;
    let validationNumber = 0

    listFieldsValidation.forEach(i => {
      if (i.value != '') {
        validationNumber+=1
      }
    })

    if (validationNumber == listFieldsValidation.length) {

      if (groupField) {
        group = groupField.value;
       }

       if (sendMessagesFormButton.dataset.event) {
         event_id = sendMessagesFormButton.dataset.event
       }
       if (sendMessagesFormButton.dataset.location) {
         location = sendMessagesFormButton.dataset.location
       }
       if (sendMessagesFormButton.dataset.date) {
         event_date = sendMessagesFormButton.dataset.date
       }
       if (sendMessagesFormButton.dataset.all_site) {
         all_site = sendMessagesFormButton.dataset.all_site
       }
       if (sendMessagesFormButton.dataset.user) {
         user = sendMessagesFormButton.dataset.user
       }

       send_message(event_id, event_date, all_site, user, location, group, description);

       listFieldsValidation.forEach(i => {
           i.style.borderColor = borderColor;
           i.value = null;
       })

       sendMessagesDiv.style.display = 'none';
       successMessages.style.display = 'block';
       setTimeout(function(){
         sendMessagesGlobal.style.display = 'none';
         successMessages.style.display = 'none';
         sendMessagesDiv.style.display = 'block';
      }, 3000);


    } else {
      listFieldsValidation.forEach(i => {
        if (i.value == '') {
          i.style.borderColor = "red";
        }
      })
    }

  })


});
