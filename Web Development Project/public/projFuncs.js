var slideIndex = 1;
var myTimer;

function advSlides(n) {
  clearInterval(myTimer);
  if (n < 0){
    showSlides(slideIndex -= 1);
  } else {
   showSlides(slideIndex += 1); 
  }
  if (n === -1){
    myTimer = setInterval(function(){advSlides(n + 2)}, 4000);
  } else {
    myTimer = setInterval(function(){advSlides(n + 1)}, 4000);
  }
}

function showSlides(n) {
  var i;
  var slides = document.getElementsByClassName("homePhoto");
  if (n > slides.length) {slideIndex = 1}
  if (n < 1) {slideIndex = slides.length}
  for (i = 0; i < slides.length; i++) {
      slides[i].style.display = "none";
  }
  slides[slideIndex-1].style.display = "block";
}


function formMessage() {
  var hideContent = document.getElementbyId("unsubContent");
  var showContent = document.getElementbyId("subContent");
  hideContent.style.display = "none";
  showContent.style.display = "block";
  event.preventDefault();
}

document.addEventListener("DOMContentLoaded",function() {
    showSlides(slideIndex);
    myTimer = setInterval(function(){plusSlides(1)}, 4000);
})
document.getElementbyId("formSubmit").addEventListener("click", formMessage);