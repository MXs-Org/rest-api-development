var MY_ENTRIES_METHOD = {
  handlerData:function(resJSON){
      var templateSource   = $("#entry-template").html(),
          template = Handlebars.compile(templateSource),
          entryHTML = template(resJSON);
     $('#entries-container').html(entryHTML);
     deleteEntry();

  },
  loadEntryData : function(){
    $.ajax({
      url:"http://localhost:8080/diary",
      method:'post',
      dataType: 'json',
      contentType: "application/json; charset=utf-8",
      data: JSON.stringify({"token": readToken()}),
      success:this.handlerData
    })
  }
};

function deleteEntry(){
  $(".delete-entry").on("click", function(event) {
  	var token = readToken();
  	var id = $(".delete-entry").val();
	  $.ajax({
	    url: 'http://localhost:8080/diary/delete',
	    type: "POST",
	    dataType: 'json',
	    contentType: "application/json; charset=utf-8",
	    data: JSON.stringify({"token": token, "id": id}),
	    success: function(response) {
	      if(response["status"] == true) {
	        Materialize.toast("Deleted Entry", 4000);
	        window.location.href = "/diary/my_entries"
	      } else {
	        Materialize.toast("Authentication failed", 4000);
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

$(document).ready(function(){
  MY_ENTRIES_METHOD.loadEntryData();
});
