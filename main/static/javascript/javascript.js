$(document).ready(function () {
  $('#birthdate').attr("max",get_current_date)
  $("input[name=guardian]").change(function(){
    if($("#yes").is(':checked')){
      $("#guardian_inputs").show();
    }
    else{
      $("#guardian_inputs").hide();
    }
  });
});

function get_current_date(){
  var today = new Date();
  var dd = today.getDate();
  var mm = today.getMonth() + 1; //January is 0
  var yyyy = today.getFullYear();

  //add '0' to get correct format for day and month
  if (dd < 10) {
    dd = '0' + dd;
  }

  if (mm < 10) {
    mm = '0' + mm;
  } 

  today = yyyy + '-' + mm + '-' + dd;
  return today
}