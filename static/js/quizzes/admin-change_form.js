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
		console.log(answersJson)
		if (answersJson.length== 0)
			createRow(mainTable);
        
        for(var i in answersJson){
			name = 'answer-'+String(i.pk)
			tbx = '<textarea id="pk-'+name+'" name="'+name+'" cols="100">'+i.text+'</textarea>';
			val = '{ "is_new":False , "connect_to":'+name+' , "pk":'+String(i.pk)+' }'
			hidden = '<input type="hidden" name="answer-info-'+String(newCount)+'" value="'+val+'" >' ;
            newCount++;
            createRow(mainTable ,tbx+hidden);
        }
    }

    
    function createRow(table , inner = ''){
        if(inner == ''){
			name = 'new-answer-'+String(newCount)
            tbx = '<textarea id="id-'+name+'" cols="100" name='+name+'"></textarea>';
            val = '{ "is_new":True , "connect_to":'+name+' }'
            hidden = '<input type="hidden" name="answer-info-'+newCount+'" value="'+val+'" >' ;
            inner = tbx+hidden;
        }
        rowCount++;
        newCount++;
        
        newrow = $('<div id="Answer-row-'+String(rowCount)+'"></div>').appendTo(table);
        newrow.append(inner);
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
                                             
