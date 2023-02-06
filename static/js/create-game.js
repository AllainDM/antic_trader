console.log('Стрипт странички создания игры успешно загружен');

// Список для отображения добавляемых игроков
const list = document.querySelector('.list');

document.getElementById('create-new-game').addEventListener('click', () => {
    console.log("Попытка создания игры засчитана")
    createTestNewGame();
});

listPlayers = []

function createTestNewGame() {
    const request = new XMLHttpRequest();
    request.open('GET', '/create_test_new_game');
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

};


function reqUsers() {
    const request = new XMLHttpRequest();
    request.open('GET', '/req_list_players');
    request.addEventListener('load', () => {
        if (request.status === 200) {
            if (request.response == "") {
                console.log("К нам пришла пустая строка");                
            } else {
                const response = JSON.parse(request.response);
                console.log(response);
                console.log("Ответ от js: Игра создалась");  
                listPlayers = response;
                console.log(listPlayers);
                // actualVar(response);
            };
        } else {
            console.log("Ответ от сервера не получен");
        }
    });
    request.send();

};

reqUsers();

const dynastyName = document.getElementById('dynasty-name');
const modalSetDynasty = document.getElementById('modal-set-dynasty');


function setDynasty() {
    dynastyName.innerHTML = "Выберите название династии";
    modalSetDynasty.style.display = 'block';

}

// setDynasty();

// Модальное окно настройки новой Династии

// Получить модальное окно
const modal = document.getElementById("my-modal");

// Получить кнопку, которая открывает модальное окно
const btnAddNewDynasty = document.getElementById("add-new-dynasty");

// Получить элемент <span>, который закрывает модальнок окно
const span = document.getElementsByClassName("close")[0];


// Когда пользователь нажимает на кнопку, откройте модальнок окно
btnAddNewDynasty.onclick = function() {
    modal.style.display = "block";
    // Отобразим список доступных(пока что вообще всех) игроков
    newPlayers = document.getElementById('choose-players');
    newPlayers.innerHTML = "<option value='000'></option>" // Почистим от предыдущей загрузки
    listPlayers.forEach((item, id) => {
        // console.log(item)
        newPlayers.innerHTML +=        
        `<option value="${id}">${item[1]}</option>`; 
    });
}

// Когда пользователь нажимает на <span> (x), закройте модальное окно
span.onclick = function() {
  modal.style.display = "none";
}

// Создадим массив, глобально, для добавления нового игрока.
// Пока не могу придумать ничего умнее. Возможно нужен какойто коллбек с ожиданием донастройки всех игрков
newGame = [];
// 0 = ид игрока
// 1 = название династии на английском
// 2 = название династии на русском
// 3 = стартовое золото

// Кнопка, которая добавляет настроенного игрока/династию
document.getElementById("add-dynasty").addEventListener("click", () => {
    console.log("Добавляем династию");
    // Сверим тип данных у "стартового золота"
    if (Number(document.getElementById('choose-players').value) == 0) {
        console.log("Игрок Админ или не выбран");
        alert("Игрок Админ или не выбран");
        return
    }
    else if (document.getElementById('name-eng').value == "") {
        console.log("name-eng");
        alert("Укажите название династии на английском");
        return
    }
    else if (document.getElementById('name-rus').value == '') {
        console.log("name-rus");
        alert("Укажите название династии на русском");
        return
    }
    else if (isNaN(document.getElementById('start-gold').value)) {
        console.log("Не число");
        alert("Стартовое золото не является числом");
        return
    }
    let newDynasty = [
        Number(document.getElementById('choose-players').value) + 1,
        document.getElementById('name-eng').value,
        document.getElementById('name-rus').value,
        Number(document.getElementById('start-gold').value),
        listPlayers[Number(document.getElementById('choose-players').value)][1]  // Имя игрока
    ];
    console.log(document.getElementById('choose-players').value);
    console.log(Number(document.getElementById('choose-players').value));
    console.log(listPlayers[Number(document.getElementById('choose-players').value)][1]);
    newGame.push(newDynasty)
    console.log(newDynasty);
    modal.style.display = "none";
    console.log(newGame);
    // Обновим список добавленных игроков
    showPlayers(newGame)
});

document.getElementById("create-new-set-game").addEventListener("click", () => {
    createNewGame(newGame);
    // Почистим массив для создания еще одной новой игры
    newGame = [];
});

function createNewGame(post) {
    const request = new XMLHttpRequest();
    request.open('POST', '/create_new_game');
    request.setRequestHeader('Content-type', 'application/json; charset=utf-8');
    
    console.log(JSON.stringify(post))
    request.send(JSON.stringify(post));

    request.addEventListener('load', () => {
        console.log("Запрос на создание новой настроенной игры")
    });

};
// Когда пользователь щелкает в любом месте за пределами модального, закройте его
// window.onclick = function(event) {
//   if (event.target == modal) {
//     modal.style.display = "none";
//   }
// } 

// Отображение добавляемых игроков
function showPlayers(players) {
    console.log(players);
    list.innerHTML = `<span>Игроки:</span>`;  // Добавим подсказку
    players.forEach((item, id) => {
        // chooseList.innerHTML += `<div class="menu-btn menu-buttons-choose"><a href="{{url_for('game')}}">Игра номер: ${item}</a></div>`;
        list.innerHTML +=         
        `<div class="show-list">
            ${item[1]} ${item[2]} ${item[4]}
        </div>`;  //   ид: ${id}
    });

    // Определяем позицию кнопки и "создаем" соответсвующий приказ
    document.querySelectorAll(".show-list").forEach((btn, i) => {
        btn.addEventListener('click', () => {
            console.log(`Вы выбрали игрока: ${players[i][4]}`);  // -1

        });
    });
};