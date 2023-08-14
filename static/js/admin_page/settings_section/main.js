var current_opened_settings_section = "set_menu"
var sections_get_data_functions = {
    "carousel_settings": mounted_carousel_settings_app.get_carousel_images,
    "booking_request_notification_emails_settings": mounted_booking_request_notification_emails_settings_app.get_emails,
    "prices_settings": mounted_prices_settings_app.open,
}

function open_settings_section(settings_section_name) {
    document.getElementById(current_opened_settings_section).style.display = "none"
    document.getElementById(settings_section_name).style.display = "block"
    current_opened_settings_section = settings_section_name
    if (current_opened_settings_section != "set_menu")
        sections_get_data_functions[current_opened_settings_section]()
}