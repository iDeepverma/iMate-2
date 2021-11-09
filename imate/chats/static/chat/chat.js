// const roomName = JSON.parse(document.getElementById('room-name').textContent);

const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/'
    + window.location.pathname.match(/chat\/(.*)$/)[1]
);

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    console.log(data);
    if(data.type.localeCompare("chat_message")==0){
        document.querySelector('#chat-log').value += (data.message + '\n');
    }
    else{
        console.log(data);
    }
};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};  

document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('#chat-message-submit').click();
    }
};

document.querySelector('#chat-message-submit').onclick = function(e) {
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;
    chatSocket.send(JSON.stringify({
        'message': message
    }));
    messageInputDom.value = '';
};