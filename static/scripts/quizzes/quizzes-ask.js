$(document).ready(function(){
    $('.radio_quiz').on('click',function(event){ 
        send_quiz_data($('#id_temporary_token').val(), event.target)
    });

    function send_quiz_data(token,element) {
        console.log("start sending data from"+element.id); // sanity check
        $.ajax({
            url : "/quizzes/update_token/", // the endpoint
            type : "POST", // http method
            data : { data : element.value ,
                    csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
                    token: token }, // data sent with the post request

            // handle a successful response
            success : function(json) {
                console.log(json); // log the returned json to the console
                console.log("success"); // another sanity check
            },

            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                console.log("error message: "+errmsg+"\n"+xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    } 
});