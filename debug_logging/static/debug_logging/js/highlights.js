/* Handles highlights */

$(document).ready(function() {
  function highlight_results() {
    time = parseFloat($('#time-threshold').val());
    queries = parseInt($('#sql-threshold').val());
    
    $('.messages .row1').each(function() {
      if (parseFloat($('.response-time', this).text()) > time) {
        $(this).removeClass('priority-low');
        $(this).addClass('priority-veryhigh');
      } else {
        $(this).removeClass('priority-veryhigh');
        $(this).addClass('priority-low');
      }
      if (parseInt($('.num-queries', this).text()) > queries) {
        $('.num-queries', this).parent().addClass('warn');
      } else {
        $('.num-queries', this).parent().removeClass('warn');
      }
    });
  }
  
  $('#time-threshold').keyup(function() {
    clearTimeout(this.highlightTimer)
    this.highlightTimer = setTimeout(highlight_results, 250);
  });
  $('#sql-threshold').keyup(function() {
    clearTimeout(this.highlightTimer)
    this.highlightTimer = setTimeout(highlight_results, 250);
  });
  
  highlight_results();
});
