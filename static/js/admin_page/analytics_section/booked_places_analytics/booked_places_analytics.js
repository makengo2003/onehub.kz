function update_booked_places_analytics(analytics) {
    update_chart(booked_places_count_chart, analytics["booked_places_count"])
    update_chart(booked_places_place_types_chart, analytics["place_types"])
    update_chart(booked_places_time_types_chart, analytics["time_types"])
    update_chart(booked_places_terms_chart, analytics["terms"])
}