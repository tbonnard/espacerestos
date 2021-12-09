document.addEventListener("DOMContentLoaded", function () {

  let locationDetailsMenu = document.querySelector('#location_details_menu');
  let locationSoireeMenu = document.querySelector('#location_soirees_menu');

  let locationDetails = document.querySelector('.location_global');
  let locationSoiree = document.querySelector('#soirees');

  locationSoiree.style.display = 'none';

  locationDetailsMenu.addEventListener('click', () => {
    locationDetails.style.display = 'block';
    locationSoiree.style.display = 'none';
  })

  locationSoireeMenu.addEventListener('click', () => {
    locationDetails.style.display = 'none';
    locationSoiree.style.display = 'block';
  })


  let buttonCancel = document.querySelectorAll('.button_form_status');
  let divCancelValidation = document.querySelectorAll('#div_cancel_validation');
  let trDistrib = document.querySelectorAll('.tr_distrib');

  buttonCancel.forEach(i => {
    i.addEventListener('click', () => {
    divCancelValidation.forEach(y => {
      if (i.dataset.event == y.dataset.event) {
        y.style.display = 'none';
        trDistrib.forEach(z => {
          if (i.dataset.event == z.dataset.event) {
            let tdValidateCancel = document.createElement('td');
            tdValidateCancel.className='table_cell';
            tdValidateCancel.textContent = "Êtes-vous certain?";
            let divCancel =document.createElement('div');
            divCancel.style.marginTop = '5px';
            divCancel.style.marginBottom = '5px';
            let aValidateCancelYes = document.createElement('a');
            aValidateCancelYes.href = `${window.location.origin}/event_delete_all/${i.dataset.event}`;
            aValidateCancelYes.title = `Oui, annuler la distribution`;
            let iValidateCancelYes = document.createElement('i');
            iValidateCancelYes.className = "fas fa-check-square";
            iValidateCancelYes.style.marginRight = '10px';
            let aValidateCancelNo = document.createElement('a');
            aValidateCancelNo.title = 'Non, laisser la date';
            let iValidateCancelNo = document.createElement('i');
            iValidateCancelNo.className = "far fa-window-close";
            iValidateCancelNo.style.marginLeft = '5px';
            z.append(tdValidateCancel);
            tdValidateCancel.append(divCancel);
            divCancel.append(aValidateCancelYes)
            divCancel.append(aValidateCancelNo)
            aValidateCancelYes.append(iValidateCancelYes);
            aValidateCancelNo.append(iValidateCancelNo);
            iValidateCancelNo.addEventListener('click', () => {
              tdValidateCancel.style.display='none';
              y.style.display = 'block';
            })
          }
        })
      }
    })
    })
  })


});
