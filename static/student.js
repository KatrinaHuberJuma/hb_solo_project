"use strict"

function showUpdates(results) {
    var bio = results.bio;
    var email = results.email;
    var demoVid = results.demoVid;
    var githubLink = results.githubLink;
    var profilePic = results.profilePic;

    if ($("#bio-content").html() !== bio) {
        $("#bio-title").html("New Bio")
        $("#bio-content").html(bio)
        $("#update-bio").val("")
    }

    if ($("#email-content").html() !== email) {
        $("#email-title").html("New Email")
        $("#email-content").html(email)
        $("#update-email").val("")
        $("#profile-pic").html("<img src=" + profilePic + "></div>") // TODO this doesn't work
    }

    if ($("#github-link-content").html() !== githubLink) {
        $("#github-link-title").html("<a  target='_blank' href='" + githubLink + "'>New Github Link</a>")

        $("#update-github-link").val("")
    }

    if ($("#demo-link-content").html() !== demoVid) {
        $("#demo-link-title").html("<a target='_blank' href='" + demoVid + "'>New Demo Video Link</a>")
        $("#update-demo-link").val("")
    }

}

function submitUpdates(evt) {

    var all_fields = []

    var newBioValue = $("#update-bio").val()
    if (newBioValue){
        all_fields.push({field: "bio", new_value: newBioValue});
    }
    

    var newGitValue = $("#update-github-link").val()
    if (newGitValue) {
        all_fields.push({field: "github_link", new_value: newGitValue})
    }

    var newDemoVidValue = $("#update-demo-link").val()
    if (newDemoVidValue) {
        all_fields.push({field: "demo_vid", new_value: newDemoVidValue})
    }


    var newEmail = $("#update-email").val()
    if (newEmail) {
        all_fields.push({field: "email", new_value: newEmail})
    }


    var newPassword = $("#update-password").val()
    if (newPassword) {
        all_fields.push({field: "password", new_value: newPassword})
    }


    var formInput = {all_fields: JSON.stringify(all_fields)}
    
    evt.preventDefault()
    $.post("/post_student_update", formInput, showUpdates)

}

$("#update-student-details").on("submit", submitUpdates);


////////////////////////////////////////////////////////////////////////////////

function showUpdatedNotes(results) {

    $("#submitted-notes").html(results.newNotes)
    console.log(results.newNotes)
}


function submitUpdatedNotes(evt) {
    var formInput = {
        "pair_notes": $("#update-notes").val(),
        "pair_id": $("#pair-id").val()
    }
    
    evt.preventDefault()
    $.post("/update-pair-notes", formInput, showUpdatedNotes)
}



$("#update-pair-notes").on("submit", submitUpdatedNotes);
