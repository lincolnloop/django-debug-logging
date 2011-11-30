/* Handles test run controls */

$(function() {
  $('#start-run').click(function() {
    
  });

  $(".select-all input").click(function(e) {
    var el = $(this);
    el.closest('table').find("input[name=run_id]").attr("checked", el.attr("checked"));
  });

  $("#runs-form").submit(function(e) {
    return window.confirm("Do you really want to delete all selected runs? This action cannot be undone");
  });
});