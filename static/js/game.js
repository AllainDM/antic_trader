console.log('Стрипт странички игры успешно загружен');


// Меню для уточнения количества
const chooseList = document.querySelector('.choose-list');

// Отображаемые в интерфейсе параметры, одновляются при запросе на сервер
let statusGame = {
    dynastyName: "Страна не загрузилась",
    year: -300,
    turn: 1,
    end_turn: false,
    endTurnKnow: true, // Оповещен ли игрок о новом ходе
    acts: [],           // Запись планируемых действий с описанием
    // actsText: [],       // Запись планируемых действий в виде текста понятного для игрока
    logsText: [],       // Запись итогов хода в виде текста понятного для игрока
    logsTextAllTurns: [],       // Запись итогов хода в виде текста понятного для игрока
    allLogs: [],        // Все логи итогов хода всех стран
    allLogsParty: [],        // Все логи итогов хода всех стран за всю партию
    gold: 0,
    title: 0,
    bodyPoints: 0,      // Очки действия для игрока
    donateSum: 0,       // Наши пожертвования
    donateLeader: 0,      // Лидер пожертвований, получает 1 победное очко
    goodsListForSell: [],  // Список ресурсов в наличии у страны, для отображения при продаже
    goodsName: [],
    goods_list: {},  // Словарь(обьект) с количеством ресурсов, для торговли
    colonyListForBuild: [],  // Список доступных для строительства построек
    // Сюда попробуем записать обьект с ценами на постройки
    colonyPrice: {},
    allGoodsPrices: {},  // Словарь(обьект) с городами и ценами на товары
    // Игроки
    dynastyList: [],
    curNumPlayers: 0,
    maxPlayers: 12,
    // Победа и победители
    winPoints: 0,
    wpForWin: 0,
    winners: [],

    user_name: "",
    game_id: "",        // ИД партии. Будем передавать вместе с ходом.
    date_create: "",
    cities: [], // Массив с городами, пока просто названия
    autoUpdate: true,  // Таймер автообновления странички
};

// Модальное окно
// Получить модальное окно
const modal = document.getElementById("my-modal");

// Получить кнопку, которая открывает модальное окно
const btnShowAllLogsParty = document.getElementById("show_all_logs_party");
const btnShowAllLogsPartyPlayers = document.getElementById("show_all_logs_party_players");

// Получить элемент <span>, который закрывает модальное окно
const span = document.getElementsByClassName("close")[0];



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
    // Первое меню
    document.getElementById('province-name').innerText = statusGame.dynastyName; 
    // Золото
    document.getElementById('gold').innerHTML = `<img class="icon" src="/static/image/icon/money.png"> ` + statusGame.gold;  // 'Золото: ' + 
    // Очки действий. Покрасим в красный цвет в случае ухода в минус
    const showBodyPoints = document.getElementById('body-points');
    showBodyPoints.innerText = `Очки действий: ${statusGame.bodyPoints - statusGame.acts.length}`;
    if (statusGame.bodyPoints - statusGame.acts.length < 0) {
        console.log("Нехватает очков действий");
        showBodyPoints.classList.add("set-red-font");
    } else {
        showBodyPoints.classList.remove("set-red-font");    
    document.getElementById('rank').innerText = 'Титул: ' + statusGame.title;}  // Титул(ранг) игрока    
    document.getElementById('donate-leader').innerText = 'Лидер пожертвований: ' + statusGame.donateLeader;
    document.getElementById('win-points').innerText = 'Победные очки: ' + statusGame.winPoints;

    // Второе меню
    document.getElementById('cur-num-players').innerText = `Игроков: ${statusGame.curNumPlayers}`;
    document.getElementById('max-players').innerText = `Макс.игроков: ${statusGame.maxPlayers}`;
    document.getElementById('victory-conditions').innerText = `Условия победы: Набрать ${statusGame.wpForWin} очков`;
    document.getElementById('winners').innerText = 'Победители: ' + statusGame.winners;

    // Третье меню со списком игрков и их готовность
    //

    // Четвертое меню, даты и хода
    document.getElementById('year-turn').innerText = 'Дата: ' + statusGame.year + " Ход: " + statusGame.turn;
    if (statusGame.end_turn) {
        document.getElementById('end-turn-bool').innerText = "Ход ГОТОВ"
    } else {
        document.getElementById('end-turn-bool').innerText = "Ход НЕ готов"
    }

    // Меню разработки
    document.getElementById('player').innerText = 'Игрок: ' + statusGame.user_name;
    document.getElementById('game-id').innerText = 'Игра: ' + statusGame.game_id;
    document.getElementById('game-date').innerText = 'Дата создания: ' + statusGame.date_create;

    if (statusGame.endTurnKnow == false) {
        confimRecTurnModal();
    };


};

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
                // Тут же проверим победителя                
                if (response.winners.length > 0) {
                    console.log(`Есть победитель, династия ${response.winners}`)
                    let infoHtml = `<p style="font-size: 20px;">Есть победитель(и), династия(и) ${response.winners}</p>` 
                    infoModal(infoHtml)
                };

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

// Делаем новый таймер, он работает от включенной переменной autoUpdate
function autoUpdate() {
    // const tm = document.getElementById("timer");
    // if (statusGame.autoUpdate) {
    //     console.log("Таймер работает")
    //     let timer = setInterval(tm.innerHTML = `<p>10</p>`, 1000)
    //     for (i = 10; i >= 0; i--) {
    //     }
    //     clearInterval(timerId2)
    //     // Отключим таймер для разработки
        console.log("Внимание, таймер отключен")
    //     requestStatus();
    //     requestStatusPlayer();
        
    // }
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

    // Год и ход
    statusGame.year = res.year;
    statusGame.turn = res.turn;

    // Инфа об условиях победы
    statusGame.wpForWin = res.need_win_points_for_win

    // Пожертвования
    statusGame.donateLeader = res.donate_leader;

    // Логи
    statusGame.allLogs = res.all_logs;
    statusGame.allLogsParty = res.all_logs_party;

    // Имя игрока и инфа о партии
    statusGame.user_name = res.user_name;
    statusGame.game_id = res.game_id;
    statusGame.date_create = res.date_create;
    statusGame.curNumPlayers = res.dynasty_list.length  // Текущим количеством игроков выведем длинну списка стран
    statusGame.maxPlayers = res.max_players

    statusGame.cities = res.cities

    statusGame.colonyPrice = res.buildings_price  // Цены на постройки    
    statusGame.allGoodsPrices = res.all_goods_prices  // Цены на товары по городам    
    console.log("тут_231234");
    console.log(res.all_goods_prices);


    updateVar();
    logAllResultStart();
    // При загрузке запустим запрос статистики игроков для отображения в отдельном окошке
    req_status_all_player_head();
};



const goodsNameHtml = document.querySelector(".stats-resources");
const buildingsNameHtml = document.querySelector(".stats-buildings");
// const goodsNameHtml = document.querySelector('.choose-list');

// Обновим параметры управляемой "страной"
function actualVarPlayer(res) {
    statusGame.winPoints = res.win_points
    statusGame.dynastyName = res.name_rus
    statusGame.gold = res.gold
    statusGame.donateSum = res.donate_sum;
    statusGame.title = res.title
    statusGame.bodyPoints = res.body_points
    statusGame.end_turn = res.end_turn

    // Игроки
    

    //  Запись не выполненных действий, массив обновляется на беке при выполнении и остаток возвращается на фронт
    statusGame.acts = res.acts
    // statusGame.actsText = res.acts_text
    statusGame.logsText = res.result_logs_text
    statusGame.logsTextAllTurns = res.result_logs_text_all_turns
    statusGame.endTurnKnow = res.end_turn_know;

    // Обновим список доступных для игрока(страны) построек
    statusGame.colonyListForBuild = res.buildings_available_list
    console.log(res.buildings_available_list);


    // Запишем список ресурсов. Для торговли
    statusGame.goods_list = res.goods_list

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

// Отправка хода с модалкой
document.getElementById('end-turn-btn').addEventListener('click', () => {
    if (statusGame.acts.length < statusGame.bodyPoints) {
        // confimModalEndTurd("У вас еще остались очки действий. Точно отправить ход?")
        modal.style.display = "block";
        let content = document.getElementById("show-content");
        content.innerHTML = `<div style="font-size: 25px">У вас еще остались очки действий. Точно отправить ход?</div>`
        content.innerHTML += `<button onclick = "postTurn(statusGame.game_id); closeModal();" style="font-size: 25px; width: 100px">Да</button>`
        content.innerHTML += `<button onclick = closeModal() style="font-size: 25px; width: 100px">Нет</button>`
    } else {
        postTurn(statusGame.game_id);
    }
    // postTurn(statusGame.game_id); // Передадим ИД партии аргументом, он сразу уйдет на Бек для определения к какой партии присвоить ход
})


function postTurn() {
    const request = new XMLHttpRequest();
    request.open('POST', `/post_turn?gameID=${statusGame.game_id}`);
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

function confirmRecTurn() {  // Подтвердить получение хода, чтобы не вылазило оповещение

    closeModal(); // Закроем модальное окошко

    const request = new XMLHttpRequest();
    request.open('GET', `/confirm_rec_turn?gameID=${statusGame.game_id}`);
    request.setRequestHeader('Content-type', 'application/json; charset=utf-8');
    
    console.log(JSON.stringify(statusGame.acts));
    // Это можно удалить???
    request.send(JSON.stringify(statusGame.acts));

    request.addEventListener('load', () => {
        console.log("Автообновление");
        requestStatus();
        requestStatusPlayer();
        closeModal(); // Закроем модальное окошко
    });

}

// Функции отображения логов. До хода и итогов хода

function logStart() {       //Функция запуска будущего лога
    let listLogs = document.getElementById('logs');
    listLogs.innerText = 'Ваши действия';  // Очистим
    if (statusGame.bodyPoints - statusGame.acts.length < 0) {
        listLogs.innerText += '\n Внимание, вы запланировали больше чем у вас доступно "очков действий", все не выполненное перенесется на следующий ход.'
    }
    statusGame.acts.forEach((item, num) => {  
        // let a = document.getElementById('logs');
        listLogs.insertAdjacentHTML('beforeend', `<div>${num + 1}: ${item[0]}</div>`);
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
            chooseList.innerHTML += `<button class="menu-buttons-choose custom-btn btn-15">${item} Стоимость: ${statusGame.colonyPrice[item]}</button>`;
            console.log(item);
        // };        
    });

    // Нарисуем кнопку отмены(выхода)
    chooseList.innerHTML += `<button class="menu-choose-exit custom-btn btn-15" id="menu-choose-exit">Отмена</button>`;
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
        `<button class="menu-buttons-show-trade custom-btn btn-15">
            ${item}
        </button>`;
        // ${statusGame.cities[id]}
    });
    
    // Нарисуем кнопку отмены(выхода)
    chooseList.innerHTML += `<button class="menu-choose-exit custom-btn btn-15" id="menu-show-trade-exit">Выход</button>`;
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
    chooseList.innerHTML = `Продаем товар в ${city}:`;
    console.log(`Продаем товар в город ${city}`);
    // Выведем список только тех товаров, которые есть в наличии
    statusGame.goodsListForSell.forEach((item, id) => {
        chooseList.innerHTML += 
        `<button class="menu-buttons-show-trade trade-goods custom-btn btn-15">
            Продать ${item}. Цена: ${statusGame.allGoodsPrices[city][item]}
        </button>`;
    });     
    chooseList.innerHTML += 
    `<button class="custom-btn btn-15 menu-buttons-show-trade" id="sell-all-goods">
        Продать весь товар
    </button>`;
    // Нарисуем кнопку отмены(выхода)
    chooseList.innerHTML += `<button class="custom-btn btn-15 menu-choose-exit" id="menu-show-trade-exit">Выход</button>`;
    // Определяем позицию кнопки и "создаем" соответсвующий приказ
    document.querySelectorAll(".trade-goods").forEach((btn, i) => {
        btn.addEventListener('click', () => {
            console.log(btn);
            console.log(statusGame.goodsListForSell[i]);
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
    `<button class="custom-btn btn-15 menu-buttons-show-trade" id="sell-all-goods">
        Продать все
    </button>`;

    chooseList.innerHTML += 
    `<fieldset> 
        <legend>Выберете количество</legend>
        <p>
            <input id="goods-value" type="range" min="0" max="${statusGame.goods_list[goods]}" 
            onchange="document.getElementById('rangeValue').innerHTML = this.value;" 
            list="rangeList"> 
            <span id="rangeValue">0</span>
        </p>
        <button class="custom-btn btn-15 menu-buttons-show-trade" id="sell-num-goods">
            Продать
        </button>
    </fieldset>`;
    // Нарисуем кнопку отмены(выхода)
    chooseList.innerHTML += `<button class="custom-btn btn-15 menu-choose-exit" id="menu-show-trade-exit">Выход</button>`; 
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
        num = document.getElementById('goods-value').value;
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


// Решения 
document.getElementById('menu-decision').addEventListener('click', () => {
    hiddenAllMenu();
    console.log("Запуск решений")
    document.getElementById("main-menu-buttons").setAttribute('style','display:none');
    document.getElementById("menu-buttons-decision").setAttribute('style','visibility:visible');

});

document.getElementById('buy-title').addEventListener('click', () => {

    modal.style.display = "block";
    let content = document.getElementById("show-content");
    content.innerHTML = `
        <div style="font-size: 20px">
            <div>Купить титул</div>
            <div>Стоимость: 1000 за 1 ранг + 100 за каждый купленный ранг игроками.</div>
            <button onclick = buyTitle() style="font-size: 25px; margin-top: 10px">Купить</button>
            <button onclick = closeModal() style="font-size: 25px">Отмена</button>
        </div>
    `;
    
    console.log("Модалка открыта");

});
function buyTitle() {
    console.log("Купить титул");
    statusGame.acts.push([`Покупаем титул`, 301]); 
    postAct(statusGame.game_id);
    logStart();
    chooseList.innerHTML = ''; 
    closeModal();
    exitToMainMenuButtons(); 
}

document.getElementById('make-donation').addEventListener('click', () => {

    modal.style.display = "block";
    let content = document.getElementById("show-content");  // <div>Сделать пожертвование.</div>
    content.innerHTML = `
        <div style="font-size: 20px">
            <div>Сделайте пожертвование на выбранную сумму. Победное очко достается только одному игроку, сделавшему на протяжении партии пожетвований на наибольшую сумму.</div>
            <div>Ваши пожертвования: ${statusGame.donateSum}.</div>
            <div>Лидер пожертвований: ${statusGame.donateLeader}.</div>
            <button onclick = makeDonation(100) style="font-size: 25px; margin-top: 10px">100</button>
            <button onclick = makeDonation(200) style="font-size: 25px; margin-top: 10px">200</button>
            <button onclick = makeDonation(300) style="font-size: 25px; margin-top: 10px">300</button>
            <button onclick = makeDonation(400) style="font-size: 25px; margin-top: 10px">400</button>
            <button onclick = makeDonation(500) style="font-size: 25px; margin-top: 10px">500</button>

            <button onclick = closeModal() style="font-size: 25px">Отмена</button>
        </div>
    `;
    
    console.log("Модалка открыта");
});

function makeDonation(sum) {
    console.log("Сделать пожертвование");
    statusGame.acts.push([`Делаем пожертвование на ${sum} золота`, 302, sum]); 
    postAct(statusGame.game_id);
    logStart();
    chooseList.innerHTML = ''; 
    closeModal();
    exitToMainMenuButtons();     
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
function req_status_all_player_head() {
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
        `<button class="menu-buttons-show-diplomaty custom-btn btn-15">
        ${playersList[id]["name_rus"]}.
        Золото: ${playersList[id]["gold"]}.
        Очки: ${playersList[id]["win_points"]}
        </button>`; 
    });
    // Нарисуем кнопку отмены(выхода)    
    chooseList.innerHTML += `<button class="menu-choose-exit custom-btn btn-15" id="menu-show-diplomaty-exit">Выход</button>`;
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
        if (playersList[id]["end_turn"] == true) {
            // status_end_turn = "Готов"
            playersStatusList.innerHTML += 
            `<div>
            ${playersList[id]["name_rus"]}: <span style="background-color: green;"> Готов </span>
            </div>`; 

        } else {
            // status_end_turn = "НЕ готов"
            playersStatusList.innerHTML += 
            `<div>
            ${playersList[id]["name_rus"]}: <span style="background-color: red;"> НЕ готов </span>
            </div>`; 

        }  
        // playersStatusList.innerHTML += 
        // `<div>
        // ${playersList[id]["name_rus"]}: <span style="background-color: red;"> ${status_end_turn} </span>
        // </div>`; 
    });
}

// Модальное окно
// Получение самого элемента вверху скрипта
// // Получить модальное окно
// const modal = document.getElementById("my-modal");

// // Получить кнопку, которая открывает модальное окно
// const btnShowAllLogsParty = document.getElementById("show_all_logs_party");

// // Получить элемент <span>, который закрывает модальное окно
// const span = document.getElementsByClassName("close")[0];

// Открыть модальное окно по нажатию
btnShowAllLogsParty.onclick = function() {
    modal.style.display = "block";
    let content = document.getElementById("show-content");
    content.innerHTML = ""
    console.log("Модалка открыта")
    statusGame.allLogsParty.forEach((item, id) => {
        console.log(item)
        content.innerHTML += `<div>${item}</div>`
    });
    content.innerHTML += `<button onclick = closeModal() style="font-size: 20px">Выйти</button>`
};

btnShowAllLogsPartyPlayers.onclick = function() {
    modal.style.display = "block";
    let content = document.getElementById("show-content");
    content.innerHTML = ""
    console.log("Модалка открыта")
    statusGame.logsTextAllTurns.forEach((item, id) => {
        console.log(item)
        content.innerHTML += `<div>${item}</div>`
    });
    content.innerHTML += `<button onclick = closeModal() style="font-size: 20px">Выйти</button>`
};

// Когда пользователь нажимает на <span> (x), закройте модальное окно
span.onclick = function() {
  modal.style.display = "none";
}

// Общая функция закрытия модального окна
function closeModal() {
    modal.style.display = "none";    
}

// Информационное модальное окошко
function infoModal(text) {
    modal.style.display = "block";
    let content = document.getElementById("show-content");
    content.innerHTML = text 
    content.innerHTML += `<button onclick = closeModal() style="font-size: 25px">Хорошо</button>`

}

// Модальное окошко подтверждения
// Не получается пока сдать универсальное
function confimModal(text, fn) {
    fn = postTurn
    modal.style.display = "block";
    let content = document.getElementById("show-content");
    content.innerHTML = `<div style="font-size: 25px">${text}</div>`
    content.innerHTML += `<button onclick = ${fn} style="font-size: 25px; width: 100px">Да</button>`
    content.innerHTML += `<button onclick = closeModal() style="font-size: 25px; width: 100px">Нет</button>`

}

function confimRecTurnModal() {
    modal.style.display = "block";
    let content = document.getElementById("show-content");
    content.innerHTML = `<div style="font-size: 25px">Новый ${statusGame.turn} ход</div>`;
    content.innerHTML += `<button onclick = confirmRecTurn() style="font-size: 25px; width: 150px">Отлично</button>`;
    // Сразу подвердим получени хода, чтобы окошко не выскакивало два раза
    statusGame.endTurnKnow = true;
}