$(function() {
//accordion
$('.title').on('click', function() {
	var findElm = $(this).next(".box");
	$(findElm).slideToggle();
	if($(this).hasClass('close')){
		$(this).removeClass('close');
	}else{
		$(this).addClass('close');
	}
});
	
//Master the header height and lower the content
	$(window).resize(function()
	{
	var height = $(".site-header").height();
	$("body").css("margin-top", height);
	});
	var height = $(".site-header").height();
	$("body").css("margin-top", height);
	
});