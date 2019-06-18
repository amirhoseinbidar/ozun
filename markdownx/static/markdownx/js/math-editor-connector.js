$( function(){
    $('.markdownx-open-math-editor').on('click',function () {
        var inputer_id = $(this).attr('markdownx-inputer-id');
        openEditor(inputer_id);
    });
    
    function openEditor(textarea) {
        win = window.open(
            '/static/visual_math_editor/VisualMathEditor.html?runLocal&codeType=Latex&encloseAllFormula=false&textarea=' + textarea,
            'VisualMathEditor',
            'height=580,width=780,top=100,left=100,status=yes,toolbar=no,menubar=no,location=no,resizable=no,scrollbars=no,modal=no,dependable=yes'
        );
        win.focus();
    }

    //for handel markdownx preview refresh 
    $('.markdownx-editor').on('keyup'  , function(){
        MathJax.Hub.Queue(['Typeset',MathJax.Hub]);
    })
});


