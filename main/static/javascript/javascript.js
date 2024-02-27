$(document).ready(function () {
  $('#birthdate').attr("max",get_current_date).attr("value",get_current_date);
  $('#birthdate').on("blur",function(){
    if(under_18()){ //when you enter a birthdate this blocks the no option if you are under 18
      console.log(under_18())
      $($('#yes').prop('checked', true));
      allow_guardian_inputs();
    }
    else{
      allow_guardian_inputs();
    }
  });
  $("input[name=guardian]").change(function(){
    if(under_18()){ //when you click on yes or no, blocks no if you are under 18
      $($('#yes').prop('checked', true));
      allow_guardian_inputs();
    }
    else{
      allow_guardian_inputs();
    }
  });
  $('#no').on("click", function(){
    if(under_18()){ //can't click on no if you are under 18
      alert("Je bent onder de 18 en moet een voogd of toezichthouder toevoegen!")
    }
  });
});
function allow_guardian_inputs(){
  if($("#yes").is(':checked')){ //if yes button is checked, show the inputs for guardian
    $("#guardian_inputs").show();
  }
  else{
    $("#guardian_inputs").hide(); // don't show guardian inputs
  }
};
function under_18(){
  //return true or false if the user is 18 or not
  var date_18 = new Date(get_current_date());
  date_18.setFullYear(date_18.getFullYear()-18); //gets the date before which you need to be born to be 18 or older
  entered_date = new Date($('#birthdate').val()) //the date entered on the form
  if (date_18 < entered_date){
    return true;
  }
  else{
    return false;
  }
};
function get_current_date(){
  //returns the current date
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