+function ($) {
  'use strict';

  var
    $footer = $('footer'),
    $footer_floatings = $('.footer-floating');

  $(window).scroll(function (){
    var
      footer_top = $footer.offset().top,
      footer_height = $footer.outerHeight(),
      scroll_top = $(this).scrollTop(),
      distance_bottom = scroll_top + $(this).height();

    $footer_floatings.each(function (){
      var
        $footer_floating = $(this),
        start_after = null,
        start_after_top = null;

      if($footer_floating.data('start-after') !== undefined){
        var $start_after = $($footer_floating.data('start-after'));

        start_after_top = $start_after.offset().top + $start_after.outerHeight();
        start_after = start_after_top + $footer_floating.outerHeight();

        $('footer').css('margin-top', ($footer_floating.outerHeight() + 20) + 'px');
      }

      if(distance_bottom > footer_top){
        $footer_floating.css('position', 'absolute');
        $footer_floating.css('bottom', footer_height + 'px');
        $footer_floating.css('top', 'auto');
      } else {
        if(start_after !== null && start_after > distance_bottom) {
          $footer_floating.css('position', 'absolute');
          $footer_floating.css('bottom', 'auto');
          $footer_floating.css('top', start_after_top + 'px');
        } else {
          $footer_floating.css('position', 'fixed');
          $footer_floating.css('bottom', '0');
          $footer_floating.css('top', 'auto');
        }
      }
    });
  }).scroll();
}(jQuery);
