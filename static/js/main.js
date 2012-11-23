(function() {
    function template(id, json) {
        console.log(arguments);
        var func = Handlebars.compile($('#' + id).html());
        return func(json);
    }

    console.log('it works');
    var nav_template = 'nav-list-item-tmpl';
    var gallery_template = 'image-list-item-tmpl';


    window.NavListView = Backbone.View.extend({
        template: 'nav-list-item-tmpl',

        el: '#image_list',

        events: {
            'click li > a': 'show_images'
        },

        initialize: function() {
            var self = this;
            $.getJSON('/list', function(json) {
                self.data = json;
                self.render();
            });
        },

        show_images: function(e) {
            var dir = $.trim($(e.target).text());
            console.log('/list/' + dir);
            $.getJSON('/list/' + dir, function(json) {
                window.image_list.render(json);
            });
        },

        render: function() {
            this.$el.html(template(this.template, this.data));
        }

    });

    window.ImageList = Backbone.View.extend({
        template: 'image-list-item-tmpl',

        el: '#thumnails',

        initialize: function(json) {
            if(json) {
                this.render(json);
            }
        },

        render: function(json) {
            var self = this;
            this.$el.isotope('destroy');
            this.$el.html(template(this.template, json));

            var $srcs = this.$('a.thumbnail');
            var size = $srcs.size(), counter = 0;
            $srcs.each(function(index, elem) {
                var src = $(elem).attr('data-src');
                $('<img />')
                .load(function() {
                    counter++;
                    console.log(counter + '/' + size);
                    if(counter == size) {
                        self.$el.isotope();
                        self.$('.thumbnail').fancybox();
                    }
                })
                .attr('src', src)
                .appendTo($(elem));
            });
        }
    });

    window.nav = new NavListView();
    window.image_list = new ImageList();
})();
