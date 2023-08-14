class Resident {
    constructor(json_data) {
        this.id = json_data["pk"]
        this.fullname = json_data["fields"]["fullname"]
        this.phone_number = json_data["fields"]["phone_number"]
        this.profession = json_data["fields"]["profession"]
        this.starts_at = moment(json_data["fields"]["starts_at"]).utc().format("DD.MM.YYYY, HH:mm")
        this.expires_at = moment(json_data["fields"]["expires_at"]).utc().format("DD.MM.YYYY, HH:mm")
        this.created_at = moment(json_data["fields"]["created_at"]).utc().format("DD.MM.YYYY, HH:mm")
        this.status = json_data["fields"]["status"]
        this.used_discount = json_data["fields"]["used_discount"]
        this.price = json_data["fields"]["price"]
        this.payment_type = json_data["fields"]["payment_type"]
        this.place_number = json_data["fields"]["place_number"]
        this.place_type = json_data["fields"]["place_type"]
        this.paper_count = json_data["fields"]["paper_count"]
        this.duration = json_data["fields"]["duration"]
        this.term = json_data["fields"]["term"]
        this.time_type = json_data["fields"]["time_type"]
        this.visited_today = json_data["fields"]["visited_today"]
    }

    compare(field, compare_value, reverse=false) {
        if (field == "expires_at") {
            var this_expires_at = moment(this.expires_at, "DD.MM.YYYY, HH:mm")
            var compare_expires_at = moment(compare_value, "DD.MM.YYYY, HH:mm")
            return this_expires_at.isAfter(compare_expires_at) ? (reverse ? -1 : 1) : (reverse ? 1 : -1)
        } else {
            return this[field] > compare_value ? (reverse ? -1 : 1) : (reverse ? 1 : -1)
        }
    }

    payment_type_text() {
        if (this.payment_type == "cash")
            return "Наличный"
        else if (this.payment_type == "cashless")
            return "Безналичный"
        else if (this.payment_type == "barter")
            return "Бартер"
    }
    term_text() {
        if (this.term == "hours")
            return "Час"
        else if (this.term == "days")
            return "День"
        else if (this.term == "weeks")
            return "Неделя"
        else if (this.term == "months fix")
            return "Месяц Fix"
        else if (this.term == "months flex")
            return "Месяц Flex"
    }
    time_type_text() {
        if (this.time_type == "day")
            return "Сутки"
        else if (this.time_type == "daytime")
            return "День"
        else if (this.time_type == "nighttime")
            return "Ночь"
    }
}

class BookedPlace {
    constructor(json_data) {
        this.id = json_data["pk"]
        this.consumer_fullname = json_data["fields"]["consumer_fullname"]
        this.consumer_phone_number = json_data["fields"]["consumer_phone_number"]
        this.starts_at = moment(json_data["fields"]["starts_at"]).utc().format("DD.MM.YYYY, HH:mm")
        this.expires_at = moment(json_data["fields"]["expires_at"]).utc().format("DD.MM.YYYY, HH:mm")
        this.created_at = moment(json_data["fields"]["created_at"]).utc().format("DD.MM.YYYY, HH:mm")
        this.status = json_data["fields"]["status"]
        this.deposit = json_data["fields"]["deposit"]
        this.is_paid = json_data["fields"]["is_paid"]
        this.payment_type = json_data["fields"]["payment_type"]
        this.number = json_data["fields"]["number"]
        this.type = json_data["fields"]["type"]
        this.duration = json_data["fields"]["duration"]
        this.term = json_data["fields"]["term"]
        this.time_type = json_data["fields"]["time_type"]
    }

    compare(field, compare_value, reverse=false) {
        if (field == "expires_at") {
            var this_expires_at = moment(this.expires_at, "DD.MM.YYYY, HH:mm")
            var compare_expires_at = moment(compare_value, "DD.MM.YYYY, HH:mm")
            return this_expires_at.isAfter(compare_expires_at) ? (reverse ? -1 : 1) : (reverse ? 1 : -1)
        } else {
            return this[field] > compare_value ? (reverse ? -1 : 1) : (reverse ? 1 : -1)
        }
    }

    payment_type_text() {
        if (this.payment_type == "cash")
            return "Наличный"
        else if (this.payment_type == "cashless")
            return "Безналичный"
        else if (this.payment_type == "barter")
            return "Бартер"
    }
    term_text() {
        if (this.term == "hours")
            return "Час"
        else if (this.term == "days")
            return "День"
        else if (this.term == "weeks")
            return "Неделя"
        else if (this.term == "months fix")
            return "Месяц Fix"
        else if (this.term == "months flex")
            return "Месяц Flex"
    }
    time_type_text() {
        if (this.time_type == "day")
            return "Сутки"
        else if (this.time_type == "daytime")
            return "День"
        else if (this.time_type == "nighttime")
            return "Ночь"
    }
}

class BookingRequest {
    constructor(json_data) {
        this.id = json_data["pk"]
        this.consumer_fullname = json_data["fields"]["consumer_fullname"]
        this.consumer_phone_number = json_data["fields"]["consumer_phone_number"]
        this.place_type = json_data["fields"]["place_type"]
        this.created_at = moment(json_data["fields"]["created_at"]).utc().format("DD.MM.YYYY, HH:mm")
        this.answered_at = moment(json_data["fields"]["answered_at"]).utc().format("DD.MM.YYYY, HH:mm")
        this.is_accepted = json_data["fields"]["is_accepted"]
    }
}

class DeletedResident {
    constructor(json_data) {
        this.id = json_data["pk"]
        this.fullname = json_data["fields"]["fullname"]
        this.phone_number = json_data["fields"]["phone_number"]
        this.profession = json_data["fields"]["profession"]
        this.starts_at = moment(json_data["fields"]["starts_at"]).utc().format("DD.MM.YYYY, HH:mm")
        this.expires_at = moment(json_data["fields"]["expires_at"]).utc().format("DD.MM.YYYY, HH:mm")
        this.deleted_at = moment(json_data["fields"]["deleted_at"]).utc().format("DD.MM.YYYY, HH:mm")
        this.created_at = moment(json_data["fields"]["created_at"]).utc().format("DD.MM.YYYY, HH:mm")
        this.used_discount = json_data["fields"]["used_discount"]
        this.price = json_data["fields"]["price"]
        this.payment_type = json_data["fields"]["payment_type"]
        this.place_number = json_data["fields"]["place_number"]
        this.place_type = json_data["fields"]["place_type"]
        this.paper_count = json_data["fields"]["paper_count"]
        this.duration = json_data["fields"]["duration"]
        this.term = json_data["fields"]["term"]
        this.time_type = json_data["fields"]["time_type"]
    }

    payment_type_text() {
        if (this.payment_type == "cash")
            return "Наличный"
        else if (this.payment_type == "cashless")
            return "Безналичный"
        else if (this.payment_type == "barter")
            return "Бартер"
    }
    term_text() {
        if (this.term == "hours")
            return "Час"
        else if (this.term == "days")
            return "День"
        else if (this.term == "weeks")
            return "Неделя"
        else if (this.term == "months fix")
            return "Месяц Fix"
        else if (this.term == "months flex")
            return "Месяц Flex"
    }
    time_type_text() {
        if (this.time_type == "day")
            return "Сутки"
        else if (this.time_type == "daytime")
            return "День"
        else if (this.time_type == "nighttime")
            return "Ночь"
    }
}

class DeletedBookedPlace {
    constructor(json_data) {
        this.id = json_data["pk"]
        this.consumer_fullname = json_data["fields"]["consumer_fullname"]
        this.consumer_phone_number = json_data["fields"]["consumer_phone_number"]
        this.starts_at = moment(json_data["fields"]["starts_at"]).utc().format("DD.MM.YYYY, HH:mm")
        this.expires_at = moment(json_data["fields"]["expires_at"]).utc().format("DD.MM.YYYY, HH:mm")
        this.deleted_at = moment(json_data["fields"]["deleted_at"]).utc().format("DD.MM.YYYY, HH:mm")
        this.created_at = moment(json_data["fields"]["created_at"]).utc().format("DD.MM.YYYY, HH:mm")
        this.deposit = json_data["fields"]["deposit"]
        this.is_paid = json_data["fields"]["is_paid"]
        this.payment_type = json_data["fields"]["payment_type"]
        this.number = json_data["fields"]["number"]
        this.type = json_data["fields"]["type"]
        this.duration = json_data["fields"]["duration"]
        this.term = json_data["fields"]["term"]
        this.time_type = json_data["fields"]["time_type"]
    }

    payment_type_text() {
        if (this.payment_type == "cash")
            return "Наличный"
        else if (this.payment_type == "cashless")
            return "Безналичный"
        else if (this.payment_type == "barter")
            return "Бартер"
    }
    term_text() {
        if (this.term == "hours")
            return "Час"
        else if (this.term == "days")
            return "День"
        else if (this.term == "weeks")
            return "Неделя"
        else if (this.term == "months fix")
            return "Месяц Fix"
        else if (this.term == "months flex")
            return "Месяц Flex"
    }
    time_type_text() {
        if (this.time_type == "day")
            return "Сутки"
        else if (this.time_type == "daytime")
            return "День"
        else if (this.time_type == "nighttime")
            return "Ночь"
    }
}
