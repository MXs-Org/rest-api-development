function handleRegisterFormSubmit() {
    $("#submit").on('click', function(event) {
        var username = $('#username').val();
        var password = $('#password').val();
        var fullname = $('#fullname').val();
        var age = $('#age').val();

        $.ajax({
          url: '/users/register',
          type: "POST",
          dataType: 'json',
          data: JSON.stringify({data: {"username": username, "password": password, "fullname": fullname, "age": age}}),
          success: function(result) {
            console.log(result);
          },
          error: function(xhr, resp, text) {
            console.log(xhr, resp, text);
          }
        });
        // alert("test");
        event.preventDefault();
      }
    );
}

$(document).ready(function() {
  handleRegisterFormSubmit();
});
