var booked_places_count = document.getElementById("booked_places_count")
let booked_places_count_chart = new Chart(booked_places_count, {
    type: 'bar',
    data: {
        labels: [],
        datasets: [
            {
                label: "Общая кол.",
                data: []
            },
            {
                label: "Стал резидентом",
                data: []
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
                text: 'Количество забронированных'
            },
            tooltip: {
                callbacks: {
                    label: function(context) { return get_percentage(context) }
                }
            }
        }
    }
})


var booked_places_place_types = document.getElementById("booked_places_place_types")
let booked_places_place_types_chart = new Chart(booked_places_place_types, {
    type: "pie",
    data: {
        labels: [],
        datasets: [
            {
                label: "Количество",
                data: [],
                backgroundColor: Object.values(CHART_COLORS),
            }
        ],
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


var booked_places_time_types = document.getElementById("booked_places_time_types")
let booked_places_time_types_chart = new Chart(booked_places_time_types, {
    type: "pie",
    data: {
        labels: [],
        datasets: [
            {
                label: "Количество",
                data: [],
                backgroundColor: Object.values(CHART_COLORS),
            }
        ],
    },
    options: {
        plugins: {
            legend: {
                position: 'top',
            },
            title: {
                display: true,
                text: 'Время дня'
            },
            tooltip: {
                callbacks: {
                    label: function(context) { return get_percentage(context) }
                }
            }
        }
    }
})


var booked_places_terms = document.getElementById("booked_places_terms")
let booked_places_terms_chart = new Chart(booked_places_terms, {
    type: "pie",
    data: {
        labels: [],
        datasets: [
            {
                label: "Количество",
                data: [],
                backgroundColor: Object.values(CHART_COLORS),
            }
        ],
    },
    options: {
        plugins: {
            legend: {
                position: 'top',
            },
            title: {
                display: true,
                text: 'Показатель по срокам'
            },
            tooltip: {
                callbacks: {
                    label: function(context) { return get_percentage(context) }
                }
            }
        }
    }
})


var booked_places_deposits = document.getElementById("booked_places_deposits_line")
let booked_places_deposits_chart = new Chart(booked_places_deposits, {
    type: "line",
    data: {
        labels: [],
        datasets: [
            {
                label: "Тг",
                data: []
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
                text: 'Депозиты'
            },
            tooltip: {
                callbacks: {
                    label: function(context) { return get_percentage(context) }
                }
            }
        }
    }
})


var booked_places_deposits_grouped_by_payment_type = document.getElementById("booked_places_deposits_grouped_by_payment_type")
let booked_places_deposits_grouped_by_payment_type_chart = new Chart(booked_places_deposits_grouped_by_payment_type, {
    type: "pie",
    data: {
        labels: [],
        datasets: [
            {
                label: "Депозит",
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
                text: 'Тип оплаты'
            },
            tooltip: {
                callbacks: {
                    label: function(context) { return get_percentage(context) }
                }
            }
        }
    }
})
