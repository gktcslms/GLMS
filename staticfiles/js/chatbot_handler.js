$(function() {
    $('#chat_input').on('keypress', function(event) {
        if (event.which == 13 && $(this).val().trim().length > 0){
            event.preventDefault();
            var message = $(this).val().replace(/(\r\n\t|\n|\r\t)/gm,"");
            $(this).val("");
            chat_add_user_message(message, true);
        }
    });

    function chat_add_user_message(message) {
        var html = '<div class="chat self">' +
            '<div class="user-photo"></div>' +
            '<p class="chat-message" style="text-align:right";>' +
                message +
            '</p>' +
        '</div>';
        chat_add_html(html);
        chat_scrolldown();
        get_chatbot_response(message);
    }

    function chat_add_bot_message(message) {
        console.log("Bot Messaging Block Called;");
        console.log(message);
        var html = '<div class="chat friend">' +
            '<div class="user-photo"></div>' +
            '<p class="chat-message">' +
                message +
            '</p>' +
        '</div>';
        chat_add_html(html);
        chat_scrolldown();
    }

    function chat_add_html(html) {
        $(".chatlogs").append(html);
    }

    function chat_scrolldown() {
        $(".chatlogs").animate({ scrollTop: $(".chatlogs")[0].scrollHeight }, 500);
    }

    function get_chatbot_response(message){
        console.log(message);
        $.ajax({
            url: '/ajax_chat/',
            data: {
              'message': message
            },
            dataType: 'json',
            success: function (data) {
                console.log(data.bot_respnse);
                var message = data.bot_respnse;
                chat_add_bot_message(message);
            },
            error: function (data) {
                console.log(data);
                var message = "Oops! Something went wrong.";
                chat_add_bot_message(message);
            }
        });
    }
});
