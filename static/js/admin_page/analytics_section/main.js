var current_selected_period = null

const CHART_COLORS = {
    c: '#4c6d89',
    c0: '#4f8cc1',
    c1: '#249fc6',
    c2: '#22C0F1',
    c3: '#93B6ED',
    c4: '#169ED9',
    c5: '#33ffe3',
    c6: '#30C591)',
    red: 'rgb(255, 99, 132)',
    orange: 'rgb(255, 159, 64)',
    yellow: 'rgb(255, 205, 86)',
    green: 'rgb(75, 192, 192)',
    blue: 'rgb(54, 162, 235)',
    purple: 'rgb(153, 102, 255)',
    grey: 'rgb(201, 203, 207)'
};

function get_chart_options(title) {
    return {
        responsive: true,
        plugins: {
            legend: {
                position: 'top',
            },
            title: {
                display: true,
                text: title
            },
            tooltip: {
                callbacks: {
                    label: function(context) { return get_percentage(context) }
                }
            }
        }
    }
}

function get_analytics(period) {
    if (!current_selected_period) {
        current_selected_period = document.getElementById(period + "_analytics_period_select_btn")
        current_selected_period.className = "selected_analytics_period_btn"
    } else {
        current_selected_period.className = "select_analytics_period_btn"
        current_selected_period = document.getElementById(period + "_analytics_period_select_btn")
        current_selected_period.className = "selected_analytics_period_btn"
    }

    axios.get("/analytics/get_analytics/", {
        params: {
            period_label: period
        }
    }).then((response) => {
        update_booking_requests_analytics(response.data["booking_requests_analytics"])
        update_booked_places_analytics(response.data["booked_places_analytics"])
        update_residents_analytics(response.data["residents_analytics"])

        document.getElementById("analytics").style.display = "block"
    })
}

function get_percentage(context) {
    let label = context.dataset.label || '';

    if (label) {
        label += ': ';
    }

    var total = 0
    context.chart.data.datasets.forEach((dataset) => {
        dataset.data.forEach((data) => {
            total += data
        })
    })

    label += context.raw + ' (' + Math.floor(context.raw / total * 100) + '%)';
    return label;
}

function update_chart(chart, data) {
    chart.data.labels = data["labels"]
    chart.data.datasets = []

    if (chart.type == "pie") {
        data["datasets"][0]["backgroundColor"] = Object.values(CHART_COLORS)
    }

    chart.data.datasets = data["datasets"]
    chart.update()
}
