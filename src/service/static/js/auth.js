function checkIfLoggedIn(){
  token = readToken();
  $.ajax({
    url: 'http://localhost:8080/users/check',
    type: "POST",
    dataType: 'json',
    contentType: "application/json; charset=utf-8",
    data: JSON.stringify({"token": token}),
    success: function(response) {
      if(response["status"] == true) {
        window.location.href = "/diary"
      } 
    }
  });
}

checkIfLoggedIn();