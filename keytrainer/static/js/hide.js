$(function() {

    game_input_area = $('#game_input');
    game_input_area.prop("disabled", true);

    function hide_element() {
      $('#level_text').remove();
      game_input_area = $('#game_input');
      game_input_area.prop("disabled", false);
      game_input_area.focus();
    }

    var show_time_element = $('#show_time');
    var show_time = parseInt(show_time_element.text());
    setTimeout(hide_element, show_time*1000);

});