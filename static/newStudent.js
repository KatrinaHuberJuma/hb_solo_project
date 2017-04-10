"use strict"

function showNewStudent(results) {
    // display 

    var resultString = results.string
    var resultId = results.createdId

    $("#student-list").append("<li><a id='new-student' href='/" + resultId + "-profile'>" + resultString + "</a></li>")

}

function submitNewStudentInfo(evt) {
    // post form data to the add-cohort route

    var formInput = {
        "new_student_name": $("#enter-student-name").val(),
        "new_student_password": $("#enter-student-password").val(),
        "new_student_email": $("#enter-student-email").val(),
        "cohort_password": $("#enter-this-cohort-password").val()
    }
    evt.preventDefault();
    $.post("/signup-student", formInput, showNewStudent);
}

$('#join-cohort').on('submit', submitNewStudentInfo)