+function ($) {
  'use strict';

  $(window).scroll(function (e){
    var
      $footer = $('footer'),
      $footer_floating = $('.footer-floating'),
      footer_top = $footer.offset().top,
      footer_height = $footer.innerHeight(),
      distance_footer = $(this).scrollTop() + $(this).height();

    if(distance_footer > footer_top){
      $footer_floating.css('position', 'absolute');
      $footer_floating.css('bottom', footer_height + 'px');
    } else {
      $footer_floating.css('position', 'fixed');
      $footer_floating.css('bottom', '0');
    }
  });
}(jQuery);
