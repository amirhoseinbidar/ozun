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

    $('#submit').click(doUpdate);
    UpdateGradeList();
    UpdataProvinceList();


    $('#image-upload').on('change',function(){  
        formdata = new FormData();
        var file = this.files[0];
        if(formdata){
            formdata.append("username",  $('#username')[0].value );
            formdata.append("image",file);
            $.ajax({
                url : '/api/rest-auth/user/' , 
                type : 'PUT',
                data : formdata ,
                processData : false , 
                contentType : false ,
                success : function () {
                    doUpdate();
                    location.reload(true);
                }
            });
        }
    });
   
   
    
    function doUpdate(){     
        var grade = $('#grade-textbox')[0].value;
        interest_lesson = grade + '/' + $('#interest-lesson-textbox')[0].value;
        
        var location = $('#province-textbox')[0].value + '/' + $('#county-textbox')[0].value + '/' + $('#city-textbox')[0].value;
        var data = {
            'username' : $('#username')[0].value ,
            'first_name': $('#first-name')[0].value,
            'last_name' : $('#last-name')[0].value,
            'bio' : $('#bio')[0].value,
            'brith_day' : $('#brith-day')[0].value,
        }
        if (grade != "")
            data['grade'] = grade
        if (interest_lesson != ""  && interest_lesson != "/" )
            data['interest_lesson'] = interest_lesson
        if(location != ""  && location != "//" )
            data['location'] = location 

        $.ajax({
            url: '/api/rest-auth/user/',
            data: data,
            type: 'PUT',
            cache: false,
            success: function(data){
                $('#editing-succ-container').html('profile uploaded successfully')
            },
            error: function(e){
                $('#errors').html(e.message)
            }
        })
    }
    
   
    
    function UpdateGradeList(){
        $.ajax({
            url : '/api/lesson/children/root',
            type : 'get',
            success : function(data){
                embedDataListLesson('#grade-list',data)  ; 
            },
            error: function(e){
                console.log(e)
            }
        })
    }

    $('#grade-textbox').on('change',function(){
        grade = this.value
        if (grade == '')
            $('#interest-lesson-list').html('')
        else{
            grade = grade.replace(' ','-');
            $.ajax({
                url : '/api/lesson/children/'+grade ,
                type : 'get' ,
                success : function(data){
                    embedDataListLesson('#interest-lesson-list',data);
                },
                error: function(e){
                    console.log(e)
                }
            });
        }     
    });

    function UpdataProvinceList(){
        $.ajax({
            url : '/api/location/children/root',
            type : 'get',
            success : function(data){
                embedDataListLocation('#province-list',data)  ; 
            },
            error: function(e){
                console.log(e)
            }
        })
    }

    $('#province-textbox').on('change',function(){
        province = this.value
        if (province == '')
            $('#county-list').html('')
        else{
            province = province.replace(' ','-');
            $.ajax({
                url : '/api/location/children/'+province ,
                type : 'get' ,
                success : function(data){
                    embedDataListLocation('#county-list',data);
                },
                error: function(e){
                    console.log(e)
                }
            });
        }     
    });
    
    $('#county-textbox').on('change',function(){
        county = this.value
        if (county == '')
            $('#city-list').html('')
        else{
            county = county.replace(' ','-');
            province = $('#province-textbox')[0].value.replace(' ','-');
            $.ajax({
                url : '/api/location/children/'+province+'/'+county ,
                type : 'get' ,
                success : function(data){
                    embedDataListLocation('#city-list',data);
                },
                error: function(e){
                    console.log(e)
                }
            });
        }     
    });
    


    function embedDataListLocation(id , data){
        data = JSON.parse(data)['children'];
        dataStr = "";
        for (ele in data){
            dataStr += "<option value='"+data[ele]+"'>"+data[ele]+"</option>";
        }
        $(id).html(dataStr) ;
    }
    
    function embedDataListLesson(id , data){        
        dataStr = "";
        for (ele in data){
            dataStr += "<option value='"+data[ele]['content']['name']+"'></option>";
        }
        $(id).html(dataStr) ;
    }
    

});
