/* Handles expandable elements */

$(document).ready(function() {
  $('.expandable').each(function() {
    $(this).hide();
    $('<a class="expandlink">Expand</a>').insertBefore(this).click(function() {
      $(this).next('.expandable').fadeToggle('fast');
      if ($(this).text() == 'Expand') {
        $(this).text('Hide');
      } else {
        $(this).text('Expand');
      }
    });
  });
});