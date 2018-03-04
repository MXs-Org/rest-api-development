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
  $.ajax({
    url: 'http://localhost:8080/users/check',
    type: "POST",
    dataType: 'json',
    contentType: "application/json; charset=utf-8",
    data: JSON.stringify({"token": token}),
    success: function(response) {
      if(response["status"] == true) {
        console.log("changing html")
        $('#navbar').html(`
          <li><a href="/diary/create_form">Create</a></li>
          <li><a href="/diary/my_entries">My Posts</a></li>
          <li><a href="#">All Users</a></li>
          <li><a href="#" id="logout" onclick="handleLogout()">Logout</a></li>
        `)
      } else {
        // Invalid token or not logged in
        $('#navbar').html(`
          <li><a href="#">Public Posts</a></li>
          <li><a href="/register_form">Register</a></li>
          <li><a href="/login_form">Login</a></li>
        `)
      }
    }
  });
}

$(document).ready(function() {
  // Renders the navigation bar according to the user's authentication status
  renderNavbar();
});
