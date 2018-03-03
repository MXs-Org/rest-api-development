// Handles all the code for localstorage cookies

function saveToken(token) {
  localStorage.setItem("token", token);
}

function readToken() {
    // Reads the token from localstorage
    return localStorage.getItem("token");
}

function checkAuthenticated() {
  // TODO: implement this
  return ""
}

$(document).ready(function() {
  // Checks if user has a token set in localstorage.token
  // checkAuthenticated();
});
