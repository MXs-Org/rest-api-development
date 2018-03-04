function handleLogout() {
  console.log("logging out....");
  var token = readToken();
  console.log(token);
  $.ajax({
    url: 'http://localhost:8080/users/expire',
    type: "POST",
    dataType: 'json',
    contentType: "application/json; charset=utf-8",
    data: JSON.stringify({"token": token}),
    success: function(response) {
      if(response["status"] == true) {
        deleteToken();
        Materialize.toast("Logging out...", 4000);
        window.location.href = "/";
      } else {
        Materialize.toast("Can't log out at this moment!", 4000);
      }
    },
    error: function(xhr, resp, text) {
      Materialize.toast("Something went horribly wrong!", 4000);
    }
  });
  event.preventDefault();
}