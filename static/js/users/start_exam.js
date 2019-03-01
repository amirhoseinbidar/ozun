$(function () {
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
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    UpdataSource();
    UpdateGradeList();

    function UpdataSource() {
        $.ajax({
            url: '/api/sources/',
            type: 'get',
            success: function (data) {
                dataStr = "";
                for (var ele in data)
                    dataStr += "<option value='" + data[ele].name + "'>" + data[ele].name + "</option>";
                $('#source-list').html(dataStr);
            }
        });
    }

    function UpdateGradeList() {
        $.ajax({
            url: '/api/lesson/children/root',
            type: 'get',
            async: false,
            success: function (data) {
                embedDataListLesson('#grade-list', data);
            },
            error: function (e) {
                console.log(e);
            }
        });
    }

    $('#id_grade').on('change', function () {
        grade = getSlug(this.value); //find grade slug
        console.log(grade)
        if (grade == '')
            $('#lesson-list').html('');
        else {
            $.ajax({
                url: '/api/lesson/children/' + grade,
                type: 'get',
                async: false,
                success: function (data) {
                    embedDataListLesson('#lesson-list', data);
                },
                error: function (e) {
                    console.log(e);
                }
            });
        }
    });


    $('#id_lesson').on('change', function () {
        lesson = getSlug(this.value); //find grade slug
        if (lesson == '')
            $('#chapter-list').html('');
        else {
            grade = getSlug($('#id_grade')[0].value);
            $.ajax({
                url: '/api/lesson/children/' + grade + '/' + lesson,
                type: 'get',
                async: false,
                success: function (data) {
                    embedDataListLesson('#chapter-list', data);
                },
                error: function (e) {
                    console.log(e);
                }
            });
        }
    });


    $('#id_chapter').on('change', function () {
        chapter = getSlug(this.value);
        if (chapter == '')
            $('#topic-list').html('');
        else {
            grade = getSlug($('#id_grade')[0].value);
            lesson = getSlug($('#id_lesson')[0].value);
            
            $.ajax({
                url: '/api/lesson/children/' + grade + '/' + lesson + '/' + chapter,
                type: 'get',
                async: false,
                success: function (data) {
                    embedDataListLesson('#topic-list', data);
                },
                error: function (e) {
                    console.log(e);
                }
            });
        }
    });

    function getSlug(name){
        return  $("option[value='"+name+"']")[0].attributes.slug.value; //find grade slug
    }
    function embedDataListLesson(id, data) {
        dataStr = "";
        for (var ele in data) {
            dataStr += "<option value='" + data[ele].content.name + "' slug='"+data[ele].content.slug+"''></option>";
        }
        $(id).html(dataStr);
    }
});