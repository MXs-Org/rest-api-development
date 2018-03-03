var MY_ENTRIES_METHOD = {
  handlerData:function(resJSON){
      var templateSource   = $("#entry-template").html(),
          template = Handlebars.compile(templateSource),
          entryHTML = template(resJSON);
     $('#entries-container').html(entryHTML);
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
  $("#delete-entry").on('click', function(event) {
  }
}

$(document).ready(function(){
  MY_ENTRIES_METHOD.loadEntryData();
});
