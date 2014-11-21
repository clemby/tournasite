$(function(){
  $('ul.navbar-nav').find('li>a').each(function(i, e) {
    var $e = $(e),
        $p = $e.parent();

    if ($e.attr('href') === location.pathname) {
      $p.addClass('active');
      return false;
    }
  });
});
