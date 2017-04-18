"use strict"

////////////////////////////////////////////////////////////////////////////////
// FOR ADDING A KEYWORD TO A LAB
////////////////////////////////////////////////////////////////////////////////
function showNewKeyword(results) {

    for (var i = 0; i < results.length; i++) {
        $("#related-keywords").append("<li>" + results[i] + "</li>")
    }

    $("#enter-new-keywords").val("")
}

function submitNewKeyword(evt) {

    var formInput ={
        "new_keywords": $("#enter-new-keywords").val(),
        "lab_id_for_keyword": $("#enter-lab-id").val()
    }

    evt.preventDefault();
    $.post("/add_keyword", formInput, showNewKeyword);
}

$("#add-keyword").on("submit", submitNewKeyword)


////////////////////////////////////////////////////////////////////////////////
// FOR SELECTING A KEYWORD TO VIEW ITS RELATED LABS
////////////////////////////////////////////////////////////////////////////////

function showRelatedLabs(results) {

    if ($("#labs-of-" + results[0].keyword_id).html() === " "){
        for (var i = 0; i < results.length; i++){
            $("#labs-of-" + results[i].keyword_id).append("<li><a href='/lab/" + 
                                                        results[i].lab_id + 
                                                        "'>" + 
                                                        results[i].lab_title + 
                                                        "</a></li>")
        }
    } else {
        $("#labs-of-" + results[0].keyword_id).slideToggle()
    }

}

function submitKeywordId(evt) {

    

    if ($("#labs-of-" + $(this) === " ")){

        var keywordId = $(this).val();
        var formInput ={
            "keyword_id": keywordId
        }

        evt.preventDefault();
        $.post("/show_related_labs", formInput, showRelatedLabs);

    } else {

        $(this).slideToggle();
    }
}

$("#keyword-list li button").click(submitKeywordId)