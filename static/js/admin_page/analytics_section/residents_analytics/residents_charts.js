var residents_count = document.getElementById("residents_count")
let residents_count_chart = new Chart(residents_count, {
    type: "line",
    data: {
        labels: [],
        datasets: [
            {
                label: "Количество",
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
                text: 'Количество продаж'
            },
            tooltip: {
                callbacks: {
                    label: function(context) { return get_percentage(context) }
                }
            }
        }
    }
})


var residents_place_types = document.getElementById("residents_place_types")
let residents_place_types_chart = new Chart(residents_place_types, {
    type: "pie",
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


var residents_time_types = document.getElementById("residents_time_types")
let residents_time_types_chart = new Chart(residents_time_types, {
    type: "pie",
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


var residents_terms = document.getElementById("residents_terms")
let residents_terms_chart = new Chart(residents_terms, {
    type: "pie",
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


var residents_income = document.getElementById("residents_income")
let residents_income_chart = new Chart(residents_income, {
    type: "line",
    data: {
        labels: [],
        datasets: [
            {
                label: "Доход",
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
                text: 'Доходы'
            },
            tooltip: {
                callbacks: {
                    label: function(context) { return get_percentage(context) }
                }
            }
        }
    }
})


var residents_income_grouped_by_payment_type = document.getElementById("residents_income_grouped_by_payment_type")
let residents_income_grouped_by_payment_type_chart = new Chart(residents_income_grouped_by_payment_type, {
    type: "pie",
    data: {
        labels: [],
        datasets: [
            {
                label: "Тг",
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


var residents_daytime_visiting = document.getElementById("residents_daytime_visiting")
let residents_daytime_visiting_chart = new Chart(residents_daytime_visiting, {
    type: "pie",
    data: {
        labels: ["Ожидалось", "На самом деле пришли"],
        datasets: [
            {
                label: "Количество посещаемости",
                data: [],
                backgroundColor: Object.values(CHART_COLORS),
            },
        ]
    },
    options: {
        plugins: {
            legend: {
                position: 'top',
            },
            title: {
                display: true,
                text: 'Посещаемость "День"'
            },
            tooltip: {
                callbacks: {
                    label: function(context) { return get_percentage(context) }
                }
            }
        }
    }
})


var residents_nighttime_visiting = document.getElementById("residents_nighttime_visiting")
let residents_nighttime_visiting_chart = new Chart(residents_nighttime_visiting, {
    type: "pie",
    data: {
        labels: ["Ожидалось", "На самом деле пришли"],
        datasets: [
            {
                label: "Количество посещаемости",
                data: [],
                backgroundColor: Object.values(CHART_COLORS),
            },
        ]
    },
    options: {
        plugins: {
            legend: {
                position: 'top',
            },
            title: {
                display: true,
                text: 'Посещаемость "Ночь"'
            },
            tooltip: {
                callbacks: {
                    label: function(context) { return get_percentage(context) }
                }
            }
        }
    }
})


var residents_day_visiting = document.getElementById("residents_day_visiting")
let residents_day_visiting_chart = new Chart(residents_day_visiting, {
    type: "pie",
    data: {
        labels: ["Ожидалось", "На самом деле пришли"],
        datasets: [
            {
                label: "Количество посещаемости",
                data: [],
                backgroundColor: Object.values(CHART_COLORS),
            },
        ]
    },
    options: {
        plugins: {
            legend: {
                position: 'top',
            },
            title: {
                display: true,
                text: 'Посещаемость "Сутки"'
            },
            tooltip: {
                callbacks: {
                    label: function(context) { return get_percentage(context) }
                }
            }
        }
    }
})
