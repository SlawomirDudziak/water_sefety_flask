let nr = 0;
let fadeTime = 100;

function changeSlide(side) {
	hideSlide();
	if (side == "next") setTimeout("nextSlide()", fadeTime);
	if (side == "previous") setTimeout("previousSlide()", fadeTime);
}

function nextSlide() {
	nr++; if (nr > 13) nr = 0;
	let image = "<img src=\"/static/img/chart"+nr+".png\" />";
	document.getElementById('slider').innerHTML = image;
	console.log('next');
	$('#slider').fadeIn(fadeTime);
	console.log('fadeIn');
}

function previousSlide() {
	nr--; if (nr < 0) nr = 13;
	let image = "<img src=\"/static/img/chart"+nr+".png\" />";
	document.getElementById('slider').innerHTML = image;
	console.log('previous');
	$('#slider').fadeIn(fadeTime);
	console.log('fadeIn');
}

function hideSlide() {
	console.log('fadeOut');
	$('#slider').fadeOut(fadeTime);
}