function checkIfNotLoggedIn(){
  token = readToken();
  $.ajax({
    url: 'http://localhost:8080/users/check',
    type: "POST",
    dataType: 'json',
    contentType: "application/json; charset=utf-8",
    data: JSON.stringify({"token": token}),
    success: function(response) {
      if(response["status"] == false) {
        window.location.href = "/login_form"
      } 
    }
  });
}

checkIfNotLoggedIn();