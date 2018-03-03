var DIARY_METHOD = {
  handlerData:function(resJSON){
    console.log(resJSON);
    console.log($("#entry-template").html());
      var templateSource   = $("#entry-template").html(),
          template = Handlebars.compile(templateSource),
          entryHTML = template(resJSON);
     $('#entries-container').html(entryHTML);
  },
  loadEntryData : function(){
    $.ajax({
      url:"http://localhost:8080/diary",
      method:'get',
      success:this.handlerData
    })
  }
};

$(document).ready(function(){
  DIARY_METHOD.loadEntryData();
});
