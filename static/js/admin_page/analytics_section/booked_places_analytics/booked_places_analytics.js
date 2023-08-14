function update_booked_places_analytics(analytics) {
    update_difficult_chart(booked_places_deposits_chart, analytics["deposits"])
    update_difficult_chart(booked_places_count_chart, analytics["booked_places_count"])
    update_simple_chart(booked_places_place_types_chart, analytics["place_types"])
    update_simple_chart(booked_places_time_types_chart, analytics["time_types"])
    update_simple_chart(booked_places_terms_chart, analytics["terms"])
    update_simple_chart(booked_places_deposits_grouped_by_payment_type_chart, analytics["deposits_grouped_by_payment_type"])
}