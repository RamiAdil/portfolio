//document.addEventListener("DOMContentLoaded", () => {
//  const form = document.querySelector("form");
//
//  form.addEventListener("submit", (e) => {
//    e.preventDefault();
//    fetch(form.action, {
//      method: "POST",
//      body: new FormData(form),
//      headers: { 'Accept': 'application/json' }
//    }).then(response => {
//      if (response.ok) {
//        window.location.href = "thankyou.html";
//      } else {
//        alert("There was a problem sending your form.");
//      }
//    });
//  });
//});
