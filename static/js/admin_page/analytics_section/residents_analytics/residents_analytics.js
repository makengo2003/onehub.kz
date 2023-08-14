function update_residents_analytics(analytics) {
    update_chart(residents_count_chart, analytics["residents_count"])
    update_chart(residents_place_types_chart, analytics["place_types"])
    update_chart(residents_time_types_chart, analytics["time_types"])
    update_chart(residents_terms_chart, analytics["terms"])
    update_chart(residents_income_chart, analytics["income"])
    update_chart(residents_income_grouped_by_payment_type_chart, analytics["income_grouped_by_payment_type"])
    update_chart(residents_daytime_visiting_chart, analytics["residents_daytime_visiting"])
    update_chart(residents_nighttime_visiting_chart, analytics["residents_nighttime_visiting"])
    update_chart(residents_day_visiting_chart, analytics["residents_day_visiting"])

    // total_visiting_hours
    document.getElementById("total_visiting_hours").innerText = analytics["total_visiting_hours"]

    // profession list
    _set_professions_list(analytics["professions"])
}

function _set_professions_list(professions) {
    var ps_professions_list = ""
    var professions_dict = {}

    professions.forEach((profession) => {
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