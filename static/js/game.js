console.log('Стрипт странички игры успешно загружен');


// Меню для уточнения количества
const chooseList = document.querySelector('.choose-list');

// Отображаемые в интерфейсе параметры, одновляются при запросе на сервер
let statusGame = {
    dynastyName: "Страна не загрузилась",
    year: -300,
    turn: 1,
    end_turn: false,
    acts: [],           // Запись планируемых действий с описанием
    // actsText: [],       // Запись планируемых действий в виде текста понятного для игрока
    logsText: [],       // Запись итогов хода в виде текста понятного для игрока
    allLogs: [],        // Все логи итогов хода всех стран
    gold: 0,
    goodsListForSell: [],  // Список ресурсов в наличии у страны, для отображения при продаже
    goodsName: [],
    goods_list: {},  // Словарь(обьект) с количеством ресурсов, для торговли
    colonyListForBuild: [],  // Список доступных для строительства построек
    winPoints: "?",
    winners: [],
    user_name: "",
    game_id: "",        // ИД партии. Будем передавать вместе с ходом.
    date_create: "",
    cities: [], // Массив с городами, пока просто названия
    autoUpdate: true,  // Таймер автообновления странички
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

// let colonyList = [
//     "Плантация(Оливки)",
//     "Рудник(Медь)",
//     "Невол.рынок(Рабы)",
//     "Угодье(Шкуры)",
//     "Поля(Зерно)",
// ];

// let goodsList = [
//     "Оливки",
//     "Медь",
//     "Рабы",
//     "Шкуры",
//     "Зерно",
// ];

// Обычная функция обновления параметров на страничке
// Неплохо бы делать вывод только тех товаров, что есть в наличии через создание верстки перебором массива с ресурсами forEach
function updateVar() {
    document.getElementById('win-points').innerText = 'Победные очки: ' + statusGame.winPoints;
    document.getElementById('winners').innerText = 'Победители: ' + statusGame.winners;

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
                actualVarPlayer(response);
                console.log("Ответ от сервера. Статус хода: " + response.end_turn)
            };
        } else {
            console.log("Ответ от сервера не получен");
        }
    });
    request.send();
}

requestStatus();
requestStatusPlayer();
// autoUpdateTimer();

// Автообновление странички при статусе "Ход отправлен"
// Запускать проверку с каждым запросом на сервер. 
// Типо: 1 = Запрос на сервер
//       2 = Если переменная "ход отправлен" остается в true, то повторный запрос через интервал
// function autoUpdate() {
//     if (statusGame.end_turn) {
//         requestStatus();
//         requestStatusPlayer();
//     } 
// };

// function autoUpdate2() {
//     requestStatus();
//     requestStatusPlayer();
// };

// Вообщем пока игра всегда каждые 20 секунд проверяет параметр "отправлен ли ход", и если отправлен делает запрос на сервер статуса игры
// function autoUpdateTimer() {
//     // console.log("Статус хода: " + statusGame.end_turn)
//     // console.log(statusGame.end_turn)
//     // while (statusGame.end_turn) {
//     //     setTimeout(autoUpdate, 3000)
//     //     console.log("Таймер работает")
//     //     // requestStatus();
//     //     // requestStatusPlayer();
//     // }
//     // if (statusGame.end_turn) {
//     //     requestStatus();
//     //     requestStatusPlayer();
//     // }
//     let timerId = setInterval(() => autoUpdate(), 20000);

// };
// autoUpdateTimer();

// Делаем новый таймер, он работает от включенной переменной autoUpdate
function autoUpdate() {
    const tm = document.getElementById("timer");
    if (statusGame.autoUpdate) {
        console.log("Таймер работает")
        // let timer = setInterval(tm.innerHTML = `<p>10</p>`, 1000)
        // for (i = 10; i >= 0; i--) {
        // }
        // clearInterval(timerId2)
        requestStatus();
        requestStatusPlayer();
        
    }
};
function showTimer() {

}
let timerId = setInterval(() => autoUpdate(), 10000);

// // autoUpdate();
// function autoUpdateTimer() {
//     // while (statusGame.end_turn) {
//     //     setTimeout(autoUpdate, 3000)
//     //     console.log("Таймер работает")
//     //     // requestStatus();
//     //     // requestStatusPlayer();
//     // }
//     // if (statusGame.end_turn) {
//     //     requestStatus();
//     //     requestStatusPlayer();
//     // }
//     let timerId = setInterval(() => autoUpdate(), 5000);
// };
// autoUpdateTimer();

// Обновим общие параметры
function actualVar(res) {
    statusGame.winners = res.winners;

    statusGame.year = res.year;
    statusGame.turn = res.turn;
    statusGame.allLogs = res.all_logs;

    statusGame.user_name = res.user_name;
    statusGame.game_id = res.game_id;
    statusGame.date_create = res.date_create;

    statusGame.cities = res.cities


    updateVar();
    logAllResultStart();
    // При загрузке запустим запрос статистики игроков для отображения в отдельном окошке
    req_status_all_player();
};



const goodsNameHtml = document.querySelector(".stats-resources");
const buildingsNameHtml = document.querySelector(".stats-buildings");
// const goodsNameHtml = document.querySelector('.choose-list');

// Обновим параметры управляемой "страной"
function actualVarPlayer(res) {
    statusGame.winPoints = res.win_points
    statusGame.dynastyName = res.name_rus
    statusGame.gold = res.gold
    statusGame.end_turn = res.end_turn

    //  Запись не выполненных действий, массив обновляется на беке при выполнении и остаток возвращается на фронт
    statusGame.acts = res.acts
    // statusGame.actsText = res.acts_text
    statusGame.logsText = res.result_logs_text

    // Обновим список доступных для игрока(страны) построек
    statusGame.colonyListForBuild = res.buildings_available_list

    // Запишем список ресурсов. Для торговли
    statusGame.goods_list = res.goods_list
    console.log("тут");
    console.log(res.goods_list);
    console.log(res.goods_name_list);

    // Вывод на экран количества ресурсов и построек
    // goodsNameHtml.innerHTML += `<div>Ресурсы: </div>`;
    goodsNameHtml.innerHTML = `<div style="margin-top: 2px; text-align: center;">Ресурсы</div>`;
    statusGame.goodsListForSell = []
    // if (res.goods_list.length > 0) {
        res.goods_name_list.forEach((item, id) => {        
            console.log("forEach 2 Тут выводим список ресурсов");
            if (res.goods_list[item] > 0) {
                // Добавим товар в массив который выводится при выборе товара для продажи
                statusGame.goodsListForSell.push(item);
                goodsNameHtml.innerHTML +=   
                `<div>
                    ${item}: ${res.goods_list[item]}
                </div>`;
            };        
        });
    // } else {
    //     goodsNameHtml.innerHTML += `<div>Ничего нет</div>`;
    // }
    
    console.log(statusGame.goodsListForSell);

    buildingsNameHtml.innerHTML = `<div style="margin-top: 2px; text-align: center;">Постройки</div>`;

    // if (res.buildings_list.length > 0) {
        res.buildings_name_list.forEach((item, id) => {
            console.log("forEach 3 Тут выводим список ресурсов");
            if (res.buildings_list[item] > 0) {
                buildingsNameHtml.innerHTML +=   
                `<div>
                    ${item}: ${res.buildings_list[item]}
                </div>`;
            };        
        });
    // } else {
    //     buildingsNameHtml.innerHTML += `<div>Ничего нет</div>`;
    // }

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
    req.open("GET", `/cancel_act?gameId=${statusGame.game_id}&what=${what}`);
    req.addEventListener('load', () => {
        console.log("Xmmm");
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
    postTurn(statusGame.game_id); // Передадим ИД партии аргументом, он сразу уйдет на Бек для определения к какой партии присвоить ход
})

function postTurn(gameId) {
    const request = new XMLHttpRequest();
    request.open('POST', `/post_turn?gameID=${gameId}`);
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
// По факту не одного, а сразу всех. И бек не пушит в массив, а перезаписывает заново
// Функция Необходима для отображения актуального списка действий, 
// который не будет пропадать и сбиваться при обновлении странички 
// Ход при этом не считается отправленным
function postAct(gameId) {
    const request = new XMLHttpRequest();
    request.open('POST', `/post_act?gameID=${gameId}`);
    request.setRequestHeader('Content-type', 'application/json; charset=utf-8');

    // Помимо самих ид действий, нужно еще отправить текстовое описание действий.
    // Текстовая теперь запись идет в массиве действия под нулевым индексом
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

// Строительство 
document.getElementById('menu-new-colony').addEventListener('click', () => {
    hiddenAllMenu();  // Скроем все меню
    chooseList.innerHTML = `<span>Выберите постройку:</span>`;  // Добавим подсказку
    statusGame.colonyListForBuild.forEach((item, id) => {
        // if (id > 0) {
            chooseList.innerHTML += `<div class="menu-btn menu-buttons-choose">${item}</div>`;
            console.log(item);
        // };        
    });

    // Нарисуем кнопку отмены(выхода)
    chooseList.innerHTML += `<div class="menu-btn menu-choose-exit" id="menu-choose-exit">Отмена</div>`;
    document.getElementById('menu-choose-exit').addEventListener('click', () => { chooseList.innerHTML = ''; exitToMainMenuButtons(); });

    // Определяем позицию кнопки и "создаем" соответсвующий приказ
    document.querySelectorAll(".menu-buttons-choose").forEach((btn, i) => {
        btn.addEventListener('click', () => {
            statusGame.acts.push([
                `Строим: ${statusGame.colonyListForBuild[i-1]}`, 101, statusGame.colonyListForBuild[i-1]
            ]);         
            // 101 это главный ид действия. i индекс постройки в списке построек в беке. Ну и текст описание действия
            postAct(statusGame.game_id);
            logStart();
            console.log(statusGame.acts);
            exitToMainMenuButtons();    // Скрываем меню
            chooseList.innerHTML = '';  // Чистим(скрываем) список
        });
    });

}) 

// Торговля
document.getElementById('menu-trade').addEventListener('click', () => {
    hiddenAllMenu();
    console.log("Запуск торговли")
    document.getElementById("main-menu-buttons").setAttribute('style','display:none');
    document.getElementById("menu-buttons-trade").setAttribute('style','visibility:visible');
    tradeChooseCity();
});

// Выбрать город для торговли
function tradeChooseCity() { 
    statusGame.cities.forEach((item, id) => {
        chooseList.innerHTML += 
        `<div class="menu-btn menu-buttons-show-trade">
            ${item}
        </div>`;
        // ${statusGame.cities[id]}
    });
    
    // Нарисуем кнопку отмены(выхода)
    chooseList.innerHTML += `<div class="menu-btn menu-choose-exit" id="menu-show-trade-exit">Выход</div>`;
    document.getElementById('menu-show-trade-exit').addEventListener('click', () => { 
        chooseList.innerHTML = ''; 
        exitToMainMenuButtons(); 
    });

    // Определяем позицию кнопки и "создаем" соответсвующий приказ
    document.querySelectorAll(".menu-buttons-show-trade").forEach((btn, i) => {
        btn.addEventListener('click', () => {
            console.log(`Вы выбрали город номер: ${btn}, ${i}`);
            console.log(`Вы выбрали город: ${statusGame.cities[i]}`);
            tradeChooseAction(statusGame.cities[i]); // Запустим дальнейшую функицю, передав ид (!не)города(ИД по списку предложенных к выбору)
        });
    });
};

// После выбора города определим дальнейшие дествия
function tradeChooseAction(city) {
    chooseList.innerHTML = "Продаем товар:";
    console.log(`Продаем товар в город ${city}`);
    // Выведем список только тех товаров, которые есть в наличии
    statusGame.goodsListForSell.forEach((item, id) => {
        chooseList.innerHTML += 
        `<div class="menu-btn menu-buttons-show-trade trade-goods">
            Продать ${item}
        </div>`;
    });     

    chooseList.innerHTML += 
    `<div class="menu-btn menu-buttons-show-trade" id="sell-all-goods">
        Продать весь товар
    </div>`;

    // Нарисуем кнопку отмены(выхода)
    chooseList.innerHTML += `<div class="menu-btn menu-choose-exit" id="menu-show-trade-exit">Выход</div>`;

    // Определяем позицию кнопки и "создаем" соответсвующий приказ
    document.querySelectorAll(".trade-goods").forEach((btn, i) => {
        btn.addEventListener('click', () => {
            console.log(btn);
            console.log(statusGame.goodsListForSell[i]);
            // console.log([`Продаем: ${statusGame.goodsListForSell[i]} в ${statusGame.cities[i]}`, 201, city, i]); 
            // statusGame.acts.push([`Продаем: ${statusGame.goodsListForSell[i]} в ${city}`, 
            //     201, city, statusGame.goodsListForSell[i]
            // ]); 
            // postAct(statusGame.game_id);
            // logStart();
            // chooseList.innerHTML = ''; 
            // exitToMainMenuButtons(); 
            tradeChooseNumGoodsTrade(statusGame.goodsListForSell[i], city);
        });
    });
    // Определяем еще одну кнопку
    document.getElementById("sell-all-goods").addEventListener('click', () => {
        console.log("А попробем-ка продать весь товар");
        statusGame.acts.push([`Продаем весь товар в ${city}`, 202, city]); 
        postAct(statusGame.game_id);
        logStart();
        chooseList.innerHTML = ''; 
        exitToMainMenuButtons(); 
    });    
    // Событие выхода на соответствующую кнопку
    document.getElementById('menu-show-trade-exit').addEventListener('click', () => { 
        chooseList.innerHTML = ''; 
        exitToMainMenuButtons(); 
    });
}

// После выбора города и выбора товара уточняем количество
function tradeChooseNumGoodsTrade(goods, city) {
    chooseList.innerHTML = "Продаем товар:";

    chooseList.innerHTML += 
    `<div class="menu-btn menu-buttons-show-trade" id="sell-all-goods">
        Продать все
    </div>`;

    // chooseList.innerHTML += 
    // `<div class="menu-btn menu-buttons-show-trade" id="sell-one-goods">
    //     Продать 1 штуку
    // </div>`;

    // chooseList.innerHTML += 
    // `<input type="range" min="0" max="${statusGame.goods_list[goods]}">`;


    chooseList.innerHTML += 
    `<fieldset> 
        <legend>Выберете количество</legend>
        <p>
            <input id="goods-value" type="range" min="0" max="${statusGame.goods_list[goods]}" 
            onchange="document.getElementById('rangeValue').innerHTML = this.value;" 
            list="rangeList"> 
            <span id="rangeValue">0</span>
        </p>
        <div class="menu-btn menu-buttons-show-trade" id="sell-num-goods">
            Продать
        </div>
    </fieldset>`;

    // Нарисуем кнопку отмены(выхода)
    chooseList.innerHTML += `<div class="menu-btn menu-choose-exit" id="menu-show-trade-exit">Выход</div>`;  

    // Продать весь выбранный товар. Аргумент -1 для бекенда
    document.getElementById('sell-all-goods').addEventListener('click', () => { 
        console.log("А попробем-ка продать веь выбранный товар");
        statusGame.acts.push([`Продаем весь товар ${goods} в ${city}`, 201, city, goods, -1]); 
        postAct(statusGame.game_id);
        logStart();
        chooseList.innerHTML = ''; 
        exitToMainMenuButtons(); 
    });
    // Продать выбранное число товара
    document.getElementById('sell-num-goods').addEventListener('click', () => { 
        num = document.getElementById('goods-value').value
        statusGame.acts.push([`Продаем ${num} товар ${goods} в ${city}`, 201, city, goods, num]); 
        console.log(`Продадим ${num} товар ${goods} в ${city}`);
        postAct(statusGame.game_id);
        logStart();
        chooseList.innerHTML = ''; 
        exitToMainMenuButtons(); 
    });
    // Определяем позицию кнопки и "создаем" соответсвующий приказ

    document.getElementById('menu-show-trade-exit').addEventListener('click', () => { 
        chooseList.innerHTML = ''; 
        exitToMainMenuButtons(); 
    });
}

//
// Просмотр "Дипломатии"
document.getElementById('menu-diplomaty').addEventListener('click', () => {
    hiddenAllMenu();
    document.getElementById("main-menu-buttons").setAttribute('style','display:none');
    document.getElementById("menu-buttons-diplomaty").setAttribute('style','visibility:visible');
    req_status_all_player();
});

// Отображение всех игроков с основными параметрами(золото, имя, готовность хода)
function req_status_all_player() {
    console.log(statusGame.game_id)
    console.log("Запрос статистики игроков")
    const request = new XMLHttpRequest();
    request.open("GET", `/req_status_all_player?gameId=${statusGame.game_id}`);
    request.addEventListener('load', () => {
        console.log("Xmmm")
        if (request.status === 200) {
            if (request.response == "") {
                console.log("К нам пришла пустая строка");
                
            } else {
                const response = JSON.parse(request.response);
                console.log(response)
                displayStatisticsOfAllPlayers(response);
                displayStatisticsOfAllPlayersOnBoard(response);
            };
        } else {
            console.log("Ответ от сервера не получен");
        }
    });
    request.addEventListener('error', () => {
        console.log('error')
    });
    request.send();
};

// И такая же функция для отображения в шапке
function req_status_all_player() {
    console.log(statusGame.game_id)
    console.log("Запрос статистики игроков")
    const request = new XMLHttpRequest();
    request.open("GET", `/req_status_all_player?gameId=${statusGame.game_id}`);
    request.addEventListener('load', () => {
        console.log("Xmmm")
        if (request.status === 200) {
            if (request.response == "") {
                console.log("К нам пришла пустая строка");
                
            } else {
                const response = JSON.parse(request.response);
                console.log(response)
                displayStatisticsOfAllPlayersOnBoard(response);
            };
        } else {
            console.log("Ответ от сервера не получен");
        }
    });
    request.addEventListener('error', () => {
        console.log('error')
    });
    request.send();
};

function displayStatisticsOfAllPlayers(playersList) {
    playersList.forEach((item, id) => {
        status_end_turn = ""
        if (playersList[id]["end_turn"] == true) {
            status_end_turn = "Готов"
        } else {
            status_end_turn = "НЕ готов"
        }  
        chooseList.innerHTML += 
        `<div class="menu-btn menu-buttons-show-diplomaty">
        ${playersList[id]["name_rus"]}.
        Золото: ${playersList[id]["gold"]}.
        Статус: ${status_end_turn}
        </div>`; 
    });
    // Нарисуем кнопку отмены(выхода)    
    chooseList.innerHTML += `<div class="menu-btn menu-choose-exit" id="menu-show-diplomaty-exit">Выход</div>`;
        document.getElementById('menu-show-diplomaty-exit').addEventListener('click', () => { 
            chooseList.innerHTML = ''; 
            exitToMainMenuButtons(); 
        });
}
function displayStatisticsOfAllPlayersOnBoard(playersList) {
    const playersStatusList = document.querySelector(".players-stat");
    playersStatusList.innerHTML = `<div style="margin-top: 2px; text-align: center;">Игроки</div>`
    console.log("Запуск функции отображения статистики игроков в шапке")
    playersList.forEach((item, id) => {
        status_end_turn = ""
        if (playersList[id]["end_turn"] == true) {
            status_end_turn = "Готов"
        } else {
            status_end_turn = "НЕ готов"
        }  
        playersStatusList.innerHTML += 
        `<div>
        ${playersList[id]["name_rus"]}: ${status_end_turn}
        </div>`; 
    });
}