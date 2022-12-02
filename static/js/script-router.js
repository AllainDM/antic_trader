console.log('Стрипт странички роутеров успешно загружен');

// Первичная загрузка шапки таблицы
function tableStart(tab) {
    document.getElementById(`${tab}`).innerHTML = `<tr class="table-color">
            <th class="table-th" id='th-model'>Модель</th>
            <th class="table-th" id='th-mac'>Мак адрес</th>
            <th class="table-th" id='th-brigada'>Бр.</th>
            <th class="table-th" id='th-comment'>Комментарий</th>
            <th class="table-th" id='th-status'>Статус</th>
            <th class="table-th" id='th-address'>Адрес</th>
            <th class="table-th" id='th-date'>Дата</th>
            <th class="table-th" id='th-btn'></th>
        </tr>`;
}

// Запрос на сервер при загрузке страницы
function start(type) {
    const req = new XMLHttpRequest();
    req.open("GET", `/${type}`);
    req.addEventListener('load', () => {
        const response = JSON.parse(req.responseText);
        output(response);
    });
    req.addEventListener('error', () => {
        console.log('error')
    });
    req.send();
};

// Get запрос комментариев для одного указанного оборудования
function routerCommentFromBD(id) {
    const req = new XMLHttpRequest();
    req.open("GET", `/read_router_comment?idrouter=${id}`);
    req.addEventListener('load', () => {
        const response = JSON.parse(req.responseText);
        // Если ответ есть, запустить функцию отображения
        if (response) {
            writeComment(response, id);
        };
    });
    req.addEventListener('error', () => {
        console.log('error')
    });
    req.send();
};

// Основной Post запрос на сервер
function postMain(router, postType) {
    const request = new XMLHttpRequest();
    request.open('POST', `${postType}`);
    request.setRequestHeader('Content-type', 'application/json; charset=utf-8');
    
    console.log(JSON.stringify(router))
    request.send(JSON.stringify(router));

    request.addEventListener('load', () => {
        console.log("Автообновление");
        start("start_backpack");
    });
};

// Отображаем комментарии для одного, указанного оборудования
// function writeComment(res, id) {
//     let comments = document.getElementById(`th-allcomm${id}`)
//     comments.innerHTML = `<span id='th-comm${id}' class="add-comm">добавить</br></span>`
//     res.forEach((item, num) => {
//         comments.insertAdjacentHTML("beforeend", `${res[num]} <br>`)
//     });
// };

function writeComment(res, id) {
    let comments = document.getElementById(`comm-from-bd${id}`)
    // let comments = document.getElementById(`th-comm${id}`)
    // comments.innerHTML = `<span id='th-comm${id}' class="add-comm">добавить</br></span>`
    res.forEach((item, num) => {
        comments.insertAdjacentHTML("beforeend", `${res[num][2]} ${res[num][3]}<br>`)
    });
};

start("start_backpack");

function output(res) {
    // Убираем лишние шапки табличек
    let tab1 = false;
    let tab2 = false;
    // let tab3 = false;
    // let tab4 = false;
    // Обязательно очистим все таблицы, иначе будет баг с удалением/перепещением последней записи
    document.getElementById('tab1').innerHTML = "";
    document.getElementById('tab2').innerHTML = "";
    // document.getElementById('tab3').innerHTML = "";
    // document.getElementById('tab4').innerHTML = "";

    if (res.length > 0) { // Проверка есть ли роутеры в массиве.
        res.forEach((item, num) => {
            // Распределяем по табличкам согласно статусу
            // 1 - На руках
            // 2 - Установлен
            let tab;
            // Если у приставки статус, для таблички которого нет шапки, то она создается
            if (item[5] == "На руках") {
                if (tab1 == false) {
                    tableStart("tab1");
                    tab1 = true;
                }
                tab = document.getElementById('tab1');
            } else if (item[5] == "Установлен") { 
                if (tab2 == false) {
                    tableStart("tab2");
                    tab2 = true;
                }
                tab = document.getElementById('tab2');
            } 
            
            tab.insertAdjacentHTML("beforeend", 
                    `<tr class="table-color">
                    <th id='th-model'>${res[num][1]}</th>
                    <td id='th-mac'><a href="https://us.gblnet.net/oper/?core_section=customer_list&action=search_page&search=${res[num][2]}&find_typer=all" target="_blank">${res[num][2]}</a><br></td> 
                    <th id='th-brigada'>${res[num][3]}</th>
                    <td id='th-allcomm${res[num][0]}'><span id='th-comm${res[num][0]}' class="add-comm">добавить</span><span id='comm-from-bd${res[num][0]}'></br></span></td> 
                    <td id='th-status'>${res[num][5]} </td> 
                    <td id='th-address'>${res[num][8]} </td> 
                    <td id='th-date'>${res[num][6]} </td> 
                    <td id='th-set${res[num][0]}'><button class="btn-save">Установлен</button></td>
                    <td id='th-del${res[num][0]}'><button class="btn-del">Удалить</button></td>
                    </tr>`
            );
            // <span id='th-comm${res[num][0]}' class="add-comm">добавить</br></span><span id='comm-from-bd${res[num][0]}'></br></span></td> 
            // Get запрос комментария, указывается id оборудования
            routerCommentFromBD(res[num][0]);
            // При нажатии на кнопку удалить, спрашивать комментарий. Все удалленные сохранять отдельно с этим комментарием.
            // Вызов функций навешивания событий на кнопки
            btnDel(res[num][0]);
            // btnSave(res[num][0]);
            btnSet(res[num][0]);
            btnComm(res[num][0]);
        });
    }
    
};

// Кнопка добавить комментарий. Функция навешивает событие на каждую кнопку, присваивая каждой свой ид соответсвующий ид из БД, ид идет как аргумент при вызове функции. Запускается в конце отображения каждого роутера, при переборе массива с роутерами(function output).
function btnComm(num) {
    document.getElementById(`th-comm${num}`).addEventListener('click', () => {
        newComment(num);
        // routerCommentFromBD(num);
    });
};

// Кнопка установить роутер. Тут просто привязка события
function btnSet(num) {
    document.getElementById(`th-set${num}`).addEventListener('click', () => {
        setupRouter(num);
        // routerCommentFromBD(num);
    });
};

// Кнопка удалить роутер. Тут просто привязка события
function btnDel(num) {
    document.getElementById(`th-del${num}`).addEventListener('click', () => {
        deleteRouter(num);
        // routerCommentFromBD(num);
    });
};

function newComment(num) {
    let comment = prompt("Введите комментарий");
    if (comment == null) {
        console.log("Комментария нет");
        return;
    } else {
        date = new Date().toLocaleString("ru");
        let post = {
            id: num,
            comment: comment,
            date: date
        };
        postMain(post, "save_comment");
    }    
};

function setupRouter(num) {
    let address = prompt("Необходимо указать адрес.");
    if (address == null) {
        console.log("Адреса нет");
        return;
    } else {
        // Не отправляем дату при установке, модет потом в отдельную ячейку
        // date = new Date().toLocaleString("ru");
        console.log(date);
        let post = {
            address: address,
            // date: date,
            id: num
        };
        postMain(post, "setup_router");
    }    
};

function deleteRouter(num) {
    let result = confirm(
        // `Удалить роутер:
        // Модель: ${post["model"]}
        // Мак: ${post["mac"]}`
        "Удалить роутер?"
        );
    if (result) {
        postMain(num, "delete_router");
        console.log("Роутер удален")
    }    
};

// Добавление нового роутера
document.getElementById('add').addEventListener('click', () => {

    let mod = document.getElementById('model');
    let model = mod.options[mod.selectedIndex].text;
    
    if (model == '') {
        alert('Укажите модель роутера');
        return;
    };

    let mac = document.getElementById('mac').value;
    let date = new Date().toLocaleDateString("ru");


    let post = {
        mac: mac,
        model: model,
        brigada: 14,
        // comment: comment
        status: 'На руках',
        date: date,
        address: "",
    };
    // console.log(post);

    result = confirm(`
    Проверьте данные: 
    Бригада: ${post["brigada"]} 
    Модель: ${post["model"]}
    Мак: ${post["mac"]}`)

    if (result) {
        postMain(post, "add_router");
        console.log("Роутер отправлен")
        // Удалим коммент на страничке
        // document.getElementById('comment').value = '';
    };
});