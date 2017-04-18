"use strict"

function showNewCohort(results) {
    // display 

    var resultString = results.string
    var resultId = results.createdId

    $("#cohort-list").append("<li id='new-cohort'><a href='/cohort" + resultId +"'>" + resultString + "</a></li>")

    $("#enter-cohort-name").val("")
    $("#enter-cohort-password").val("")
    $("#enter-grad-password").val("")
}

function submitNewCohortInfo(evt) {
    // post form data to the add-cohort route
    var today = new Date();
    var dd = today.getDate();
    var mm = today.getMonth()+4; //January is 0!
    var yyyy = today.getFullYear();

    var gradDate = $("#enter-grad-date").val() || yyyy + "-" + mm + "-" + dd

    var formInput = {
        "new_cohort_name": $("#enter-cohort-name").val(),
        "new_cohort_password": $("#enter-cohort-password").val(),
        "new_grad_date": gradDate
    }
    evt.preventDefault();
    $.post("/add-cohort", formInput, showNewCohort);
}

$('#create-cohort').on('submit', submitNewCohortInfo)

////////////////////////////////////////////////////////////////////////////////

function showNewLab(results) {
    // display 

    var resultString = results.string
    var resultId = results.createdId

    $("#lab-list").append("<li id='new-lab'><a href='/lab/" + resultId + "'>" + resultString + "</a></li>")

    $("#enter-lab-name").val("")
    $("#enter-lab-description").val("")
    $("#enter-lab-date").val("")
}

function submitNewLabInfo(evt) {
    // post form data to the add-cohort route
    var today = new Date();
    var dd = today.getDate();
    var mm = today.getMonth()+1; //January is 0!
    var yyyy = today.getFullYear();

    var labDate = $("#enter-lab-date").val() || yyyy + "-" + mm + "-" + dd

    var formInput = {
        "new_lab_name": $("#enter-lab-name").val(),
        "new_lab_description": $("#enter-lab-description").val(),
        "new_lab_date": labDate
    }

    evt.preventDefault();
    $.post("/add-lab", formInput, showNewLab);
}

$('#create-lab').on('submit', submitNewLabInfo)


////////////////////////////////////////////////////////////////////////////////

$('#new-pair').multiSelect({
  afterSelect: function(values){
    // if num of ms-selected = 2, disable all other students
    if ($('.ms-selected').length > 2) {
        $(".ms-elem-selectable").prop('disabled', true);
        $(".ms-elem-selectable").addClass(".greyed-out"); // TODO why doesn't this work???
    }

  },
  afterDeselect: function(values){
    // if num of ms-selected < 2, reenable all other students
    if ($('.ms-selected').length <= 2) {
        $(".ms-elem-selectable").prop('disabled', false);
    }
  }
});

  $('#deselect-all').click(function(){
    $('#new-pair').multiSelect('deselect_all');
    return false;
  });
  $('#refresh').on('click', function(){
    $('#new-pair').multiSelect('refresh');
    return false;
  });
  $('#add-option').on('click', function(){
    $('#new-pair').multiSelect('addOption', { value: 42, text: 'test 42', index: 0 });
    return false;
  });

//------------------------------------------------------------------------------


function showPairedStudents(results) {

    $("#established-pairs").html(" ");

    var pairs = results.pairs;
    var unpaireds = results.unpaireds;

    for (var pair of pairs){
        $("#established-pairs").append("<li><h3>" + pair.student_1_name + 
            " paired with " + pair.student_2_name + "</h3>notes: " + pair.notes + "</li>")
    }

    $("#new-pair").html(" ");

    for (var unpaired of unpaireds) {
        $("#new-pair").append("<option value='" + unpaired.student_id +"'>" + unpaired.student_name + "</option>") 
    }

    $('#new-pair').multiSelect('refresh')

}

function submitPairGroup(evt){

    var formInput = {
        "new_pair1": $("#new-pair").val()[0],
        "new_pair2": $("#new-pair").val()[1],
        "lab_id": $("#lab-id").val()
    }
    evt.preventDefault();
    $.post("/pair_students", formInput, showPairedStudents)
}


$("#new-pairs").on("submit", submitPairGroup)