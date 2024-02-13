$(document).ready(function () {
  $("input[name=guardian]").change(function(){
    if($("#yes").is(':checked')){
      $("#guardian_inputs").show();
    }
    else{
      $("#guardian_inputs").hide();
    }
  });
});