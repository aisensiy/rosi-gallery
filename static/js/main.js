(function() {
    function template(id, json) {
        console.log(arguments);
        var func = Handlebars.compile($('#' + id).html());
        return func(json);
    }

    console.log('it works');
    var nav_template = 'nav-list-item-tmpl';
    var gallery_template = 'image-list-item-tmpl';

    window.TotalApp = Backbone.View.extend({
        el: 'body',

        events: {
            'click .navbar ul.nav > li': 'active_toggle',
            'click #popular': 'get_popular'
        },

        initialize: function() {
            this.$nav_links = this.$('ul.nav > li');
        },

        get_popular: function(e) {
            e && e.preventDefault();
            nav.$el.parent().hide();
            image_list.$el.parent().removeClass('span9').addClass('span12');
            $.getJSON('/popular', function(json) {
                window.image_list.render(json);
            });

            e && app.navigate('top', false);
        },

        active_toggle: function(e) {
            console.log(e);
            $self = $(e.target).parent();
            this.$nav_links.removeClass('active');
            $self.addClass('active');
        }
    });

    window.NavListView = Backbone.View.extend({
        template: 'nav-list-item-tmpl',

        el: '#image_list',

        events: {
            'click li > a': 'click_show_images'
        },

        initialize: function() {
            var self = this;
            $.getJSON('/list', function(json) {
                self.data = json;
                self.render();
                if(!self.init_load) {
                    self.$el.children().first().find('a').click();
                    self.init_load = true;
                }
            });
        },

        click_show_images: function(e) {
            e.preventDefault();
            console.log('prevent!');
            var dir = $.trim($(e.target).text());
            app.navigate('gallery/' + dir, false);
            this.show_images(dir);
        },

        show_images: function(dir) {
            window.scrollTo(0);
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
            if(this.$el.children().length)
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
                        self.$('.thumbnail').fancybox({
                            'preload': false
                        });
                    }
                })
                .attr('src', src)
                .appendTo($(elem));
            });
        }
    });

    var AppRouter = Backbone.Router.extend({
        routes: {
            "": "gallery",
            "gallery/:dir": "single_gallery",
            "top": "popular"
        },

        initialize: function() {
            window.totalapp = new TotalApp();
            window.nav = new NavListView();
            window.image_list = new ImageList();
        },

        gallery: function() {

        },

        single_gallery: function(dir) {
            nav.show_images(dir);
        },

        popular: function() {
            totalapp.get_popular();
        }
    });
    
    var app = new AppRouter();
    Backbone.history.start();
})();
