prices_settings_app = Vue.createApp({
    data() {
        return {
            selected_place_type: null,
            place_types: [],
            is_editing: false,
            before_editing_place_type_index: 0
        }
    },
    methods: {
        get_prices_of_place_type() {
            axios.get("/site_settings/get_prices_of_place_type/", {
                params: {
                    place_type_id: this.selected_place_type["id"]
                }
            }).then((response) => {
                this.selected_place_type["prices"] = []
                if (response.data["prices"].length == 0) {
                    this.selected_place_type["prices"].push(new PlaceTypePrice())
                } else {
                    response.data["prices"].forEach((price) => {
                        this.selected_place_type["prices"].push(new PlaceTypePrice(price))
                    })
                }
                if (this.is_editing) {
                    this.cancel_price_editing()
                }
            })
        },
        open() {
            this.selected_place_type = null
            if (this.is_editing) {
                this.cancel_price_editing()
            }
            this.get_place_types()
        },
        get_place_types() {
            axios.get("/site_settings/get_place_types/").then((response) => {
                this.place_types = []

                response.data["place_types"].forEach((place_type) => {
                    this.place_types.push(new PlaceType(place_type["pk"], place_type["fields"]["name"]))
                })

                if (this.selected_place_type == null) {
                    this.selected_place_type = this.place_types[0]
                }

                if (this.place_types.length > 0) {
                    this.get_prices_of_place_type()
                }

                if (this.is_editing) {
                    this.cancel_price_editing()
                }
            })
        },
        add_new_place_type() {
            swal({
              text: 'Название нового типа места',
              content: "input",
              button: {
                text: "Добавить",
                closeModal: true,
              },
            }).then((name) => {
                if (name) {
                    axios.post("/site_settings/add_place_type/", {place_type_name: name}, {
                        headers: {
                            "X-CSRFToken": $cookies.get("csrftoken"),
                        }
                    }).then((response) => {
                        this.place_types.push(new PlaceType(response.data["id"], name))
                        if (this.is_editing) {
                            this.cancel_price_editing()
                        }
                    })
                }
            })
        },
        submit_prices() {
            axios.post("/site_settings/update_place_type_info_and_its_prices/", this.selected_place_type, {
                headers: {
                    "X-CSRFToken": $cookies.get("csrftoken"),
                }
            }).then((response) => {
                this.is_editing = false
            })
        },
        allow_price_editing() {
            this.is_editing = true
            this.before_editing_place_type_index = this.place_types.indexOf(this.selected_place_type)
            this.before_editing_place_type_data = JSON.parse(JSON.stringify(this.selected_place_type))
        },
        delete_place_type() {
            swal({
              title: "Подтвердите ваше действия. Вы точно хотите удалить этот тип места?",
              icon: "warning",
              buttons: true,
              dangerMode: true,
            }).then((will) => {
                if (will) {
                    axios.post("/site_settings/delete_place_type/", {place_type_id: this.selected_place_type.id}, {
                        headers: {
                            "X-CSRFToken": $cookies.get("csrftoken"),
                        }
                    }).then((response) => {
                        this.place_types.splice(this.place_types.indexOf(this.selected_place_type), 1)
                        this.selected_place_type = null
                    })
                }
            })
        },
        cancel_price_editing() {
            this.place_types[this.before_editing_place_type_index] = this.before_editing_place_type_data
            this.selected_place_type = this.place_types[this.before_editing_place_type_index]
            this.is_editing = false
        },
        delete_price(price) {
            this.selected_place_type["prices"].splice(this.selected_place_type["prices"].indexOf(price), 1)

        },
        add_price() {
            this.selected_place_type["prices"].push(new PlaceTypePrice())

        }
    }
})


prices_settings_app.config.compilerOptions.delimiters = ["${", "}"];
mounted_prices_settings_app = prices_settings_app.mount("#prices_settings")