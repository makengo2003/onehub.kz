var residents_count = document.getElementById("residents_count")
let residents_count_chart = new Chart(residents_count, {
    type: "line",
    data: {},
    options: get_chart_options('Количество продаж')
})


var residents_place_types = document.getElementById("residents_place_types")
let residents_place_types_chart = new Chart(residents_place_types, {
    type: "pie",
    data: {},
    options: get_chart_options('Тип места')
})


var residents_time_types = document.getElementById("residents_time_types")
let residents_time_types_chart = new Chart(residents_time_types, {
    type: "pie",
    data: {},
    options: get_chart_options('Время дня')
})


var residents_terms = document.getElementById("residents_terms")
let residents_terms_chart = new Chart(residents_terms, {
    type: "pie",
    data: {},
    options: get_chart_options('Показатель по срокам')
})


var residents_income = document.getElementById("residents_income")
let residents_income_chart = new Chart(residents_income, {
    type: "line",
    data: {},
    options: get_chart_options('Доходы')
})


var residents_income_grouped_by_payment_type = document.getElementById("residents_income_grouped_by_payment_type")
let residents_income_grouped_by_payment_type_chart = new Chart(residents_income_grouped_by_payment_type, {
    type: "pie",
    data: {},
    options: get_chart_options('Тип оплаты')
})


var residents_daytime_visiting = document.getElementById("residents_daytime_visiting")
let residents_daytime_visiting_chart = new Chart(residents_daytime_visiting, {
    type: "pie",
    data: {},
    options: get_chart_options('Посещаемость "День"')
})


var residents_nighttime_visiting = document.getElementById("residents_nighttime_visiting")
let residents_nighttime_visiting_chart = new Chart(residents_nighttime_visiting, {
    type: "pie",
    data: {},
    options: get_chart_options('Посещаемость "Ночь"')
})


var residents_day_visiting = document.getElementById("residents_day_visiting")
let residents_day_visiting_chart = new Chart(residents_day_visiting, {
    type: "pie",
    data: {},
    options: get_chart_options('Посещаемость "Сутки"')
})
