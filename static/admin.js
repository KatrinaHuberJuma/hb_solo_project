"use strict"

function showNewCohort(results) {
    // display 

    var resultString = results.string
    var resultId = results.createdId

    $("#cohort-list").append("<li id='new-cohort'><a href='" + resultId + "'>" + resultString + "</a></li>")

    $("#enter-cohort-name").val("")
    $("#enter-cohort-password").val("")
}

function submitNewCohortInfo(evt) {
    // post form data to the add-cohort route

    var formInput = {
        "new-cohort-name": $("#enter-cohort-name").val(),
        "new-cohort-password": $("#enter-cohort-password").val()
    }
    evt.preventDefault();
    $.post("/add-cohort", formInput, showNewCohort);
}

$('#create-cohort').on('submit', submitNewCohortInfo)