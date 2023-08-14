class CarouselImage {
    constructor(json_data=null) {
        if (!json_data) {
            this.name = ""
            this.serial_number = ""
            this.file = ""
        } else {
            this.name = json_data["fields"]["name"]
            this.url = "/media/" + json_data["fields"]["image"]
            this.serial_number = json_data["fields"]["serial_number"]
            this.file = ""
        }
    }
}

class PlaceTypePrice {
    constructor(json_data=null) {
        if (!json_data) {
            this.duration = ""
            this.term = ""
            this.time_type = ""
            this.price = ""
        } else {
            this.duration = json_data["fields"]["duration"]
            this.term = json_data["fields"]["term"]
            this.time_type = json_data["fields"]["time_type"]
            this.price = json_data["fields"]["price"]
        }
    }
}



class PlaceType {
    constructor(id, name) {
        this.id = id
        this.name = name
        this.prices = []
    }
}

