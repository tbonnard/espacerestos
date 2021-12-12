document.addEventListener("DOMContentLoaded", function () {

  // let distribDetailsMenu = document.querySelector('#distrib_details_menu');
  // let distribBenevolesMenu = document.querySelector('#distrib_benevoles_menu');
  //
  // let distribDetails = document.querySelector('.distrib_global');
  // let distribBenevoles = document.querySelector('#distrib_benevoles');
  //
  // distribDetails.style.display = 'none';
  //
  // distribDetailsMenu.addEventListener('click', () => {
  //   distribDetails.style.display = 'block';
  //   distribBenevoles.style.display = 'none';
  // })
  //
  // distribBenevolesMenu.addEventListener('click', () => {
  //   distribDetails.style.display = 'none';
  //   distribBenevoles.style.display = 'block';
  // })

  let formChangeManager = document.querySelector('#change_manager');
  let iconChangeManager = document.querySelector('#icon_change_manager');
  formChangeManager.style.display = 'none';
  iconChangeManager.addEventListener('click', () => {
    formChangeManager.style.display = 'block';
    iconChangeManager.style.display = 'none';
    let approveChangeManager = document.querySelector('#icon_approve_change_manager');
    let cancelChangeManager = document.querySelector('#icon_cancel_change_manager');
    cancelChangeManager.addEventListener('click', () => {
      formChangeManager.style.display = 'none';
      iconChangeManager.style.display = 'inherit';
    })
  })


  if (document.querySelector('#event_link_date_distrib')) {
    let numWeeks = 8;
    let now = new Date();
    now.setDate(now.getDate() + numWeeks * 7);
    event_link = document.querySelector('#event_link_date_distrib');
    event_link_original = event_link.href
    date_to = now.toISOString().split('T')[0];
    event_link.href = event_link_original+date_to;
  }


});
