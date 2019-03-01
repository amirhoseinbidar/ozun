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



    $('#submit').click(doUpdate);
    UpdateGradeList();
    UpdataProvinceList();
    if ($('#id_grade')[0].value != '')
        updateLesson();
    if ($('#id_province')[0].value != '')
        updateCounty();
    if ($('#id_county')[0].value != '')
        updateCity();

    $('#id_image').on('change', function () {
        formdata = new FormData();
        var file = this.files[0];
        if (formdata) {
            formdata.append("username", $('#username')[0].value);
            formdata.append("image", file);
            $.ajax({
                url: '/api/rest-auth/user/',
                type: 'PUT',
                data: formdata,
                processData: false,
                contentType: false,
                success: function () {
                    doUpdate();
                    location.reload(true);
                }
            });
        }
    });



    function doUpdate() {
        var grade = $('#id_grade')[0].value;
        interest_lesson = grade + '/' + $('#id_interest_lesson')[0].value;

        var location = $('#id_province')[0].value + '/' + $('#id_county')[0].value + '/' + $('#id_city')[0].value;
        var data = {
            'username': $('#username')[0].value,
            'first_name': $('#id_first_name')[0].value,
            'last_name': $('#id_last_name')[0].value,
            'bio': $('#id_bio')[0].value,
            'brith_day': $('#id_brith_day')[0].value,
        };
       
        if (grade != "")
            data.grade = grade;
        if (interest_lesson != "" && interest_lesson != "/")
            data.interest_lesson = interest_lesson;
        if (location != "" && location != "//")
            data.location = location;
        $.ajax({
            url: '/api/rest-auth/user/',
            data: data,
            type: 'PUT',
            cache: false,
            success: function (data) {
                $('#editing-succ-container').html('profile uploaded successfully');
            },
            error: function (e) {
                $('#errors').html(e.message);
            }
        });
    }



    function UpdateGradeList() {
        $.ajax({
            url: '/api/lesson/children/root',
            type: 'get',
            async : false ,
            success: function (data) {
                embedDataListLesson('#grade-list', data);
            },
            error: function (e) {
                console.log(e);
            }
        });
    }

    $('#id_grade').on('change', updateLesson);
    function updateLesson() {
        grade_val = $('#id_grade')[0].value;
        grade = $("option[value='"+grade_val+"']")[0].attributes.slug.value;

        if (grade == '')
            $('#interest_lesson-list').html('');
        else {
            $.ajax({
                url: '/api/lesson/children/' + grade,
                type: 'get',
                async : false ,
                success: function (data) {
                    embedDataListLesson('#interest_lesson-list', data);
                },
                error: function (e) {
                    console.log(e);
                }
            });
        }
    }

    function UpdataProvinceList() {
        $.ajax({
            url: '/api/location/children/root',
            type: 'get',
            success: function (data) {
                embedDataListLocation('#province-list', data);
            },
            error: function (e) {
                console.log(e);
            }
        });
    }

    $('#id_province').on('change', updateCounty);
    function updateCounty() {
        province = $('#id_province')[0].value;

        if (province == '')
            $('#county-list').html('');
        else {
            province = province.replace(' ', '-');
            $.ajax({
                url: '/api/location/children/' + province,
                type: 'get',
                success: function (data) {
                    embedDataListLocation('#county-list', data);
                },
                error: function (e) {
                    console.log(e);
                }
            });
        }
    }
    
    $('#id_county').on('change', updateCity);
    function updateCity() {
        county = $('#id_county')[0].value;
        if (county == '')
            $('#city-list').html('');
        else {
            county = county.replace(' ', '-');
            province = $('#id_province')[0].value.replace(' ', '-');
            $.ajax({
                url: '/api/location/children/' + province + '/' + county,
                type: 'get',
                success: function (data) {
                    embedDataListLocation('#city-list', data);
                },
                error: function (e) {
                    console.log(e);
                }
            });
        }
    }


    function embedDataListLocation(id, data) {
        data = JSON.parse(data).children;
        dataStr = "";
        for (var ele in data) {
            dataStr += "<option value='" + data[ele] + "'>" + data[ele] + "</option>";
        }
        $(id).html(dataStr);
    }

    function embedDataListLesson(id, data) {
        dataStr = "";
        for (var ele in data) {
            dataStr += "<option value='" + data[ele].content.name + "' slug='"+data[ele].content.slug +"'></option>";
        }
        $(id).html(dataStr);
    }


});