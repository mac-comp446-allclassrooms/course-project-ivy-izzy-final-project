function darkmode() {
  const wasDarkmode = localStorage.getItem('darkmode') === 'true';
  localStorage.setItem('darkmode', !wasDarkmode);
  document.body.classList.toggle('dark-mode', !wasDarkmode);
  var navbarElem = document.getElementsByClassName('nav');
  
    for (const element of navbarElem) {
      element.classList.toggle('dark-mode', !wasDarkmode);
    }
  
}

function onload() {
  const wasDarkmode = localStorage.getItem('darkmode') === 'true';
  localStorage.setItem('darkmode', !wasDarkmode);
  document.body.classList.toggle('dark-mode', !wasDarkmode);
  var navbarElem = document.getElementsByClassName('nav');
  
    for (const element of navbarElem) {
      element.classList.toggle('dark-mode', !wasDarkmode);
    }
  console.log('hi');  
}
