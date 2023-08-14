var booked_places_count = document.getElementById("booked_places_count")
let booked_places_count_chart = new Chart(booked_places_count, {
    type: 'bar',
    data: {},
    options: get_chart_options('Количество забронированных')
})


var booked_places_place_types = document.getElementById("booked_places_place_types")
let booked_places_place_types_chart = new Chart(booked_places_place_types, {
    type: "pie",
    data: {},
    options: get_chart_options('Тип места')
})


var booked_places_time_types = document.getElementById("booked_places_time_types")
let booked_places_time_types_chart = new Chart(booked_places_time_types, {
    type: "pie",
    data: {},
    options: get_chart_options('Время дня')
})


var booked_places_terms = document.getElementById("booked_places_terms")
let booked_places_terms_chart = new Chart(booked_places_terms, {
    type: "pie",
    data: {},
    options: get_chart_options('Показатель по срокам')
})
