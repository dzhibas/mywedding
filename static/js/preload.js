// plugin to preload images

/*
   demo code:
   $(['15.jpg', '0.jpg', '12.jpg', '18.jpg']).preload();
*/

(function($)
{
    $.fn.preload = function(path) {
        this.each(function()
        {
            var image_file = path + this;
            $('<img/>')[0].src = image_file;
        });
    };
})(jQuery);