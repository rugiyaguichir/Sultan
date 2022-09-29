const header = document.querySelector('header');

function validateForm() {
  var x = document.forms["myForm"]["username"].value;
  if (x == "") {
    alert("Name must be filled out");
    return false;
  }
}

function myFunction() {
  var str = "Как правильно регистрироваться на сайтах";
  var result = str.link("http://prosto-ponyatno.ru/komp-dlya-pro/kak-pravilno-registrirovatsya-na-sajtax/");
  document.getElementById("demo").innerHTML = result;
}

