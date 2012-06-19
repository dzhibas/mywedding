// plugin for rotating head

(function($)
    {
        var defaultSettings = {
            imagePath: 'images/',
            top: 0,
            left: 0,
            width: 200,
            height: 0
        };

        $.fn.rotatingHead = function(option, settings) {

            if(typeof option === 'object')
            {
                settings = option;
            } else if(typeof option == 'string') {

                var data = this.data('_rotatingHead');

                if(data) {

                    if(defaultSettings[option] !== undefined) {

                        if(settings !== undefined) {

                            if(option == 'title') {

                                data.content.html(settings);
                            }

                            data.settings[option] = settings;

                            return true;
                        }
                        else {

                            return data.settings[option];
                        }
                    }
                }

                return false;
            }

            settings = $.extend({}, defaultSettings, settings || {});

            // iterate through all elements and return them to maintain jQuery method chaining
            return this.each(function() {

                var elem = $(this);

                $settings = jQuery.extend(true, {}, settings);
                $settings.title = settings.title || elem.attr('title') || 'No title set';

                var rotatingHead = new RotatingHead(elem, $settings);

                rotatingHead.generate();

                elem.data('_rotatingHead', rotatingHead);
                $(document).mousemove(function(event) {
                    rotatingHead.mousemove(event);
                });
            });
        };

        function RotatingHead(element, settings)
        {
            this.element = element;
            this.image = null;
            this.rotatingHead = null;
            this.settings = settings;
            this.x = 0;
            this.y = 0;

            this.top = 0;
            this.left = 0;
            this.width = 0;
            this.height = 0;

            this.preloadImages();

            return this;
        }

        RotatingHead.prototype = {

            generate: function() {
                var $this = this;
                if($this.rotatingHead) {
                    return $this.rotatingHead;
                }
                this.image = $('<img/>', {
                        src: this.settings.imagePath + '0.jpg',
                        width: this.settings.width,
                        height: this.settings.height,
                        border: 0
                    });
                this.element.html(this.image);

                var pos = $(this.element).position();
                this.top = pos.top;
                this.left = pos.left;
                this.width = this.settings.width;
                this.height = $(this.image).height();
            },

            mousemove: function(event) {
                this.getMouseXY(event);
                
                if (this.height === 0)
                    this.height = $(this.image).height();

                if (this.x > this.left + this.width && this.y > this.top &&
                    this.y < this.top + this.height)
                    $(this.image).attr('src', this.settings.imagePath + '15.jpg');

                if (this.x > this.left+this.width && this.y < this.top)
                    $(this.image).attr('src', this.settings.imagePath + '13-30.jpg');

                if (this.x > this.left && this.x < this.left+this.width &&
                    this.y > this.top && this.y < this.top+this.height)
                    $(this.image).attr('src', this.settings.imagePath + '0.jpg');

                if (this.x > this.left && this.x < this.left+this.width &&
                    this.y < this.top)
                    $(this.image).attr('src', this.settings.imagePath + '12.jpg');

                if (this.x > this.left+this.width && this.y > this.top+this.height)
                    $(this.image).attr('src', this.settings.imagePath + '16-30.jpg');

                if (this.x > this.left && this.x < this.left+this.width &&
                    this.y > this.top+this.height)
                    $(this.image).attr('src', this.settings.imagePath + '18.jpg');

                if (this.x < this.left && this.y > this.top+this.height)
                    $(this.image).attr('src', this.settings.imagePath + '19-30.jpg');

                if (this.x < this.left && this.y > this.top && this.y < this.top + this.height)
                    $(this.image).attr('src', this.settings.imagePath + '21.jpg');

                if (this.x < this.left && this.y < this.top)
                    $(this.image).attr('src', this.settings.imagePath + '22-30.jpg');
            },

            preloadImages: function() {
                var path = this.settings.imagePath;
                var images = ['12.jpg', '13-30.jpg', '15.jpg', '16-30.jpg',
                        '18.jpg', '19-30.jpg', '21.jpg', '22-30.jpg',
                        '0.jpg'];
                $.each(images, function(i, v) {
                    $('<img/>')[0].src = path+v;
                });
            },

            // works on IE6,FF,Moz,Opera7
            getMouseXY: function(e) {
              if (!e) e = window.event; // works on IE, but not NS (we rely on NS passing us the event)

              if (e)
              {
                if (e.pageX || e.pageY)
                { // this doesn't work on IE6!! (works on FF,Moz,Opera7)
                  this.x = e.pageX;
                  this.y = e.pageY;
                }
                else if (e.clientX || e.clientY)
                { // works on IE6,FF,Moz,Opera7
                  this.x = e.clientX + document.body.scrollLeft;
                  this.y = e.clientY + document.body.scrollTop;
                }
              }
            }
        };

})(jQuery);