console.log('Стрипт странички создания игры успешно загружен');

document.getElementById('create-new-game').addEventListener('click', () => {
    console.log("Попытка создания игры засчитана")
    createNewGame();
});

function createNewGame() {
    const request = new XMLHttpRequest();
    request.open('GET', '/create_new_game');
    request.addEventListener('load', () => {
        if (request.status === 200) {
            if (request.response == "") {
                console.log("К нам пришла пустая строка");                
            } else {
                const response = JSON.parse(request.response);
                console.log(response);
                console.log("Ответ от js: Игра создалась");    
                // actualVar(response);
            };
        } else {
            console.log("Ответ от сервера не получен");
        }
    });
    request.send();

}