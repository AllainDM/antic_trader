console.log('Стрипт странички создания игры успешно загружен');

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
const modal = document.getElementById("myModal");

// Получить кнопку, которая открывает модальное окно
const btn = document.getElementById("myBtn");

// Получить элемент <span>, который закрывает модальнок окно
const span = document.getElementsByClassName("close")[0];


// Когда пользователь нажимает на кнопку, откройте модальнок окно
btn.onclick = function() {
    modal.style.display = "block";
    // Отобразим список доступных(пока что вообще всех) игроков
    newPlayers = document.getElementById('add-players');
    newPlayers.innerHTML = "<option value='000'></option>" // Почистим от предыдущей загрузки
    listPlayers.forEach((item, id) => {
        newPlayers.innerHTML +=        
        `<option value="${id}">${item[1]}</option>`; 
    });
}

// Когда пользователь нажимает на <span> (x), закройте модальное окно
span.onclick = function() {
  modal.style.display = "none";
}

// Когда пользователь щелкает в любом месте за пределами модального, закройте его
// window.onclick = function(event) {
//   if (event.target == modal) {
//     modal.style.display = "none";
//   }
// } 
