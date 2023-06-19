console.log("Скрипт чата успешно загружен");

const chatBox = document.querySelector(".chat");
const chatText = document.getElementById('chat-text');
const sendButton = document.getElementById('chat-send-text');
const inputText = document.getElementById('chat-input-text');

sendButton.addEventListener("click", () => {
    postMessage();
});

function postMessage() {
    const request = new XMLHttpRequest();
    request.open('POST', `/post_chat`);
    request.setRequestHeader('Content-type', 'application/json; charset=utf-8');

    console.log(JSON.stringify(inputText.value));
    request.send(JSON.stringify(inputText.value));

    request.addEventListener('load', () => {
        console.log("Автообновление");
        if (request.status === 200) {
            if (request.response == "") {
                console.log("К нам пришла пустая строка");
                
            } else {
                const response = JSON.parse(request.response);
                console.log(response);
                chatText.innerText = response;
            };
        } else {
            console.log("Ответ от сервера не получен");
        }

    });

};