$(function() {
    //alert( "ready!" );
    label_text = $('#level_text');
    // Текст который нужно ввести
    text = label_text.text();
    var current_letter_index = 0;
    var current_letter = text[current_letter_index];
    //console.log(text);
    game_input_area = $('#game_input');
    game_input_area.focus();

    game_input_area.keypress(function(e) {
        var code = e.keyCode || e.which;
        letter = String.fromCharCode(code);
        if (letter != current_letter) {
            //console.log("Ошибка");
            //console.log("current_letter", current_letter);
            //console.log("letter", letter);
            location.reload();
        }
        else {
           current_letter_index += 1;
           current_letter = text[current_letter_index];
        }
    });
});