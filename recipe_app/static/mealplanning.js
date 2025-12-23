const STORAGE_KEY = "mealHeaders";

function getStoredHeaders() {
    return JSON.parse(localStorage.getItem(STORAGE_KEY)) || {};
}

function saveHeader(headerId, text) {
    const headers = getStoredHeaders();
    headers[headerId] = text;
    localStorage.setItem(STORAGE_KEY, JSON.stringify(headers));
}

document.addEventListener('DOMContentLoaded', () => {
    const headers = getStoredHeaders();

    Object.entries(headers).forEach(([id, text]) => {
        const headerEl = document.getElementById(id);
        if (headerEl) {
            headerEl.innerHTML = text;
        }
    });
});

const dropdowns = document.querySelectorAll("select");
dropdowns.forEach(dropdown => {
    dropdown.style.display = "none";
});

const addRecipes = document.querySelectorAll(".btn");

addRecipes.forEach(recipe => {
    recipe.addEventListener('click', (event) => {
        const clickedButtonID = event.target.id;

        switch(clickedButtonID) {
            case "Sunday-recipe":
                const sun = document.querySelector('select[id*=recipe-categories-sun]');
                const sunSubmit = document.querySelector("button[id*=submit-sun]");
                sun.style.display = "block";
                sunSubmit.style.display = "block";
                
                break;
            case 'Monday-recipe':
                const mon = document.querySelector('select[id*=recipe-categories-mon]');
                const monSubmit = document.querySelector("button[id*=submit-mon]");
                mon.style.display = "block";
                monSubmit.style.display = "block";
                break;
            case 'Tuesday-recipe':
                const tues = document.querySelector('select[id*=recipe-categories-tues]');
                const tuesSubmit = document.querySelector("button[id*=submit-tues]");
                tues.style.display = "block";
                tuesSubmit.style.display = "block";
                break;
            case 'Wednesday-recipe':
                const wed = document.querySelector('select[id*=recipe-categories-wed]');
                const wedSubmit = document.querySelector("button[id*=submit-wed]");
                wed.style.display = "block";
                wedSubmit.style.display = "block";
                break;
            case 'Thursday-recipe':
                const thur = document.querySelector('select[id*=recipe-categories-thur]');
                const thurSubmit = document.querySelector("button[id*=submit-thur]");
                thur.style.display = "block";
                thurSubmit.style.display = "block";
                break;
            case 'Friday-recipe':
                const fri = document.querySelector('select[id*=recipe-categories-fri]');
                const friSubmit = document.querySelector("button[id*=submit-fri]");
                fri.style.display = "block";
                friSubmit.style.display = "block";
                break;
            case 'Saturday-recipe':
                const sat = document.querySelector('select[id*=recipe-categories-sat]');
                const satSubmit = document.querySelector("button[id*=submit-sat]");
                sat.style.display = "block";
                satSubmit.style.display = "block";
                break;
        }
    }); 
});

function toggleMeal(day) {
    switch (day){
        case 'Sun':
            let mealValSun = document.getElementById("recipe-categories-sun").value;
            let dropdownBreakfastSun = document.querySelector("select[id*=dropdown-content-sun-b]");
            let dropdownLunchSun = document.getElementById("dropdown-content-sun-l");
            let dropdownDinnerSun = document.getElementById("dropdown-content-sun-d");

            if (mealValSun == "Breakfast") {
                dropdownBreakfastSun.style.display = "block";
            }
            else {
                dropdownBreakfastSun.style.display = "none";
            }

            if (mealValSun == "Lunch") {
                dropdownLunchSun.style.display = "block";
            }
            else {
                dropdownLunchSun.style.display = "none";
            }

            if (mealValSun == "Dinner") {
                dropdownDinnerSun.style.display = "block";
            }
            else {
                dropdownDinnerSun.style.display = "none";
            }
        case 'Mon':
            let mealValMon = document.getElementById("recipe-categories-mon").value;
            let dropdownBreakfastMon = document.getElementById("dropdown-content-mon-b");
            let dropdownLunchMon = document.getElementById("dropdown-content-mon-l");
            let dropdownDinnerMon = document.getElementById("dropdown-content-mon-d");

            if (mealValMon == "Breakfast") {
                dropdownBreakfastMon.style.display = "block";
            }
            else {
                dropdownBreakfastMon.style.display = "none";
            }

            if (mealValMon == "Lunch") {
                dropdownLunchMon.style.display = "block";
            }
            else {
                dropdownLunchMon.style.display = "none";
            }

            if (mealValMon == "Dinner") {
                dropdownDinnerMon.style.display = "block";
            }
            else {
                dropdownDinnerMon.style.display = "none";
            }
        case 'Tues':
            let mealValTues = document.getElementById("recipe-categories-tues").value;
            let dropdownBreakfastTues = document.getElementById("dropdown-content-tues-b");
            let dropdownLunchTues = document.getElementById("dropdown-content-tues-l");
            let dropdownDinnerTues = document.getElementById("dropdown-content-tues-d");

            if (mealValTues == "Breakfast") {
                dropdownBreakfastTues.style.display = "block";
            }
            else {
                dropdownBreakfastTues.style.display = "none";
            }

            if (mealValTues == "Lunch") {
                dropdownLunchTues.style.display = "block";
            }
            else {
                dropdownLunchTues.style.display = "none";
            }

            if (mealValTues == "Dinner") {
                dropdownDinnerTues.style.display = "block";
            }
            else {
                dropdownDinnerTues.style.display = "none";
            }
        case 'Wed':
            let mealValWed = document.getElementById("recipe-categories-wed").value;
            let dropdownBreakfastWed = document.getElementById("dropdown-content-wed-b");
            let dropdownLunchWed = document.getElementById("dropdown-content-wed-l");
            let dropdownDinnerWed = document.getElementById("dropdown-content-wed-d");

            if (mealValWed == "Breakfast") {
                dropdownBreakfastWed.style.display = "block";
            }
            else {
                dropdownBreakfastWed.style.display = "none";
            }

            if (mealValWed == "Lunch") {
                dropdownLunchWed.style.display = "block";
            }
            else {
                dropdownLunchWed.style.display = "none";
            }

            if (mealValWed == "Dinner") {
                dropdownDinnerWed.style.display = "block";
            }
            else {
                dropdownDinnerWed.style.display = "none";
            }
        case 'Thur':
            let mealValThur = document.getElementById("recipe-categories-thur").value;
            let dropdownBreakfastThur = document.getElementById("dropdown-content-thur-b");
            let dropdownLunchThur = document.getElementById("dropdown-content-thur-l");
            let dropdownDinnerThur = document.getElementById("dropdown-content-thur-d");

            if (mealValThur == "Breakfast") {
                dropdownBreakfastThur.style.display = "block";
            }
            else {
                dropdownBreakfastThur.style.display = "none";
            }

            if (mealValThur == "Lunch") {
                dropdownLunchThur.style.display = "block";
            }
            else {
                dropdownLunchThur.style.display = "none";
            }

            if (mealValThur == "Dinner") {
                dropdownDinnerThur.style.display = "block";
            }
            else {
                dropdownDinnerThur.style.display = "none";
            }
        case 'Fri':
            let mealValFri = document.getElementById("recipe-categories-fri").value;
            let dropdownBreakfastFri = document.getElementById("dropdown-content-fri-b");
            let dropdownLunchFri = document.getElementById("dropdown-content-fri-l");
            let dropdownDinnerFri = document.getElementById("dropdown-content-fri-d");

            if (mealValFri == "Breakfast") {
                dropdownBreakfastFri.style.display = "block";
            }
            else {
                dropdownBreakfastFri.style.display = "none";
            }

            if (mealValFri == "Lunch") {
                dropdownLunchFri.style.display = "block";
            }
            else {
                dropdownLunchFri.style.display = "none";
            }

            if (mealValFri == "Dinner") {
                dropdownDinnerFri.style.display = "block";
            }
            else {
                dropdownDinnerFri.style.display = "none";
            }
        case 'Sat':
            let mealValSat = document.getElementById("recipe-categories-sat").value;
            let dropdownBreakfastSat = document.getElementById("dropdown-content-sat-b");
            let dropdownLunchSat = document.getElementById("dropdown-content-sat-l");
            let dropdownDinnerSat = document.getElementById("dropdown-content-sat-d");

            if (mealValSat == "Breakfast") {
                dropdownBreakfastSat.style.display = "block";
            }
            else {
                dropdownBreakfastSat.style.display = "none";
            }

            if (mealValSat == "Lunch") {
                dropdownLunchSat.style.display = "block";
            }
            else {
                dropdownLunchSat.style.display = "none";
            }

            if (mealValSat == "Dinner") {
                dropdownDinnerSat.style.display = "block";
            }
            else {
                dropdownDinnerSat.style.display = "none";
            }
    }
}

function clearMealPlan() {
    const HEADER_REGEX_IDS = /^(sun|mon|tues|wed|thur|fri|sat)-header-(b|l|d)$/;
    const headers = Array.from(document.querySelectorAll('h5'))
        .filter(header => HEADER_REGEX_IDS.test(header.id));
    
    headers.forEach(header => {
        header.innerHTML = "No recipe added yet";
    });

    localStorage.clear();
}