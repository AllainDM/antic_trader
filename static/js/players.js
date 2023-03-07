console.log('Стрипт странички списка игроков успешно загружен');

const list = document.querySelector('.list');

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
                showPlayers(response);
                return response;
            };
        } else {
            console.log("Ответ от сервера не получен");
        }
    });
    request.send();

};

reqUsers();

// Отображение списка игроков

function showPlayers(players) {
    console.log(players);
    list.innerHTML = `<span>Игроки:</span>`;  // Добавим подсказку
    players.forEach((item, id) => {
        // chooseList.innerHTML += `<div class="menu-btn menu-buttons-choose"><a href="{{url_for('game')}}">Игра номер: ${item}</a></div>`;
        list.innerHTML +=         
        `<div class="show-list">
            ${item[1]}
        </div>`;  //   ид: ${id}
    });

    // Определяем позицию кнопки и "создаем" соответсвующий приказ
    document.querySelectorAll(".show-list").forEach((btn, i) => {
        btn.addEventListener('click', () => {
            console.log(`Вы выбрали игрока: ${players[i][1]}`);  // -1

        });
    });
};