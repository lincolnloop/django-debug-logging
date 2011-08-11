/* Handles expandable elements */

$(function() {
  $('.expandable').each(function() {
    $(this).hide();
    $('<a class="expandlink button">Expand</a>').insertBefore(this).click(function() {
      $(this).next('.expandable').fadeToggle('fast');
      if ($(this).text() == 'Expand') {
        $(this).text('Hide');
      } else {
        $(this).text('Expand');
      }
    });
  });
});