$(function() {
//Accordion click behavior
$('.title').on('click', function() {//Click on the title element
	var findElm = $(this).next(".box");//Get the area where the accordion will be played immediately after
	$(findElm).slideToggle();//Accordion up and down movement
	if($(this).hasClass('close')){//If the title element has the class name close
		$(this).removeClass('close');//Remove class name
	}else{
		$(this).addClass('close');//Add class name close
	}
});
	
});