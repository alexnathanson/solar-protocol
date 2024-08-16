/*
Custom off-cavas menu for Panke
 */

(function ($) {

    var menu_active = false;
//    var active_color;

    // ==================================================  Functions for mobile menu

    function toggleIconClass() {
        if (menu_active === true) {
            $(".container").removeClass("glyphicon-menu-hamburger");
            $(".menu-icon").addClass("glyphicon-remove");
        } else {
            $(".menu-icon").addClass("glyphicon-menu-hamburger");
            $(".menu-icon").removeClass("glyphicon-remove");
        }
    }


    function toggleMenu() {
        if (menu_active === false) {
            menu_active = true;
        } else {
            menu_active = false;
        }

        $(".off-canvas").toggleClass("menu-active");
        $(".container").toggleClass("menu-active");

        toggleIconClass();
    }

    function enableOffCanvas() {

        $('.toggle-menu').click(function () {
            toggleMenu();
        });

        if (menu_active === true) {
            $('.container').click(function () {
                toggleMenu();
            });
        }
    }

    // ==================================================  Functions for theme colour

//    function swapThemeColor() {
//        $(".container").removeClass(function (index, css) {
//            return (css.match(/(^|\s)theme-\S+/g) || []).join(' ');
//        });
//
//        $('.container').addClass('theme-' + active_color);
//        Cookies.set('active_color', active_color);
//    }
//
//    function readColorCookie() {
//
//        active_color = Cookies.get('active_color');
//        // prompt('Farbe ausgewählt zu ' + active_color);
//        if (active_color!='undefined')
//            swapThemeColor();
//
//    }
//
//    function enableColorSwap() {
//
//        $('#color-swap ').children('div').click(function () {
//            active_color = $(this).attr('class');
//            // prompt('Farbe ausgewählt zu ' + active_color);
//            swapThemeColor();
//        });
//
//    }

    $(document).ready(function () {

        enableOffCanvas();
//        readColorCookie();
//        enableColorSwap();

    });

})(jQuery);


