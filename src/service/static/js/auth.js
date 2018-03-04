// Handles all the code for localstorage cookies

function saveToken(token) {
  localStorage.setItem("token", token);
}

function readToken() {
    // Reads the token from localstorage
    return localStorage.getItem("token");
}

function deleteToken() {
  localStorage.removeItem("token");
}

function renderNavbar() {
  // Check with server if token is valid
  // If token is not valid, set the token to null
  token = readToken()
  console.log(token);
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