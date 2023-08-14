var booking_requests_count = document.getElementById("booking_requests_count")
let booking_requests_count_chart = new Chart(booking_requests_count, {
    type: 'bar',
    data: {
        labels: [],
        datasets: [
            {
                label: 'Принято',
                data: [],
            },
            {
                label: 'Отказано',
                data: [],
            }
        ]
    },
    options: {
        responsive: true,
        plugins: {
            legend: {
                position: 'top',
            },
            title: {
                display: true,
                text: 'Количество запросов'
            },
            tooltip: {
                callbacks: {
                    label: function(context) { return get_percentage(context) }
                }
            }
        }
    },
})


var booking_requests_place_types = document.getElementById("booking_requests_place_types")
let booking_requests_place_types_chart = new Chart(booking_requests_place_types, {
    type: 'pie',
    data: {
        labels: [],
        datasets: [
            {
                label: "Количество",
                data: [],
                backgroundColor: Object.values(CHART_COLORS),
            }
        ]
    },
    options: {
        plugins: {
            legend: {
                position: 'top',
            },
            title: {
                display: true,
                text: 'Тип места'
            },
            tooltip: {
                callbacks: {
                    label: function(context) { return get_percentage(context) }
                }
            }
        }
    }
})

