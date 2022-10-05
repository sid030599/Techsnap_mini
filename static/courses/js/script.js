// Owlcarousel
$(document).ready(function(){
    $(".owl-carousel").owlCarousel({
        loop:true,
        responsiveClass: true,
      margin:10,
      nav:true,
      autoplay:false,
      autoplayTimeout:3000,
      autoplayHoverPause:true,
      center: true,
      navText: [
          "<i class='fa fa-angle-left'></i>",
          "<i class='fa fa-angle-right'></i>"
      ],
      responsive:{
          0:{
              items:1
          },
          600:{
              items:3
          },
          1200:{
              items:3
          }
      }
    });
  });

  $(document).ready(function() {
    $(".active-nav li a").on('click', function(e) {
        e.preventDefault()
        var page = $(this).data('page');
        $("#pages .page:not('hide')").stop().fadeOut('fast', function() {
            $(this).addClass('hide');
            $('#pages .page[data-page="'+page+'"]').fadeIn('slow').removeClass('hide');
        });
    });
});
$(document).ready(function() {
    $(".top-bar li a").on('click', function(e) {
        e.preventDefault()
        var page = $(this).data('page');
        $("#page01 .pages:not('hide')").stop().fadeOut('fast', function() {
            $(this).addClass('hide');
            $('#page01 .pages[data-page="'+page+'"]').fadeIn('slow').removeClass('hide');
        });
    });
});
  