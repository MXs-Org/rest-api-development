var DIARY_METHOD = {
  handlerData:function(resJSON){
    var templateSource   = $("#entry-template").html(),
        template = Handlebars.compile(templateSource),
        entryHTML = template(resJSON);
    header = "<div class='col s12'><h5>Public Posts</h5>"
    if(entryHTML.trim() == ""){
      $('#entries-container').html(header + "<div class='card-panel'><div class='row'>No public posts! Why don't you create one?</div></div></div>")
    } else {
      $('#entries-container').html(header + entryHTML);
    }
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
