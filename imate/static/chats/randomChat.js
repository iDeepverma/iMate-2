// const roomName = JSON.parse(document.getElementById('room-name').textContent);

$(".messages").animate({scrollTop: $(document).height()}, "fast");


$(".expand-button").click(function () {
    $("#profile").toggleClass("expanded");
    $("#contacts").toggleClass("expanded");
});

function newMessage(msgType,message,whoDid) {
    // message = $(".message-input input").val();
    if ($.trim(message) == '') {
        return false;
    }
    $('<li class="'+msgType+'"><p>' + message + '</p></li>').appendTo($('.messages ul'));
    // $('.message-input input').val(null);
    // $('.contact.active .preview').html('<span>You: </span>' + message);
    if(whoDid==true){
        $('.contact.active .preview').html(message);
    }
    else{
        $('.contact.active .preview').html('<span>You: </span>'+message);
    }
    $(".messages").animate({scrollTop: $('.messages').scrollHeight()}, "fast");
};

function endChat(offline){
    //called when user gets offline or when chat timer expires  
    const inputBox = document.querySelector("#msg-input-box");
    inputBox.disabled=true;
    inputBox.placeholder = "Chat Ended";
    inputBox.style.textAlign = 'center';
}


const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/randomChat/'
    // + window.location.pathname.match(/chat\/(.*)$/)[1]
);

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    console.log(data);
    if(data.type.localeCompare("chat_message")==0){
        if(data.sender.localeCompare('notme')==0){
            newMessage('sent',data['message'],true)
        }
        else{
            newMessage('replies',data['message'],false)
        }
    }
    else if(data.type.localeCompare("end_chat")==0){
        endChat();
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
    if ($.trim(message) == '') {
        console.log('empty')
    }
    else{
    chatSocket.send(JSON.stringify({
        'message': message
    }));
    messageInputDom.value = '';
}};


function addFriend(){
    chatSocket.send(JSON.stringify({
        'signal':'add_friend'
    }))
    const addFriendBtnDOM = document.querySelector('#addFriend-button');
    addFriendBtnDOM.disabled = true;
}