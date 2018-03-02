function handleLoginFormSubmit() {
    $("#submit").on('click', function(event) {
        var username = $('#username').val();
        var password = $('#password').val();
        $.ajax({
          url: '/users/authenticate',
          type: "POST",
          dataType: 'json',
          contentType: "application/json; charset=utf-8",
          data: JSON.stringify({"username": username, "password": password}),
          success: function(result) {
            console.log(result);
            if(result["status"] == true) {
              Materialize.toast(result['token'], 4000);
              // window.location.href = "/diary";
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
  handleLoginFormSubmit();
});
