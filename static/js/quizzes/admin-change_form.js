(function ($) {
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

        var js_src = '/static/markdownx/js/markdownx.js';

        function reload_markdownx_js() {
            $("script[src='" + js_src + "']").remove();
            $('head').append('<script type="text/javascript" src="' + js_src + '"></script>');
        }

        var newCount = 0;
        var rowCount = 0;
        var deleteBtn = '<input type="button" value="delete" />';
        var mainTable = '#answer-field-container';
        var quiz_data = [];
        var quiz_id = $('#quiz_id')[0].value;

        $('#addAnswerBtn').on('click', function (event) {
            createRow('');
            reload_markdownx_js();
        });

        init();

        function init() {
            $.ajax({
                url: '/api/quiz/get/' + quiz_id + '/',
                type: 'GET',
                success: function (data) {
                    quiz_data = data = data[0];
                    for (var answer in data.answer_set) {
                        createRow(content = data.answer_set[answer].content,
                            is_correct_answer = data.answer_set[answer].is_correct_answer);
                    }
                    reload_markdownx_js();
                    quiz_data.answer_set = [];
                    quiz_data.added_by = quiz_data.added_by.pk;
                    quiz_data.source = quiz_data.source.name;
                }
            });
        }



        function createRow(content, is_correct_answer) {
            rowCount++;
            newCount++;

            var name = 'new-answer-' + String(newCount);
            var cbx = '<input type="radio" name="is_correct_ansewer" class="correct_answer_rdbx" for_answer="id_' + name + '" '; // is correct box
            if (is_correct_answer)
                cbx += 'checked';
            cbx += '>';

            var editor = getEditor(name, content);

            newrow = $('<fieldset id="Answer-row-' + String(rowCount) + ' class="form-row field-answer" >' + cbx + editor + '</fieldset>').appendTo(mainTable);
            $(deleteBtn).on('click', function (event) {
                deleteRow(event.target);
            }).appendTo(newrow);

        }

        function getEditor(name, content) {
            editor = `<div class="markdownx"><textarea name="` + name + `" cols="40" rows="10" required id="id_` + name + `"
        class="markdownx-editor markdownx-editor answer_editor" data-markdownx-editor-resizable
        data-markdownx-urls-path="/markdownx/markdownify/" 
        data-markdownx-upload-urls-path="/markdownx/upload/" data-markdownx-latency="500" 
        style="transition: opacity 1s ease 0s;">` + content + `</textarea> 
        <input type="button" value="open in math editor" class="markdownx-open-math-editor" markdownx-inputer-id="id_` + name + `">
        <div class="markdownx-preview"></div></div>`;
            return editor;
        }

        $('input[name="_save"] , input[name="_addanother"] , input[name="_continue"]').on('click', function () {
            answers = $('.correct_answer_rdbx');
            quiz_data.answer_set = []; //empty answers list and recollect answers 

            for (i = 0; i < answers.length; i++) {
                is_correct = answers[i].checked;
                answer = $('#' + answers[i].attributes.for_answer.value)[0];

                quiz_data.answer_set.push({
                    'is_correct_answer': is_correct,
                    'content': answer.value
                });
            }

            $.ajax({
                url: '/api/quiz-manage/update/' + quiz_data.id + '/',
                type: 'PUT',
                cache: false,
                contentType: 'application/json',
                data: JSON.stringify(quiz_data),
                success: function () {
                    console.log('answers updated');
                }
            });
        });

        function deleteRow(row) {
            row.parentNode.remove();
            rowCount--;
        }
    });
})(django.jQuery);