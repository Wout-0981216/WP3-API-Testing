$(document).ready(function () {
  $('#birthdate').attr("max",get_current_date).attr("value",get_current_date);
  $('#birthdate').on("blur",function(){
    if(under_18()){
      console.log(under_18())
      $($('#yes').prop('checked', true));
      allow_guardian_inputs();
    }
    else{
      allow_guardian_inputs();
    }
  });
  $("input[name=guardian]").change(function(){
    if(under_18()){
      $($('#yes').prop('checked', true));
      allow_guardian_inputs();
    }
    else{
      allow_guardian_inputs();
    }
  });
  $('#no').on("click", function(){
    if(under_18()){
      alert("Je bent onder de 18 en moet een voogd of toezichthouder toevoegen!")
    }
  });
});
function allow_guardian_inputs(){
  if($("#yes").is(':checked')){
    $("#guardian_inputs").show();
  }
  else{
    $("#guardian_inputs").hide();
  }
};
function under_18(){
  var date_18 = new Date(get_current_date());
  //gets the date before which you need to be born to be 18 or older
  date_18.setFullYear(date_18.getFullYear()-18);
  entered_date = new Date($('#birthdate').val())
  if (date_18 < entered_date){
    return true;
    $($('#yes').prop('checked', true));
    allow_guardian_inputs();
  }
  else{
    return false;
    allow_guardian_inputs();
  }
};
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
};