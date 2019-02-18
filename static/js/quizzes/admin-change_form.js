(function($){
    $(document).ready(function() {
    newCount = 0;
    rowCount = 0;
    deleteBtn = '<input type="button" value="delete" />' 
    mainTable = '#answer-field-container'
    
    $('#addAnswerBtn').on('click',function(event){
        createRow(mainTable);
    });

    init();

    function init(){ 
        $.ajax({
            url:'/api/quiz/get/6/',
            type:'GET',
            success:function(data){
                data = data[0]
                for(answer in data['answer_set']){
                    createRow(content = data['answer_set'][answer]['content'] , 
                        is_correct_answer = data['answer_set'][answer]['is_correct_answer'])
                }
            }
        })
    }

    
    function createRow(content , is_correct_answer){
        rowCount++;
        newCount++;

        name = 'new-answer-'+String(newCount)
        tbx = '<textarea id="id-'+name+'" cols="100" name="'+name+'" is_correct_answer="'+is_correct_answer+'">'+content+'</textarea>';
        console.log(tbx)
        newrow = $('<div id="Answer-row-'+String(rowCount)+'">'+tbx+'</div>').appendTo(mainTable);
        $(deleteBtn).on('click',function(event){
			deleteRow(event.target);
		}).appendTo(newrow)
    }
    function deleteRow(row){
        row.parentNode.remove();
		rowCount--;
    }
	});
})(django.jQuery);
                                             
