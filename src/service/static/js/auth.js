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

function checkAuthenticated() {
  if (readToken() == null) {
    return false;
  }
  return true;
}

$(document).ready(function() {
  // Checks if user has a token set in localstorage.token
  // checkAuthenticated();
});
