function darkmode() {
  const wasDarkmode = localStorage.getItem('darkmode') === 'true';
  localStorage.setItem('darkmode', !wasDarkmode);
  document.body.classList.toggle('dark-mode', !wasDarkmode);
  // for(element in document.h1){
  //   element.classList.toggle('dark-mode', !wasDarkmode);
  // }

  // for(let element2 in document.h2){
  //   element2.classList.toggle('dark-mode', !wasDarkmode);
  // }
  
  
}

function onload() {
  document.body.classList.toggle('dark-mode', localStorage.getItem('darkmode') === 'true');
}