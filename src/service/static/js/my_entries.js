var MY_ENTRIES_METHOD = {
  handlerData:function(resJSON){
    console.log(resJSON);
    console.log(readToken);
    console.log($("#entry-template").html());
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

$(document).ready(function(){
  console.log("test");
  MY_ENTRIES_METHOD.loadEntryData();
});
