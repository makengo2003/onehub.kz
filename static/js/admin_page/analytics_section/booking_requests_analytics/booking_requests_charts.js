var booking_requests_count = document.getElementById("booking_requests_count")
let booking_requests_count_chart = new Chart(booking_requests_count, {
    type: 'bar',
    data: {},
    options: get_chart_options('Количество запросов'),
})


var booking_requests_place_types = document.getElementById("booking_requests_place_types")
let booking_requests_place_types_chart = new Chart(booking_requests_place_types, {
    type: 'pie',
    data: {},
    options: get_chart_options('Тип места')
})

