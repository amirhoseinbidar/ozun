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

    UpdataSource()
    UpdateGradeList()

    function UpdataSource(){  
        $.ajax({
            url : '/api/sources/' , 
            type : 'get',
            success : function (data){
                dataStr = "";
                for (ele in data)
                    dataStr += "<option value='"+data[ele]['name']+"'>"+data[ele]['name']+"</option>";
                $('#source-list').html(dataStr) ;
            }
        });  
    };

    function UpdateGradeList(){
        $.ajax({
            url : '/api/lesson/children/root',
            type : 'get',
            success : function(data){
                embedDataList('#grade-list',data)  ; 
            },
            error: function(e){
                console.log(e)
            }
        })
    }

    $('#grade-txt').on('change',function(){
        grade = this.value
        if (grade == '')
            $('#lesson-list').html('')
        else{
            grade = grade.replace(' ','-');
            $.ajax({
                url : '/api/lesson/children/'+grade ,
                type : 'get' ,
                success : function(data){
                    embedDataList('#lesson-list',data);
                },
                error: function(e){
                    console.log(e)
                }
            });
        }     
    });

    
    $('#lesson-txt').on('change',function(){
        lesson = this.value
        if (lesson == '')
            $('#chapter-list').html('')
        else{
            lesson = lesson.replace(' ','-');
            grade = $('#grade-txt')[0].value;
            $.ajax({
                url : '/api/lesson/children/'+grade+'/'+lesson ,
                type : 'get' ,
                success : function(data){
                    embedDataList('#chapter-list',data);
                },
                error: function(e){
                    console.log(e)
                }
            });
        }     
    });

        
    $('#chapter-txt').on('change',function(){
        chapter = this.value
        if (chapter == '')
            $('#topic-list').html('')
        else{
            chapter = chapter.replace(' ','-');
            grade = $('#grade-txt')[0].value;
            lesson = $('#lesson-txt')[0].value;
            $.ajax({
                url : '/api/lesson/children/'+grade+'/'+lesson+'/'+chapter ,
                type : 'get' ,
                success : function(data){
                    embedDataList('#topic-list',data);
                },
                error: function(e){
                    console.log(e)
                }
            });
        }     
    });


    function embedDataList(id , data){
        data = JSON.parse(data)['children'];
        dataStr = "";
        for (ele in data){
            dataStr += "<option value='"+data[ele]+"'>"+data[ele]+"</option>";
        }
        $(id).html(dataStr) ;
    }

});
