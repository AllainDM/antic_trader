console.log('Стрипт странички выбора игры успешно загружен');

// Будущий список выбора игры
const chooseList = document.querySelector('.choose-list');

function requestStatus() {
    const request = new XMLHttpRequest();
    request.open('GET', '/load-all-my-game');
    request.addEventListener('load', () => {
        if (request.status === 200) {
            if (request.response == "") {
                console.log("К нам пришла пустая строка");
                
            } else {
                const response = JSON.parse(request.response);
                        // После обсчета хода игрок один раз получает сообщение, что пришел новый ход
                        // Баг!!! При сообщении о новом ходе все параметры висят по нулям
                        // По скольку это временный вариант, чинить не буду
                        // if (statusGame.year < response.year) {
                        //     // Обновим параметры на странице
                        //     actualVar(response);
                        //     alert(`Новый ход обработан. Текущий год: ${response.year}`);
                        // } else {
                        //     // Обновим параметры на странице
                        //     actualVar(response);
                        // }
                console.log(response);
                console.log("Ответ от сервера");
                chooseGame(response);
            };
        } else {
            console.log("Ответ от сервера не получен");
        }
    });
    request.send();

}

requestStatus();

function chooseGame(gamesList) {
    chooseList.innerHTML = `<span>Выберите игру:</span>`;  // Добавим подсказку
    gamesList.forEach((item, id) => {
        // chooseList.innerHTML += `<div class="menu-btn menu-buttons-choose"><a href="{{url_for('game')}}">Игра номер: ${item}</a></div>`;
        chooseList.innerHTML += `<div class="menu-btn menu-buttons-choose">Игра номер: ${item}</div>`;
    });

    // Определяем позицию кнопки и "создаем" соответсвующий приказ
    document.querySelectorAll(".menu-buttons-choose").forEach((btn, i) => {
        btn.addEventListener('click', () => {
            console.log(`Вы выбрали игру номер: ${gamesList[i]}`);
            setActiveGame(gamesList[i]); // Установить активную игру, ее данные будет отправлять бек при обновлении и загрузке новой страницы 
        });
    });
};

function setActiveGame(id){
    const req = new XMLHttpRequest();
    req.open("GET", `/set_active_game?id=${id}`);
    req.addEventListener('load', () => {
        console.log("Xmmm");
        window.location.href = 'game';
        // То что ниже в комментах оставим, интересно....
        // Если ответ есть, запустить функцию отображения
        // if (response) {
            // writeComment(response, id);
        // };
    });
    req.addEventListener('error', () => {
        console.log('error')
    });
    req.send();
}
