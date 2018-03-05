function handleLogout() {
  console.log("Logging out....");
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

function renderNavbar() {
  // Check with server if token is valid
  // If token is not valid, set the token to null
  token = readToken();
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
          <li><a href="#" id="logout" onclick="handleLogout()">Logout</a></li>
        `)
      } else {
        // Invalid token or not logged in
        $('#navbar').html(`
          <li><a href="/diary">Public Posts</a></li>
          <li><a href="/register_form">Register</a></li>
          <li><a href="/login_form">Login</a></li>
        `)
      }
    }
  });
}

// Renders the navigation bar according to the user's authentication status
renderNavbar();
