/* ==============================================
 Back to Top
 =============================================== */

$(window).scroll(function(){
	if($(window).scrollTop() > 300){
		$("#back-to-top").fadeIn(600);
	} else{
		$("#back-to-top").fadeOut(600);
	}
});

$('#back-to-top, .back-to-top').click(function() {
	$('html, body').animate({ scrollTop:0 }, '1000');
	return false;
});
