function handleLoginFormSubmit() {
    $("#submit").on('click', function(event) {
        var username = $('#username').val();
        var password = $('#password').val();
        $.ajax({
          url: 'http://localhost:8080/users/authenticate',
          type: "POST",
          dataType: 'json',
          contentType: "application/json; charset=utf-8",
          data: JSON.stringify({"username": username, "password": password}),
          success: function(response) {
            if(response["status"] == true) {
              Materialize.toast("Logging in...", 4000);
              saveToken(response['result']['token']);
              window.location.href = "/diary";
            } else {
              Materialize.toast(response["error"], 4000);
            }
          },
          error: function(xhr, resp, text) {
            Materialize.toast("Something went horribly wrong!", 4000);
          }
        });
        event.preventDefault();
      }
    );
}

$(document).ready(function() {
  handleLoginFormSubmit();
});
