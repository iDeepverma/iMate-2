// const roomName = JSON.parse(document.getElementById('room-name').textContent);

$(".messages").animate({scrollTop: $(document).height()}, "fast");


$(".expand-button").click(function () {
    $("#profile").toggleClass("expanded");
    $("#contacts").toggleClass("expanded");
});

function newMessage(msgType,message,whoDid) {
    // message = $(".message-input input").val();
    // if ($.trim(message) == '') {
    //     return false;
    // }
    $('<li class="'+msgType+'"><p>' + message + '</p></li>').appendTo($('.messages ul'));
    // $('.message-input input').val(null);
    // $('.contact.active .preview').html('<span>You: </span>' + message);
    if(whoDid==true){
        $('.contact.active .preview').html(message);
    }
    else{
        $('.contact.active .preview').html('<span>You: </span>'+message);
    }
    $(".messages").animate({scrollTop: $(document).height()}, "fast");
};

// $('.submit').click(function () {
//     newMessage();
// });

// $(window).on('keydown', function (e) {
//     if (e.which == 13) {
//         newMessage();
//         return false;
//     }
// });

function chatRedirect(current_frnd_username) {
    window.location.href = "/chat/" + current_frnd_username + "/";
}

//# sourceURL=pen.js



const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/'
    + window.location.pathname.match(/chat\/(.*)$/)[1]
);

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    // console.log(data);
    if(data.type.localeCompare("chat_message")==0){
        if(data.sender.localeCompare(chatData['frndUsername'])==0){
            newMessage('sent',data['message'],true)
        }
        else{
            newMessage('replies',data['message'],false)
        }
    }
    // else{
    //     // console.log(data);
    // }
};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};  

// document.querySelector('#chat-message-input').focus();
document.querySelector('.message-input input').onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('.submit').click();
    }
};

document.querySelector('.submit').onclick = function(e) {
    const messageInputDom = document.querySelector('.message-input input');
    const message = messageInputDom.value;
    chatSocket.send(JSON.stringify({
        'message': message
    }));
    messageInputDom.value = '';
};