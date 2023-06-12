console.log('Стрипт админской странички списка игр успешно загружен');


// Меню для вывода инфы по играм
const chooseList = document.querySelector('.choose-list');


// Запрос статуса для отображения выбора игры
function requestStatus() {
    const request = new XMLHttpRequest();
    request.open('GET', '/load_all_games');
    request.addEventListener('load', () => {
        if (request.status === 200) {
            if (request.response == "") {
                console.log("К нам пришла пустая строка");
                
            } else {
                const response = JSON.parse(request.response);
                console.log(response);
                console.log("Ответ от сервера");
                chooseGame(response);
            };
        } else {
            console.log("Ответ от сервера не получен");
        }
    });
    request.send();
};


requestStatus();

// Функция выбора игры. 

function chooseGame(gamesList) {
    chooseList.innerHTML = `<span>Список игр:</span>`;  // Добавим подсказку
    gamesList.forEach((item, id) => {
        // chooseList.innerHTML += `<div class="menu-btn menu-buttons-choose"><a href="{{url_for('game')}}">Игра номер: ${item}</a></div>`;
        chooseList.innerHTML +=         // Игра номер: ${gamesList.game_id}
        `<div class="menu-btn menu-buttons-choose">
            Игра номер: ${item}
        </div>`;  //   ид: ${id}
    });

    // Определяем позицию кнопки и "создаем" соответсвующий приказ
    document.querySelectorAll(".menu-buttons-choose").forEach((btn, i) => {
        btn.addEventListener('click', () => {
            console.log(`Вы выбрали игру номер: ${gamesList[i]}`);
            deleteGame(gamesList[i])
        });
    });
};


// Удалить выбранную игру
function deleteGame(gameId) {
    const request = new XMLHttpRequest();
    request.open('GET', `/delete_game?id=${gameId}`);
    request.addEventListener('load', () => {
        console.log("Xmmm");
        requestStatus();
    });
    request.addEventListener('error', () => {
        console.log('error')
    });
    request.send();
}


