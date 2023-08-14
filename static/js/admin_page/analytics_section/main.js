var analytics_starts_at, analytics_ends_at
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


function get_analytics(event) {
    event.preventDefault()

    axios.get("/analytics/get_analytics/", {
        params: {
            starts_at: analytics_starts_at,
            ends_at: analytics_ends_at
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


function update_simple_chart(chart, data) {
    var labels = []
    var chart_data = []

    for (var label in data) {
        labels.push(label)
        chart_data.push(data[label])
    }

    chart.data.labels = labels
    chart.data.datasets[0].data = chart_data
    chart.update()
}


function update_difficult_chart(chart, data, exclude_keys=[]) {
    var i = 0

    for (var key in data) {
        if (exclude_keys.includes(key)) {
            continue
        }

        var period_as_dict = _get_inputted_analytics_period_as_dict()
        _fill_period_as_dict_with_data(period_as_dict, data[key])
        chart.data.datasets[i].data = _get_chart_data_from_period_as_dict(period_as_dict)

        i++
    }

    chart.data.labels = _get_labels_from_period_as_dict(period_as_dict)
    chart.update()
}


function _get_inputted_analytics_period_as_dict() {
    var months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
    var starts_at = new Date(analytics_starts_at)
    var ends_at = new Date(analytics_ends_at)
    var period_as_dict = {}

    for (var i = starts_at.getFullYear(); i <= ends_at.getFullYear(); i++) {
        var months_starts_at = 0
        var months_ends_at = 0

        if (i == starts_at.getFullYear()) {
            months_starts_at = starts_at.getMonth()

            if (i == ends_at.getFullYear()) {
                months_ends_at = ends_at.getMonth()
            } else {
                months_ends_at = 11
            }
        } else if (i == ends_at.getFullYear()) {
            months_starts_at = 0
            months_ends_at = ends_at.getMonth()
        } else {
            months_starts_at = 0
            months_ends_at = 11
        }

        period_as_dict[i] = {}

        for (var j = months_starts_at; j <= months_ends_at; j++) {
            period_as_dict[i][j] = {
                label: months[j] + " " + i + "y.",
                data: 0
            }
        }
    }

    return period_as_dict
}


function _fill_period_as_dict_with_data(period_as_dict, data) {
    for (var year in data) {
        for (var month in data[year]) {
            period_as_dict[year][month]["data"] = data[year][month]
        }
    }
}


function _get_chart_data_from_period_as_dict(period_as_dict) {
    var chart_data = []
    for (var year in period_as_dict) {
        for (var month in period_as_dict[year]) {
            chart_data.push(period_as_dict[year][month]["data"])
        }
    }
    return chart_data
}


function _get_labels_from_period_as_dict(period_as_dict) {
    var labels = []
    for (var year in period_as_dict) {
        for (var month in period_as_dict[year]) {
            labels.push(period_as_dict[year][month]["label"])
        }
    }
    return labels
}
