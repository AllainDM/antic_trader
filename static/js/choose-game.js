console.log('Стрипт странички выбора игры успешно загружен');

// Будущий список выбора игры
const chooseList = document.querySelector('.choose-list');

// Запрос статуса для отображения выбора игры
function requestStatus() {
    const request = new XMLHttpRequest();
    request.open('GET', '/load_all_my_game');
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

}

requestStatus();

// Функция выбора игры. 

function chooseGame(gamesList) {
    // Добавим подсказку
    if (gamesList.length > 0) {
        console.log("Игры есть");
        chooseList.innerHTML = `<span>Выберите игру:</span>`;  
    } else {
        chooseList.innerHTML = `<span>Нет доступных игр</span>`;  
    };
    gamesList.forEach((item, id) => {
        chooseList.innerHTML +=         // Игра номер: ${gamesList.game_id}   class="menu-btn menu-buttons-choose"
        `<div >
            <button class="btn btn-choose-game">Войти</button>
            Игра № ${item}
        </div>`;  //   ид: ${id}
    });

    // Определяем позицию кнопки и "создаем" соответсвующий приказ
    document.querySelectorAll(".btn-choose-game").forEach((btn, i) => {
        btn.addEventListener('click', () => {
            console.log(`Вы выбрали игру номер: ${gamesList[i]}`);
            setActiveGame(gamesList[i]); // Установить активную игру, ее данные будет отправлять бек при обновлении и загрузке новой страницы 
        });
    });
};

// При выборе игры, эта игра становится активной для бекенда и сразу идет перенаправление на страничку игры, скачивается "активная" игра с бека

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
