function handleRegisterFormSubmit() {
    $("#submit").on('click', function(event) {
        var username = $('#username').val();
        var password = $('#password').val();
        var fullname = $('#fullname').val();
        var age = $('#age').val();
        $.ajax({
          url: 'http://localhost:8080/users/register',
          type: "POST",
          dataType: 'json',
          contentType: "application/json; charset=utf-8",
          data: JSON.stringify({"username": username, "password": password, "fullname": fullname, "age": age}),
          success: function(result) {
            if(result["status"] == true) {
              Materialize.toast("Your account has been created!", 4000);
              window.location.href = "/login_form";
            } else {
              Materialize.toast(result["error"], 4000);
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
  handleRegisterFormSubmit();
});
