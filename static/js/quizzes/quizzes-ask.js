$(document).ready(function () {
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

    $('.radio_answer').on('click', function (event) {
        data = JSON.stringify({
            'quizstatus_set': [{
                'quiz': event.target.attributes.for_quiz.value,
                'user_answer': event.target.value,
            }]
        })
        $.ajax({
            url: "/api/exam/update/",
            type: "PUT",
            data: data,
            contentType: 'application/json',
        });
    });

    $('.up-vote-btn').on('click', function (event) {
        quiz = event.target.attributes.for_quiz.value
        $.ajax({
            url: "/api/quiz/" + quiz + "/feed-back/",
            type: 'POST',
            data: {
                'feedback_type': 'up vote'
            },
            success: function () {
                $('#' + quiz + '-quiz-vote-status').html('quiz up voted !')
            }
        })
    });

    $('.down-vote-btn').on('click', function (event) {
        quiz = event.target.attributes.for_quiz.value
        $.ajax({
            url: "/api/quiz/" + quiz + "/feed-back/",
            type: 'POST',
            data: {
                'feedback_type': 'down vote'
            },
            success: function () {
                $('#' + quiz + '-quiz-vote-status').html('quiz down voted !')
            }
        })
    });
    $('#finish-btn').on('click', function (event) {
        $.ajax({
            url: '/api/exam/finish/', // this recognize exam automaticlly there is no need to send exam pk
            type: 'GET',
            success: function () {
                exam = event.target.attributes.for_exam.value
                location.replace('/quizzes/show_answer/' + exam + '/')
            }
        })

    });
});