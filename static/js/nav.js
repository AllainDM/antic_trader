console.log('Стрипт навигации успешно загружен');
// Переключения в меню

function hiddenAllMenu() {  //Скрыть все доп меню
    document.getElementById("menu-buttons-colony").setAttribute('style','display:none');
    document.getElementById("menu-buttons-diplomaty").setAttribute('style','display:none');
    document.getElementById("menu-buttons-trade").setAttribute('style','display:none');
};

function hiddenAllAllMenu() {  //Скрыть все меню включая основное
    document.getElementById("menu-buttons-colony").setAttribute('style','display:none');
    document.getElementById("menu-buttons-diplomaty").setAttribute('style','display:none');
    document.getElementById("menu-buttons-trade").setAttribute('style','display:none');
    document.getElementById("main-menu-buttons").setAttribute('style','display:none');

};

function hiddenMenu() {  //Скрыть все меню кроме основного
    document.getElementById("menu-buttons-colony").setAttribute('style','display:none');
    document.getElementById("menu-buttons-diplomaty").setAttribute('style','display:none');
    document.getElementById("menu-buttons-trade").setAttribute('style','display:none');
    document.getElementById("menu-buttons").setAttribute('style','visibility:visible');
};

function exitToMainMenuButtons() {  // Выйти в главное меню
    hiddenAllMenu();
    document.getElementById("main-menu-buttons").setAttribute('style','display:flex');
};


// Тут видимо навешиваем обытие выхода в главное меню для всех кнопок "выход"
const exitButtons = document.querySelectorAll('.menu-exit');

exitButtons.forEach((i) => {
    i.addEventListener('click', () => {
        hiddenAllMenu();
        document.getElementById("main-menu-buttons").setAttribute('style','display:flex');
    });
});

document.getElementById('menu-colony').addEventListener('click', () => {
    hiddenAllMenu();
    document.getElementById("main-menu-buttons").setAttribute('style','display:none');
    document.getElementById("menu-buttons-colony").setAttribute('style','visibility:visible');
});

document.getElementById('menu-trade').addEventListener('click', () => {
    hiddenAllMenu();
    document.getElementById("main-menu-buttons").setAttribute('style','display:none');
    document.getElementById("menu-buttons-trade").setAttribute('style','visibility:visible');
});

// document.getElementById('menu-diplomaty').addEventListener('click', () => {
//     hiddenAllMenu();
//     document.getElementById("main-menu-buttons").setAttribute('style','display:none');
//     document.getElementById("menu-buttons-diplomaty").setAttribute('style','visibility:visible');
// });