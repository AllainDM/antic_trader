console.log('Стрипт странички игры успешно загружен');


// Меню для уточнения количества
const chooseList = document.querySelector('.choose-list');

// Отображаемые в интерфейсе параметры, одновляются при запросе на сервер
let statusGame = {
    dynastyName: "none",
    year: -300,
    turn: 1,
    end_turn: false,
    acts: [],           // Запись планируемых действий с описанием
    // actsText: [],       // Запись планируемых действий в виде текста понятного для игрока
    logsText: [],       // Запись итогов хода в виде текста понятного для игрока
    allLogs: [],        // Все логи итогов хода всех стран
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
    user_name: "",
    game_id: "",
    date_create: "",
};



// Запись планируемых действий. Лог ид и текстовый лог. 
// !=== Переместим в StatusGame. В этом случае проблема с сохранением записи хода при обновлении данных с сервера
// let acts = [];
// let actsText = [];
// let logsResult = [];

// Переменная для работы функции автообновления. При отправленном ходе раз в некоторое время происходит запрос новых данных на сервер.
// !!! Можно еще сделать переменные, чтобы при первом получении данных нового хода выскакивало сообщение, что ход обработан.
// Обязательно обрабатывать ответ от сервера с новым ходом, чтоб менять положение это переменной.
// let turnEnd = false;
// Это все есть в обьекте statusGame, по умолчание false

// Список возможных построек. Пока в базовом варианте. В виде массива, для перебора при отображении в виде пунктов меню
// На будущее так же сможет скачиваться с бека

let colonyList = [
    "Плантация(Оливки)",
    "Рудник(Медь)",
    "Невол.рынок(Рабы)",
    "Угодье(Шкуры)",
    "Поля(Зерно)",
];

let goodsList = [
    "Оливки",
    "Медь",
    "Рабы",
    "Шкуры",
    "Зерно",
];

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

    document.getElementById('player').innerText = 'Игрок: ' + statusGame.user_name;
    document.getElementById('game-id').innerText = 'Игра: ' + statusGame.game_id;
    document.getElementById('game-date').innerText = 'Дата создания: ' + statusGame.date_create;


    document.getElementById('goods1').innerText = `${goodsList[0]}: ` + statusGame.goods1;
    document.getElementById('goods2').innerText = `${goodsList[1]}: ` + statusGame.goods2;
    document.getElementById('goods3').innerText = `${goodsList[2]}: ` + statusGame.goods3;
    document.getElementById('goods4').innerText = `${goodsList[3]}: ` + statusGame.goods4;
    document.getElementById('goods5').innerText = `${goodsList[4]}: ` + statusGame.goods5;
    document.getElementById('colony_goods1').innerText = `${colonyList[0]}: ` + statusGame.colony_goods1;
    document.getElementById('colony_goods2').innerText = `${colonyList[1]}: ` + statusGame.colony_goods2;
    document.getElementById('colony_goods3').innerText = `${colonyList[2]}: ` + statusGame.colony_goods3;
    document.getElementById('colony_goods4').innerText = `${colonyList[3]}: ` + statusGame.colony_goods4;
    document.getElementById('colony_goods5').innerText = `${colonyList[4]}: ` + statusGame.colony_goods5;
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
                console.log(response);
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
            console.log("Ответ от сервера не получен");
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

// Вообщем пока игра всегда каждые 20 секунд проверяет параметр "отправлен ли ход", и если отправлен делает запрос на сервер статуса игры
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
    let timerId = setInterval(() => autoUpdate(), 20000);

};
// autoUpdateTimer();

// Обновим общие параметры
function actualVar(res) {
    statusGame.year = res.year;
    statusGame.turn = res.turn;
    statusGame.allLogs = res.all_logs;

    statusGame.user_name = res.user_name;
    statusGame.game_id = res.game_id;
    statusGame.date_create = res.date_create;


    updateVar();
    logAllResultStart();
};

// Обновим параметры управляемой "страной"
function actualVarPlayer(res) {
    statusGame.dynastyName = res.name_rus
    statusGame.gold = res.gold
    statusGame.end_turn = res.end_turn

    //  Запись не выполненных действий, массив обновляется на беке при выполнении и остаток возвращается на фронт
    statusGame.acts = res.acts
    // statusGame.actsText = res.acts_text
    statusGame.logsText = res.result_logs_text

    statusGame.goods1 = res.goods[0]
    statusGame.goods2 = res.goods[1]
    statusGame.goods3 = res.goods[2]
    statusGame.goods4 = res.goods[3]
    statusGame.goods5 = res.goods[4]
    statusGame.colony_goods1 = res.colony_buildings[0]
    statusGame.colony_goods2 = res.colony_buildings[1]
    statusGame.colony_goods3 = res.colony_buildings[2]
    statusGame.colony_goods4 = res.colony_buildings[3]
    statusGame.colony_goods5 = res.colony_buildings[4]


    // end_turn = res.end_turn;
    updateVar();
    logStart();
    logResultStart();
    logAllResultStart();
}

// Отмена приказов
document.getElementById('cancel-all-acts').addEventListener('click', () => {
    cancelAct("all");
});

document.getElementById('cancel-act').addEventListener('click', () => {
    cancelAct("last");
});

function cancelAct(what) {
    const req = new XMLHttpRequest();
    req.open("GET", `/cancel_act?what=${what}`);
    req.addEventListener('load', () => {
        console.log("Xmmm")
        requestStatusPlayer();
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
};

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
    console.log(JSON.stringify(statusGame.acts))
    request.send(JSON.stringify(statusGame.acts));

    request.addEventListener('load', () => {
        console.log("Автообновление");

        // Обновим общие параметры и параметры игрока
        requestStatus();
        requestStatusPlayer();

        // Временно отключу автообновление, неудобно для тестов
        // autoUpdateTimer();

        // Автообновление параметров игры после обсчета хода
        // getVar()
    });

    // requestStatus();
    // requestStatusPlayer();

    // autoUpdateTimer();
};

// Отправка одного действия
// Функция Необходима для отображения актуального списка действий, 
// который не будет пропадать и сбиваться при обновлении странички 
// Ход при этом не считается отправленным
function postAct() {
    const request = new XMLHttpRequest();
    request.open('POST', `/post_act`);
    request.setRequestHeader('Content-type', 'application/json; charset=utf-8');

    // Помимо самих ид действий, нужно еще отправить текстовое описание действий.
    // post = {
    //     acts: statusGame.acts,
    //     // actsText: statusGame.actsText,
    // }
    
    console.log(JSON.stringify(statusGame.acts))
    request.send(JSON.stringify(statusGame.acts));

    request.addEventListener('load', () => {
        console.log("Автообновление");
        requestStatus();
        requestStatusPlayer();
    });
};

// Функции отображения логов. До хода и итогов хода

function logStart() {       //Функция запуска будущего лога
    document.getElementById('logs').innerText = '';  // Очистим
    statusGame.acts.forEach((item, num) => {  
        let a = document.getElementById('logs');
        a.insertAdjacentHTML('beforeend', `<div>${num + 1}: ${item[0]}</div>`);
    });
}

function logResultStart() {       //Функция запуска лога итога хода
    document.getElementById('logs-result').innerText = 'Лог прошлого хода';  // Очистим + подсказка
    statusGame.logsText.forEach((item, num) => {  
        let a = document.getElementById('logs-result');
        a.insertAdjacentHTML('beforeend', `<div>${num + 1}: ${item}</div>`);
    }); 
}

function logAllResultStart() {       //Функция запуска лога итога хода всех игроков
    document.getElementById('all-logs-result').innerText = 'Общий лог прошлого хода';  // Очистим + подсказка
    statusGame.allLogs.forEach((item, num) => {  
        let a = document.getElementById('all-logs-result');
        a.insertAdjacentHTML('beforeend', `<div>${num + 1}: ${item}</div>`);
    }); 
}


// Запись действий игрока
document.getElementById('menu-new-colony').addEventListener('click', () => {
    hiddenAllMenu();  // Скроем все меню
    chooseList.innerHTML = `<span>Выберите постройку:</span>`;  // Добавим подсказку
    colonyList.forEach((item, id) => {
        // if (id > 0) {
            chooseList.innerHTML += `<div class="menu-btn menu-buttons-choose">${colonyList[id]}</div>`;
            console.log(colonyList[id]);
        // };        
    });

    // Нарисуем кнопку отмены(выхода)
    chooseList.innerHTML += `<div class="menu-btn menu-choose-exit" id="menu-choose-exit">Отмена</div>`;
    document.getElementById('menu-choose-exit').addEventListener('click', () => { chooseList.innerHTML = ''; exitToMainMenuButtons(); });

    // Определяем позицию кнопки и "создаем" соответсвующий приказ
    document.querySelectorAll(".menu-buttons-choose").forEach((btn, i) => {
        btn.addEventListener('click', () => {
            statusGame.acts.push([`Строим: ${colonyList[i]}`, 101, i]);         
            // 101 это главный ид действия. i индекс постройки в списке построек в беке. Ну и текст описание действия
            // statusGame.actsText.push(`Построим постройку`);
            postAct();
            logStart();
            console.log(statusGame.acts);
            exitToMainMenuButtons();    // Скрываем меню
            chooseList.innerHTML = '';  // Чистим(скрываем) список
        });
    });

}) 