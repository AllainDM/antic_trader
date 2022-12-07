console.log('Стрипт странички игры успешно загружен');


// Меню для уточнения количества
const chooseList = document.querySelector('.choose-list');

// Отображаемые в интерфейсе параметры, одновляются при запросе на сервер
let statusGame = {
    dynastyName: "none",
    year: -300,
    turn: 1,
    end_turn: false,
    // acts: [],           // Запись планируемых действий
    // actsText: [],       // Запись планируемых действий в виде текста понятного для игрока
    gold: 0,
    goods1: 0,
    goods2: 0,
    goods3: 0,
    goods4: 0,
    goods5: 0,
    colony_goods1: 0,
    colony_goods2: 0,
    colony_goods3: 0,
    colony_goods4: 0,
    colony_goods5: 0,
};

// Запись планируемых действий. Лог ид и текстовый лог. 
// !=== Переместим в StatusGame. В этом случае проблема с сохранинием записи хода при обновлении данных с сервера
let acts = [];
let actsText = [];

// Переменная для работы функции автообновления. При отправленном ходе раз в некоторое время происходит запрос новых данных на сервер.
// !!! Можно еще сделать переменные, чтобы при первом получении данных нового хода выскакивало сообщение, что ход обработан.
// Обязательно обрабатывать ответ от сервера с новым ходом, чтоб менять положение это переменной.
// let turnEnd = false;
// Это все есть в обьекте statusGame, по умолчание false

// Список возможных построек. Пока в базовом варианте. В виде массива, для перебора при отображении в виде пунктов меню
// На будущее так же сможет скачиваться с бека
let colonyList = [
    "colony_goods1",
    "colony_goods2",
    "colony_goods3",
    "colony_goods4",
    "colony_goods5",
]

// Обычная функция обновления параметров на страничке
// Неплохо бы делать вывод только тех товаров, что есть в наличии через создание верстки перебором массива с ресурсами forEach
function updateVar() {
    document.getElementById('gold').innerText = 'Золото: ' + statusGame.gold;
    document.getElementById('year-turn').innerText = 'Дата: ' + statusGame.year + " Ход: " + statusGame.turn;
    document.getElementById('province-name').innerText = statusGame.dynastyName;
    if (statusGame.end_turn) {
        document.getElementById('end-turn-bool').innerText = "Ход отправлен"
    } else {
        document.getElementById('end-turn-bool').innerText = "Ход НЕ отправлен"
    }

    document.getElementById('goods1').innerText = 'goods1: ' + statusGame.goods1;
    document.getElementById('goods2').innerText = 'goods2: ' + statusGame.goods2;
    document.getElementById('goods3').innerText = 'goods3: ' + statusGame.goods3;
    document.getElementById('goods4').innerText = 'goods4: ' + statusGame.goods4;
    document.getElementById('goods5').innerText = 'goods5: ' + statusGame.goods5;
    document.getElementById('colony_goods1').innerText = 'colony_goods1: ' + statusGame.colony_goods1;
    document.getElementById('colony_goods2').innerText = 'colony_goods2: ' + statusGame.colony_goods2;
    document.getElementById('colony_goods3').innerText = 'colony_goods3: ' + statusGame.colony_goods3;
    document.getElementById('colony_goods4').innerText = 'colony_goods4: ' + statusGame.colony_goods4;
    document.getElementById('colony_goods5').innerText = 'colony_goods5: ' + statusGame.colony_goods5;
}

updateVar();


// "Отдельный" запрос на сервер, получающий дату, номер хода и другие общие параметры
// Будет актуально для "наблюдающего", например для Админа
function requestStatus() {
    const request = new XMLHttpRequest();
    request.open('GET', '/req_status_game');
    request.addEventListener('load', () => {
        if (request.status === 200) {
            if (request.response == "") {
                console.log("К нам пришла пустая строка");
                
            } else {
                const response = JSON.parse(request.response);
                console.log(response)
                actualVar(response);
            };
        } else {
            console.log("Ответ от сервера не получег");
        }
    });
    request.send();

}

// Запрос на сервер уже конкретно параметров "страны" игрока
function requestStatusPlayer() {
    const request = new XMLHttpRequest();
    request.open('GET', '/req_status_game_player');
    request.addEventListener('load', () => {
        if (request.status === 200) {
            if (request.response == "") {
                console.log("К нам пришла пустая строка");
                
            } else {
                const response = JSON.parse(request.response);
                console.log(response)
                actualVarPlayer(response);
                console.log("Ответ от сервера. Статус хода: " + response.end_turn)
            };
        } else {
            console.log("Ответ от сервера не получег");
        }
    });
    request.send();

    // console.log("Ответ от сервера. Статус хода: " + response.end_turn)
    // autoUpdate(); // Автообновление в случае "отправленного хода"
}

requestStatus();
requestStatusPlayer();
// autoUpdateTimer();

// Автообновление странички при статусе "Ход отправлен"
// Запускать проверку с каждым запросом на сервер. 
// Типо: 1 = Запрос на сервер
//       2 = Если переменная "ход отправлен" остается в true, то повторный запрос через интервал
function autoUpdate() {
    if (statusGame.end_turn) {
        requestStatus();
        requestStatusPlayer();
    } 
};

// function autoUpdate2() {
//     requestStatus();
//     requestStatusPlayer();
// };

// Вообщем пока игра всегда каждые 10 секунд проверяет параметр "отправлен ли ход", и если отправлен делает запрос на сервер статуса игры
function autoUpdateTimer() {
    // console.log("Статус хода: " + statusGame.end_turn)
    // console.log(statusGame.end_turn)
    // while (statusGame.end_turn) {
    //     setTimeout(autoUpdate, 3000)
    //     console.log("Таймер работает")
    //     // requestStatus();
    //     // requestStatusPlayer();
    // }
    // if (statusGame.end_turn) {
    //     requestStatus();
    //     requestStatusPlayer();
    // }
    let timerId = setInterval(() => autoUpdate(), 10000);

};
autoUpdateTimer();

// Обновим общие параметры
function actualVar(res) {
    statusGame.year = res.year
    statusGame.turn = res.turn

    updateVar();
};

// Обновим параметры управляемой "страной"
function actualVarPlayer(res) {
    statusGame.dynastyName = res.name_rus
    statusGame.gold = res.gold
    statusGame.end_turn = res.end_turn

    statusGame.goods1 = res.goods1
    statusGame.goods2 = res.goods2
    statusGame.goods3 = res.goods3
    statusGame.goods4 = res.goods4
    statusGame.goods5 = res.goods5
    statusGame.colony_goods1 = res.colony_goods1
    statusGame.colony_goods2 = res.colony_goods2
    statusGame.colony_goods3 = res.colony_goods3
    statusGame.colony_goods4 = res.colony_goods4
    statusGame.colony_goods5 = res.colony_goods5


    // end_turn = res.end_turn;
    updateVar();
}

// Отправка хода
document.getElementById('end-turn-btn').addEventListener('click', () => {
    postTurn();
})

function postTurn() {
    const request = new XMLHttpRequest();
    request.open('POST', `/post_turn`);
    request.setRequestHeader('Content-type', 'application/json; charset=utf-8');
    
    // console.log(JSON.stringify(country.acts))
    // request.send(JSON.stringify("turn"));
    console.log(JSON.stringify(acts))
    request.send(JSON.stringify(acts));

    request.addEventListener('load', () => {
        console.log("Автообновление");

        requestStatus();
        requestStatusPlayer();

        autoUpdateTimer();
        // Автообновление параметров игры после обсчета хода
        // getVar()
    });

    // requestStatus();
    // requestStatusPlayer();

    // autoUpdateTimer();
};


// Запись действий игрока
document.getElementById('menu-new-colony').addEventListener('click', () => {
    hiddenAllMenu();  // Скроем все меню
    chooseList.innerHTML = `<span>Выберите постройку:</span>`;  // Добавим подсказку
    colonyList.forEach((item, id) => {
        chooseList.innerHTML += `<div class="menu-btn menu-buttons-choose">${colonyList[id]}</div>`;
        console.log(colonyList[id]);
    });

    // Нарисуем кнопку отмены(выхода)
    chooseList.innerHTML += `<div class="menu-btn menu-choose-exit" id="menu-choose-exit">Отмена</div>`;
    document.getElementById('menu-choose-exit').addEventListener('click', () => { chooseList.innerHTML = ''; exitToMainMenuButtons(); });

    document.querySelectorAll(".menu-buttons-choose").forEach((btn, i) => {
        btn.addEventListener('click', () => {
            acts.push([100+i]);         // 100 это главный ид. +i автоматически создаст нужный ид, например 103 или даже 100 для постройки с индексом 0
                                        // На беке кстати можно вычитать 100 и получать "чистый" индекс в массиве построек
            console.log(acts);
            exitToMainMenuButtons();    // Скрываем меню
            chooseList.innerHTML = '';  // Чистим(скрываем) список
        });
    });

}) 