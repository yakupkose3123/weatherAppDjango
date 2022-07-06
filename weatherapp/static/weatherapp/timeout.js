let element = document.querySelector(".alert");


element &&
  setTimeout(function () {
    element.style.display = "none";
  }, 3000);
