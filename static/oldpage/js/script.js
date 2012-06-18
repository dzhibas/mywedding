$(function() {
	
	$.fn.preload = function() {
   		 this.each(function(){
	        $('<img/>')[0].src = this;
	    });
	}

	$(['imgs/simuka/15.jpg', 'imgs/simuka/0.jpg',
	   'imgs/simuka/12.jpg', 'imgs/simuka/18.jpg',
	   'imgs/simuka/21.jpg', 'imgs/simuka/13-30.jpg',
	   'imgs/simuka/16-30.jpg', 'imgs/simuka/19-30.jpg',
	   'imgs/simuka/22-30.jpg']).preload();
	
	var x=0, y=0;
	var pictureTop = 200, pictureLeft = 200,
		pictureWidht = 200, pictureHeight = 239;
	
	var picture2Left = 1140;

	var img = $("#simuka");
	var img2 = $("#simuka2");

	var images = ['12.jpg', '13-30.jpg', '...'];


	$(document).mousemove(function(event) {
		getMouseXY(event);
		// photo 1

		if (x > pictureLeft+pictureWidht && y > pictureTop && y < pictureTop + pictureHeight)
			$(img).attr('src', 'imgs/simuka/15.jpg');
		if (x > pictureLeft+pictureWidht && y < pictureTop)
			$(img).attr('src', 'imgs/simuka/13-30.jpg');
		if (x > pictureLeft && x < pictureLeft+pictureWidht && y > pictureTop && y < pictureTop+pictureHeight)
			$(img).attr('src', 'imgs/simuka/0.jpg');
		if (x > pictureLeft && x < pictureLeft+pictureWidht && y < pictureTop)
			$(img).attr('src', 'imgs/simuka/12.jpg');
		if (x > pictureLeft+pictureWidht && y > pictureTop+pictureHeight)
			$(img).attr('src', 'imgs/simuka/16-30.jpg');
		if (x > pictureLeft && x < pictureLeft+pictureWidht && y > pictureTop+pictureHeight)
			$(img).attr('src', 'imgs/simuka/18.jpg');
		if (x < pictureLeft && y > pictureTop+pictureHeight)
			$(img).attr('src', 'imgs/simuka/19-30.jpg');
		if (x < pictureLeft && y > pictureTop && y < pictureTop + pictureHeight)
			$(img).attr('src', 'imgs/simuka/21.jpg');
		if (x < pictureLeft && y < pictureTop)
			$(img).attr('src', 'imgs/simuka/22-30.jpg');


		// photo 2
		if (x > picture2Left+pictureWidht && y > pictureTop && y < pictureTop + pictureHeight)
			$(img2).attr('src', 'imgs/simuka/15.jpg');
		if (x > picture2Left+pictureWidht && y < pictureTop)
			$(img2).attr('src', 'imgs/simuka/13-30.jpg');
		if (x > picture2Left && x < picture2Left+pictureWidht && y > pictureTop && y < pictureTop+pictureHeight)
			$(img2).attr('src', 'imgs/simuka/0.jpg');
		if (x > picture2Left && x < picture2Left+pictureWidht && y < pictureTop)
			$(img2).attr('src', 'imgs/simuka/12.jpg');
		if (x > picture2Left+pictureWidht && y > pictureTop+pictureHeight)
			$(img2).attr('src', 'imgs/simuka/16-30.jpg');
		if (x > picture2Left && x < picture2Left+pictureWidht && y > pictureTop+pictureHeight)
			$(img2).attr('src', 'imgs/simuka/18.jpg');
		if (x < picture2Left && y > pictureTop+pictureHeight)
			$(img2).attr('src', 'imgs/simuka/19-30.jpg');
		if (x < picture2Left && y > pictureTop && y < pictureTop + pictureHeight)
			$(img2).attr('src', 'imgs/simuka/21.jpg');
		if (x < picture2Left && y < pictureTop)
			$(img2).attr('src', 'imgs/simuka/22-30.jpg');

		//	console.log(x,y);
	});	
function getMouseXY(e) // works on IE6,FF,Moz,Opera7
{
  if (!e) e = window.event; // works on IE, but not NS (we rely on NS passing us the event)

  if (e)
  {
    if (e.pageX || e.pageY)
    { // this doesn't work on IE6!! (works on FF,Moz,Opera7)
      x = e.pageX;
      y = e.pageY;
      algor = '[e.pageX]';
      if (e.clientX || e.clientY) algor += ' [e.clientX] '
    }
    else if (e.clientX || e.clientY)
    { // works on IE6,FF,Moz,Opera7
      x = e.clientX + document.body.scrollLeft;
      y = e.clientY + document.body.scrollTop;
      algor = '[e.clientX]';
      if (e.pageX || e.pageY) algor += ' [e.pageX] '
    }
  }
}

});
