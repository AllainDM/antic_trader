console.log('Стрипт странички создания игры успешно загружен');

// Список для отображения добавляемых игроков
const list = document.querySelector('.list');

document.getElementById('create-new-game').addEventListener('click', () => {
    console.log("Попытка создания игры засчитана")
    createTestNewGame();
});
document.getElementById('add-new-dynasty').addEventListener('click', () => {
    console.log("Добавить нового игрока");
    setGames.numPlayers += 1; // Добавим счетчик игроков, он же ИД для элементов на странице
    tableStart();
});

let setGames = {
    listPlayers: [],
    numPlayers: 1,
    namesEng: ['Magonid', 'Barkid', 'Ganonid', 'Bomgid', 'Hvarid', 'Umrid', 'Bolid', 'Tankid', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
    namesRus: ['Магониды', 'Баркиды', 'Ганониды', 'Бомгиды', 'Хвариды', 'Умриды', 'Болиды', 'Танкиды', '1', '2', '3', '4', '5', '6', '7', '8', '9'],

}

// Создадим массив, глобально, для добавления нового игрока.
// Пока не могу придумать ничего умнее. Возможно нужен какойто коллбек с ожиданием донастройки всех игрков
newGame = [];
// 0 = ид игрока
// 1 = название династии на английском
// 2 = название династии на русском
// 3 = стартовое золото

document.getElementById("create-new-set-game").addEventListener("click", () => {
    // Почистим массив
    newGame = [];
    for (i = 1; i <= setGames.numPlayers; i++) {
        // playerId = document.getElementById(`choose-players_${i}`);
        // nameEng = setGames.namesEng[i];
        // nameRus = setGames.namesRus[i];
        // nameEng = document.getElementById(`choose-nameEng_${i}`);
        let newDynasty = {
            playerId: Number(document.getElementById(`choose-players_${i}`).value) + 1,
            nameEng: setGames.namesEng[i-1],
            nameRus: setGames.namesRus[i-1],
        }
        newGame.push(newDynasty);
        console.log(newDynasty);
        console.log(newGame);
    }
    createNewGame(newGame);
});

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

function tableStart() {
    document.getElementById('tables').insertAdjacentHTML("beforeend", 
        `<table class="table-main">
            <select class="add-players" id="choose-players_${setGames.numPlayers}">
                <option value='000'></option>
            </select>
        </table>`) 
        // <select class="add-players" id="choose-nameEng_${setGames.numPlayers}">
        //     <option value='000'></option>
        // </select>
    newPlayers = document.getElementById(`choose-players_${setGames.numPlayers}`);
    // newPlayersNameEng = document.getElementById(`choose-nameEng_${setGames.numPlayers}`);
    // newPlayersNameRus = document.getElementById(`choose-nameRus_${setGames.numPlayers}`);
    setGames.listPlayers.forEach((item, id) => {
        newPlayers.innerHTML +=        
        `<option value="${item[0]-1}">${item[1]}</option>`; 
    });
    // setGames.namesEng.forEach((item, id) => {
    //     newPlayersNameEng.innerHTML +=        
    //     `<option value="${item}">${item}</option>`; 
    // });
    // setGames.namesRus.forEach((item, id) => {
    //     newPlayersNameRus.innerHTML +=        
    //     `<option value="${item}">${item}</option>`; 
    // });
};

// function moreTable() {
//     document.getElementById('tables').innerHTML += `
//         <table class="table-main">
//             <select class="add-players" id="choose-players_${setGames.numPlayers}"></select>
//         </table>
//     `
//     // document.getElementById('set-new-dynasty').innerHTML += `
//     //     <select class="add-players" id="choose-players">Смотрим</select>
//     // `
//     newPlayers = document.getElementById(`choose-players_${setGames.numPlayers}`);
//     newPlayers.innerHTML = "<option value='000'></option>" // Почистим от предыдущей загрузки
//     setGames.listPlayers.forEach((item, id) => {
//         newPlayers.innerHTML +=        
//         `<option value="${item[0]-1}">${item[1]}</option>`; 
//     });
// };

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
                setGames.listPlayers = response;
                console.log(setGames.listPlayers);
                tableStart();
                // actualVar(response);
            };
        } else {
            console.log("Ответ от сервера не получен");
        }
    });
    request.send();

};

reqUsers();

function createNewGame(post) {
    const request = new XMLHttpRequest();
    request.open('POST', '/create_new_game');
    request.setRequestHeader('Content-type', 'application/json; charset=utf-8');
    
    console.log(JSON.stringify(post));
    request.send(JSON.stringify(post));

    request.addEventListener('load', () => {
        // console.log(request.response)
        console.log("Запрос на создание новой настроенной игры");
        console.log("Запрос на создание новой настроенной игры");
        alert(request.response);
    });

};

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


// Кнопка, которая добавляет настроенного игрока/династию
// document.getElementById("add-dynasty").addEventListener("click", () => {
//     console.log("Добавляем династию");
//     // Сверим тип данных у "стартового золота"
//     if (Number(document.getElementById('choose-players').value) == 0) {
//         console.log("Игрок Админ или не выбран");
//         alert("Игрок Админ или не выбран");
//         return
//     }
//     else if (document.getElementById('name-eng').value == "") {
//         console.log("name-eng");
//         alert("Укажите название династии на английском");
//         return
//     }
//     else if (document.getElementById('name-rus').value == '') {
//         console.log("name-rus");
//         alert("Укажите название династии на русском");
//         return
//     }
//     else if (isNaN(document.getElementById('start-gold').value)) {
//         console.log("Не число");
//         alert("Стартовое золото не является числом");
//         return
//     }
//     let newDynasty = [
//         Number(document.getElementById('choose-players').value),
//         document.getElementById('name-eng').value,
//         document.getElementById('name-rus').value,
//         Number(document.getElementById('start-gold').value),
//         listPlayers[Number(document.getElementById('choose-players').value)][1] // Имя игрока
//     ];
//     console.log(document.getElementById('choose-players').value);
//     console.log(Number(document.getElementById('choose-players').value));
//     console.log(listPlayers[Number(document.getElementById('choose-players').value)][1]);
//     newGame.push(newDynasty);
//     console.log(newDynasty);
//     modal.style.display = "none";
//     console.log(newGame);
//     // Обновим список добавленных игроков
//     showPlayers(newGame);
// });