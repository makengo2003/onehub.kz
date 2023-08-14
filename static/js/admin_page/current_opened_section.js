var current_opened_section = null

var last_opened_subsection_of_section = {
	"main_section_app": null,
	"site_settings_section_app": null,
	"analytics_section": "null",
	"admin_actions_section": "null",
}

var default_subsection_of_section = {
	"main_section_app": "residents_list",
	"site_settings_section_app": "set_menu",
	"analytics_section": "",
	"admin_actions_section": "",
}

var sections_open_function = {
	"main_section_app": mounted_main_section_app.open_section,
	"site_settings_section_app": () => {},
	"analytics_section": () => {},
	"admin_actions_section": () => {},
}

var subsections_open_function = {
	"main_section_app": mounted_main_section_app.choose_section,
	"site_settings_section_app": open_settings_section,
	"analytics_section": () => {},
	"admin_actions_section": () => {},
}


function set_current_opened_section_and_subsection_to_url_params(section, subsection=null) {
	var params = new URLSearchParams(window.location.search)
	params.set("section", section)

	if (subsection) {
		params.set("subsection", subsection)
	} else {
		params.delete("subsection")
	}

	if (history.pushState) {
	    var new_url = window.location.protocol + "//" + window.location.host + window.location.pathname + '?' + params.toString();
	    window.history.pushState({path: new_url},'',new_url);
	}
}


function get_current_opened_section_and_subsection_from_url_params() {
	var params = new URLSearchParams(window.location.search)
	return [params.get("section"), params.get("subsection")]
}


function open_section(section) {
	if (current_opened_section != section) {
		if (current_opened_section != null) {
	        document.getElementById(current_opened_section).style.display = "none"
		}
        document.getElementById(section).style.display = "block"
        
        sections_open_function[section]()
        
        current_opened_section = section

        if (last_opened_subsection_of_section[section] == null) {
        	open_subsection(default_subsection_of_section[section])
        }

        set_current_opened_section_and_subsection_to_url_params(section, last_opened_subsection_of_section[section])
    }
}


function open_subsection(subsection) {
	if (last_opened_subsection_of_section[current_opened_section] != subsection) {
		if (last_opened_subsection_of_section[current_opened_section] != null) {
        	document.getElementById(last_opened_subsection_of_section[current_opened_section]).style.display = "none"
		}
        document.getElementById(subsection).style.display = "block"
        
        subsections_open_function[current_opened_section](subsection)
        set_current_opened_section_and_subsection_to_url_params(current_opened_section, subsection)

        last_opened_subsection_of_section[current_opened_section] = subsection
    }
}


var prev_opened_section_and_subsection = get_current_opened_section_and_subsection_from_url_params()

if (prev_opened_section_and_subsection[0] != null) {
	open_section(prev_opened_section_and_subsection[0])
	open_subsection(prev_opened_section_and_subsection[1])
} else {
	open_section("main_section_app")
	open_subsection("residents_list")
}

document.getElementById("sidebar_" + current_opened_section + "_choose_btn").checked = true
