"use strict"

function showNewCohort(results) {
    // display 

    var resultString = results.string
    var resultId = results.createdId

    $("#cohort-list").append("<li id='new-cohort'><a href='/cohort" + resultId +"'>" + resultString + "</a></li>")

    $("#enter-cohort-name").val("")
    $("#enter-cohort-password").val("")
}

function submitNewCohortInfo(evt) {
    // post form data to the add-cohort route

    var formInput = {
        "new_cohort_name": $("#enter-cohort-name").val(),
        "new_cohort_password": $("#enter-cohort-password").val()
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
