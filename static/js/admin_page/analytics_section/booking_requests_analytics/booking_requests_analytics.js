function update_booking_requests_analytics(analytics) {
    update_simple_chart(booking_requests_place_types_chart, analytics["place_types"])
    update_difficult_chart(booking_requests_count_chart, analytics["booking_requests_count"], ["total"])
    _set_total_booking_requests_count(analytics["booking_requests_count"]["total"])
    _set_response_times(analytics["response_times"])
    _set_rejection_reasons_list(analytics["rejection_reasons_list"])
}

function _set_total_booking_requests_count(total_booking_requests_count_grouped_by_month) {
    var total = 0;
    for (var year in total_booking_requests_count_grouped_by_month) {
        for (var month in total_booking_requests_count_grouped_by_month[year]) {
            total += total_booking_requests_count_grouped_by_month[year][month]
        }
    }
    document.querySelector("#analytics_section #total_booking_requests_count").innerText = total;
}

function _set_response_times(response_times) {
    document.getElementById("max_response_time").innerText = response_times["max"]
    document.getElementById("min_response_time").innerText = response_times["min"]
    document.getElementById("avg_response_time").innerText = response_times["avg"]
}

function _set_rejection_reasons_list(rejection_reasons_list) {
    var ps_rejection_reasons_list = ""
    rejection_reasons_list.forEach((rejection_reason) => {
        if (rejection_reason != "None")
            ps_rejection_reasons_list += "<p>" + rejection_reason + "</p>"
    })
    document.getElementById("rejection_reasons_list").innerHTML = ps_rejection_reasons_list
}
