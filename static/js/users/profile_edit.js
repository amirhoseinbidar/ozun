$(function(){
    function getCookie(name) {
        // Function to get any cookie available in the session.
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function csrfSafeMethod(method) {
        // These HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    var csrftoken = getCookie('csrftoken');
    // This sets up every ajax call with proper headers.
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $.noConflict();
    formdata = new FormData();

    $('#image').on('change',function(){
        var file = this.files[0];
        if(formdata){
            formdata.append("username", $('#username').value );
            formdata.append("image",file);
            $.ajax({
                url : '/api/res-auth/user/' , 
                type : 'POST',
                data : formdata ,
                processData : false , 
                contentType : false ,
                sucess : function () {
                    doUpdate();
                    location.reload(true);
                }
            });
        }
    });
   
    $('#submit').click(doUpdate);
    
    function doUpdate(){     
        var grade = $('#grade').value;
        var interest_lesson = grade + '/' + $('#interest-lesson').value;
        var location = $('#location-province').value + '/' + $('#location-county').value + '/' + $('#location-city').value;
        $.ajax({
            url: '/api/res-auth/user/',
            data:{
                'username' : $('#username').value ,
                'first_name': $('#first-name').value,
                'last_name' : $('#last-name').value,
                'bio' : $('#bio').value,
                'brith-day' : $('#brith-day').value,
                'grade' : grade,
                'interest_lesson' : interest_lesson,
                'location' : location
            },
            type: 'post',
            cache: false,
            success: function(data){
                // create a message in #succ-containter
            },
            error: function(e){
                // create a message in #error
            }
        })
    }

});
