/* Handles expandable elements */

$(document).ready(function() {
  $element = $('.expandable');
  $element.hide();
  $expandlink = $('<a class="expandlink">Expand</a>')
  $expandlink.insertAfter($element).click(function() {
    $element.fadeToggle('fast');
    if ($expandlink.text() == 'Expand') {
      $expandlink.text('Hide');
    } else {
      $expandlink.text('Expand');
    }
  });
});