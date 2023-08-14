function update_residents_analytics(analytics) {
    update_difficult_chart(residents_count_chart, analytics["residents_count"])
    update_simple_chart(residents_place_types_chart, analytics["place_types"])
    update_simple_chart(residents_time_types_chart, analytics["time_types"])
    update_simple_chart(residents_terms_chart, analytics["terms"])
    update_difficult_chart(residents_income_chart, analytics["income"])
    update_simple_chart(residents_income_grouped_by_payment_type_chart, analytics["income_grouped_by_payment_type"])
    update_simple_chart(residents_daytime_visiting_chart, analytics["residents_visiting"]["daytime"])
    update_simple_chart(residents_nighttime_visiting_chart, analytics["residents_visiting"]["nighttime"])
    update_simple_chart(residents_day_visiting_chart, analytics["residents_visiting"]["day"])
    _set_residents_professions_list(analytics["professions"])
    _set_total_visiting_hours(analytics["total_visiting_hours"])
}


function _set_total_visiting_hours(total_visiting_hours) {
    document.getElementById("total_visiting_hours").innerText = total_visiting_hours
}


function _set_residents_professions_list(professions_list) {
    var ps_professions_list = ""
    var professions_dict = {}

    professions_list.forEach((profession) => {
        if (profession != "None") {
            if (profession in professions_dict) {
                professions_dict[profession.toLowerCase()] += 1
            } else {
                professions_dict[profession.toLowerCase()] = 1
            }
        }
    })

    for (var key in professions_dict) {
        ps_professions_list += "<p>" + key + ": " + professions_dict[key] + "</p>"
    }

    document.getElementById("professions_list").innerHTML = ps_professions_list
}
