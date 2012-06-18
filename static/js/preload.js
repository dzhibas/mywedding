// plugin to preload images

/*
   demo code:
   $(['15.jpg', '0.jpg', '12.jpg', '18.jpg']).preload();
*/

(function($)
{
    $.fn.preload = function() {
        this.each(function()
        {
            $('<img/>')[0].src = this;
        });
    };
})(jQuery);