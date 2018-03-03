function handleCreateEntrySubmit() {
    $("#submit").on('click', function(event) {
        var token = readToken();
        var title = $('#title').val();
        var public = $('#public').val();
        var text = $('#text').val();
        
        $.ajax({
          url: 'http://localhost:8080/diary/create',
          type: "POST",
          dataType: 'json',
          contentType: "application/json; charset=utf-8",
          data: JSON.stringify({"token": token, "title": title, "public": public, "text": text}),
          success: function(response) {
            if(response["status"] == true) {
              Materialize.toast("Your entry has been created!", 4000);
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
  handleCreateEntrySubmit();
});
