const main_section_app = Vue.createApp({
    data() {
        return {
            search_input: "",
            current_chosen_section: "",

            api_section_get_functions: {
                "residents_list": this.get_residents_list,
                "booked_places_list": this.get_booked_places_list,
                "booking_requests_list": this.get_booking_requests_list,
                "deleted_residents_list": function(){},
                "deleted_booked_places_list": function(){},
            },

            lists_before_searching: {
                "residents_list": {
                    "is_already_searching": false,
                    "list": [],
                    "field_for_searching": "fullname",
                },
                "booked_places_list": {
                    "is_already_searching": false,
                    "list": [],
                    "field_for_searching": "consumer_fullname",
                },
                "booking_requests_list": {
                    "is_already_searching": false,
                    "list": [],
                    "field_for_searching": "consumer_fullname",
                },
                "deleted_residents_list": {
                    "is_already_searching": false,
                    "list": [],
                    "field_for_searching": "fullname",
                },
                "deleted_booked_places_list": {
                    "is_already_searching": false,
                    "list": [],
                    "field_for_searching": "consumer_fullname",
                },
            },

            place_types: [],

            residents: [],
            residents_last_obj_id: 0,

            booked_places: [],
            booked_places_last_obj_id: 0,

            deleted_residents: [],
            deleted_residents_last_obj_id: 0,

            deleted_booked_places: [],
            deleted_booked_places_last_obj_id: 0,

            booking_requests: [],
            booking_requests_last_obj_id: 0,
            new_booking_requests_count: 0,
            booking_requests_not_answered_requests_count: 0,

            which_one_add: "resident",
            add_booked_place_form: {
                "booking_request": null,
                "booking_request_id": 0,
                "payment_type": "cashless",
                "consumer_fullname": "",
                "consumer_phone_number": "",
                "time_type": "daytime",
                "starts_at": "",
                "number": "",
                "duration": 1,
                "term": "hours",
                "type": "",
                "deposit": 0,
                "discount": 0,
                "price": 0,
                "window": 0
            },
            add_resident_form: {
                "payment_type": "cashless",
                "fullname": "",
                "phone_number": "",
                "profession": "",
                "time_type": "daytime",
                "submit_function": "calculate_price",
                "starts_at": "",
                "place_number": "",
                "duration": 1,
                "term": "hours",
                "place_type": "",
                "used_discount": 0,
                "price": 0,
                "window": 0
            },

            renew_resident_form: {
                resident: 0,
                resident_id: 0,
                duration: 1,
                term: "hours",
                time_type: "daytime",
                price: 0,
                used_discount: 0,
                payment_type: "cashless",
                submit_function: "calculate_price",
                window: 0
            },
            renew_booked_place_form: {
                booked_place: 0,
                booked_place_id: 0,
                duration: 1,
                term: "hours",
                time_type: "daytime",
                discount: 0,
                price: 0,
                type: "",
                deposit: 0,
                window: 0
            },

            current_opened_deleted_booked_place: null,
            current_opened_deleted_resident: null,
            current_opened_booked_place: null,
            current_opened_resident: null,
            editable_resident_fields: {
                fullname: {
                    enabled: false,
                    value_before_editing: null
                },
                phone_number: {
                    enabled: false,
                    value_before_editing: null
                },
                profession: {
                    enabled: false,
                    value_before_editing: null
                },
                paper_count: {
                    enabled: false,
                    value_before_editing: null
                },
                locker: {
                    enabled: false,
                    value_before_editing: null
                }
            },
            editable_booked_place_fields: {
                consumer_fullname: {
                    enabled: false,
                    value_before_editing: null
                },
                consumer_phone_number: {
                    enabled: false,
                    value_before_editing: null
                },
                deposit: {
                    enabled: false,
                    value_before_editing: null
                }
            },
            booking_request_rejection_form: {
                booking_request: null,
                rejection_reason: ""
            },
            residents_order_by_column: '',
            booked_places_order_by_column: '',
            deleted_residents_starts_at: "",
            deleted_residents_ends_at: "",
            deleted_booked_places_starts_at: "",
            deleted_booked_places_ends_at: ""
        }
    },
    methods: {
        get_residents_list() {
            axios.get('/onehub_admin/get_residents_list/', {params: {last_obj_id: this.residents_last_obj_id}}).then((response) => {
                 var _search_input = this.search_input
                 this.search_input = ""
                 this.search()

                var residents_list = response.data["residents_list"]
                if (this.residents_last_obj_id == 0) {
                    residents_list.forEach(resident => this.residents.push(new Resident(resident)))
                } else {
                    residents_list.forEach(resident => this.residents.unshift(new Resident(resident)))
                }
                this.check_residents_status(this.residents.slice(0, residents_list.length))
                if (residents_list.length > 0)
                    this.residents_last_obj_id = response.data["last_obj_id"]

                if (this.residents_order_by_column == "") {
                    this.residents_order_by("expires_at")
                }

                 this.search_input = _search_input
                 this.search()
            })
        },
        get_booked_places_list() {
            axios.get('/onehub_admin/get_booked_places_list/', {params: {last_obj_id: this.booked_places_last_obj_id}}).then((response) => {
                 var _search_input = this.search_input
                 this.search_input = ""
                 this.search()

                var booked_places_list = response.data["booked_places_list"]
                if (this.booked_places_last_obj_id == 0) {
                    booked_places_list.forEach(booked_place => this.booked_places.push(new BookedPlace(booked_place)))
                } else {
                    booked_places_list.forEach(booked_place => this.booked_places.unshift(new BookedPlace(booked_place)))
                }
                this.check_booked_places_status(this.booked_places.slice(0, booked_places_list.length))
                if (booked_places_list.length > 0)
                    this.booked_places_last_obj_id = response.data["last_obj_id"]

                if (this.booked_places_order_by_column == "") {
                    this.booked_places_order_by("expires_at")
                }

                 this.search_input = _search_input
                 this.search()
            })
        },
        get_booking_requests_list() {
            axios.get('/onehub_admin/get_booking_requests_list/', {params: {last_obj_id: this.booking_requests_last_obj_id}}).then((response) => {
                 var _search_input = this.search_input
                 this.search_input = ""
                 this.search()

                if (this.booking_requests_last_obj_id == 0) {
                    var appending_function = (booking_request) => {this.booking_requests.push(booking_request)}
                } else {
                    var appending_function = (booking_request) => {this.booking_requests.unshift(booking_request)}
                }


                response.data["booking_requests_list"].forEach((booking_request) => {
                    var booking_request_obj = new BookingRequest(booking_request)

                    if (booking_request_obj.is_accepted == null) {
                        this.booking_requests_not_answered_requests_count += 1
                    }

                    appending_function(booking_request_obj)
                })

                this.new_booking_requests_count = this.booking_requests_not_answered_requests_count

                if (response.data["booking_requests_list"].length > 0)
                    this.booking_requests_last_obj_id = response.data["last_obj_id"]

                 this.search_input = _search_input
                 this.search()
            })
        },
        get_deleted_residents_list() {
            this.deleted_residents = []
            axios.get('/onehub_admin/get_deleted_residents_list/', {
                params: {
                    last_obj_id: this.deleted_residents_last_obj_id,
                    starts_at: this.deleted_residents_starts_at,
                    ends_at: this.deleted_residents_ends_at
                }
            }).then((response) => {
                 var _search_input = this.search_input
                 this.search_input = ""
                 this.search()

                if (this.deleted_residents_last_obj_id == 0) {
                    response.data["deleted_residents_list"].forEach(deleted_resident => this.deleted_residents.push(new DeletedResident(deleted_resident)))
                } else {
                    response.data["deleted_residents_list"].forEach(deleted_resident => this.deleted_residents.unshift(new DeletedResident(deleted_resident)))
                }
                if (response.data["deleted_residents_list"].length > 0)
                    this.deleted_residents_last_obj_id = response.data["last_obj_id"]

                 this.search_input = _search_input
                 this.search()
            })
        },
        get_deleted_booked_places_list() {
            this.deleted_booked_places = []
            axios.get('/onehub_admin/get_deleted_booked_places_list/', {
                params: {
                    last_obj_id: this.deleted_booked_places_last_obj_id,
                    starts_at: this.deleted_booked_places_starts_at,
                    ends_at: this.deleted_booked_places_ends_at
                }
            }).then((response) => {
                 var _search_input = this.search_input
                 this.search_input = ""
                 this.search()

                if (this.deleted_booked_places_last_obj_id == 0) {
                    response.data["deleted_booked_places_list"].forEach(deleted_booked_place => this.deleted_booked_places.push(new DeletedBookedPlace(deleted_booked_place)))
                } else {
                    response.data["deleted_booked_places_list"].forEach(deleted_booked_place => this.deleted_booked_places.unshift(new DeletedBookedPlace(deleted_booked_place)))
                }
                if (response.data["deleted_booked_places_list"].length > 0)
                    this.deleted_booked_places_last_obj_id = response.data["last_obj_id"]

                 this.search_input = _search_input
                 this.search()
            })
        },
        get_new_booking_requests_count() {
            if (this.current_chosen_section == "booking_requests_list" && this.booking_requests_last_obj_id != 0)
                this.get_booking_requests_list()
            else
                axios.get('/booking/get_new_booking_requests_count/').then((response) => {
                    this.new_booking_requests_count = response.data["new_booking_requests_count"]
                })
        },
        get_place_types() {
            axios.get('/site_settings/get_place_types/').then((response) => {
                this.place_types = []
                response.data["place_types"].forEach(place_type => this.place_types.unshift(place_type["fields"]["name"]))
                this.add_booked_place_form["type"] = response.data["place_types"][0]["fields"]["name"]
                this.add_resident_form["place_type"] = response.data["place_types"][0]["fields"]["name"]
            })
        },
        choose_section(section_name) {
            if (this.current_chosen_section != section_name) {
                if (this.current_chosen_section != "") {
                    document.getElementById(this.current_chosen_section + "_choose_section_btn").value = 0
                    document.getElementById("section_" + this.current_chosen_section).style.display = "none"
                }
                document.getElementById(section_name + "_choose_section_btn").value = 1
                document.getElementById("section_" + section_name).style.display = "block"
                this.current_chosen_section = section_name
                this.api_section_get_functions[section_name]()
                window.location.hash = ""
            }
        },
        open_section() {
            window.location.hash = ""
            this.get_place_types()
            this.get_new_booking_requests_count()
        },
        open_add_form() {
            window.location.hash = "add-zatemnenie"
            this.which_one_add = "resident"
            if (this.add_booked_place_form["booking_request_id"] != 0 || this.add_resident_form["booked_place_id"] != 0) {
                this.add_booked_place_form["booking_request"] = null
                this.add_booked_place_form["booking_request_id"] = 0
                this.add_resident_form["booked_place"] = null
                this.add_resident_form["booked_place_id"] = 0
                this.add_resident_form["submit_function"] = "calculate_price"
            }

            this.add_booked_place_form["starts_at"] = moment().format('YYYY-MM-DDTHH:mm')
            this.add_resident_form["starts_at"] = moment().format('YYYY-MM-DDTHH:mm')
        },
        calculate_booking_price(event) {
            event.preventDefault();

            axios("/booking/calculate_price/", {
                params: {
                    "booked_place_form": JSON.stringify(this.add_booked_place_form)
                }
            }).then((response) => {
                this.add_booked_place_form["price"] = response.data["price"]
            })
        },
        calculate_renewing_booked_place_price(event) {
            event.preventDefault();

            axios("/booking/calculate_price/", {
                params: {
                    "booked_place_form": JSON.stringify(this.renew_booked_place_form)
                }
            }).then((response) => {
                this.renew_booked_place_form["price"] = response.data["price"]
            })
        },
        submit_add_booked_place_form() {
            swal({
              title: "Подтвердите ваше действия. Вы точно хотите добавить забронированное место?",
              icon: "warning",
              buttons: true,
              dangerMode: true,
            })
            .then((will) => {
              if (will) {
                axios.post("/booking/add_booked_place/", this.add_booked_place_form, {
                    headers: {
                        "X-CSRFToken": $cookies.get("csrftoken"),
                    }
                }).then((response) => {
                    alert("Добавлено!")
                    window.location.hash = ""
                    if (this.current_chosen_section == "booked_places_list") {
                        this.get_booked_places_list()
                    }
                    if (this.add_booked_place_form["booking_request_id"]) {
                        this.add_booked_place_form["booking_request"].is_accepted = true
                        this.add_booked_place_form["booking_request"].answered_at = moment.tz("Asia/Almaty").format("DD.MM.YYYY, HH:mm")

                        if (this.new_booking_requests_count != 0) {
                            this.booking_requests_not_answered_requests_count -= 1
                            this.new_booking_requests_count = this.booking_requests_not_answered_requests_count
                        }
                    }
                    this.add_booked_place_form = {
                        "booking_request": null,
                        "booking_request_id": 0,
                        "payment_type": "cashless",
                        "consumer_fullname": "",
                        "consumer_phone_number": "",
                        "time_type": "daytime",
                        "starts_at": moment().format('YYYY-MM-DDTHH:mm'),
                        "number": "",
                        "duration": 1,
                        "term": "hours",
                        "type": this.place_types[0],
                        "deposit": 0,
                        "discount": 0,
                        "price": 0,
                        "window": 0
                    }
                }).catch((error) => {
                    if (error.response) {
                        if (error.response.status == 400) {
                            alert("Ошибка в заполнении формы")
                        } else if (error.response.status == 409) {
                            alert("Место занято")
                        } else {
                            alert("Неизвестная ошибка. Проверьте выбранные Тарифы!")
                        }
                    }
                })
              }
            });
        },
        submit_add_resident_form() {
            if (this.add_resident_form["submit_function"] == "calculate_price") {
                axios.get("/resident/calculate_resident_adding_price/", {params: this.add_resident_form}).then((response) => {
                    this.add_resident_form["price"] = response.data["price"]

                    if (this.add_resident_form["booked_place_id"] != 0) {
                        this.add_resident_form["price"] -= this.add_resident_form["booked_place"]["deposit"]
                    }

                    this.add_resident_form["submit_function"] = "add_resident"
                }).catch((error) => {
                    if (error.response) {
                        if (error.response.status == 400) {
                            alert("Ошибка в заполнении формы")
                        } else if (error.response.status == 409) {
                            alert("Место занято")
                        } else {
                            alert("Неизвестная ошибка. Проверьте выбранные Тарифы!")
                        }
                    }
                })
            } else {
                swal({
                  title: "Подтвердите ваше действия. Вы точно хотите добавить резидента?",
                  icon: "warning",
                  buttons: true,
                  dangerMode: true,
                }).then((will) => {
                    if (will) {
                        axios.post("/resident/add_resident/", this.add_resident_form, {
                            headers: {
                                "X-CSRFToken": $cookies.get("csrftoken"),
                            }
                        }).then((response) => {
                            alert("Добавлено!")
                            window.location.hash = ""
                            if (this.current_chosen_section == "residents_list") {
                                this.get_residents_list()
                            }
                            if (this.add_resident_form["booked_place_id"]) {
                                this.booked_places.splice(this.booked_places.indexOf(this.add_resident_form["booked_place"]), 1)
                            }
                            this.add_resident_form = {
                                "payment_type": "cashless",
                                "fullname": "",
                                "phone_number": "",
                                "profession": "",
                                "time_type": "daytime",
                                "submit_function": "calculate_price",
                                "starts_at": moment().format('YYYY-MM-DDTHH:mm'),
                                "place_number": "",
                                "duration": 1,
                                "term": "hours",
                                "place_type": this.place_types[0],
                                "used_discount": 0,
                                "price": 0,
                                "window": 0
                            }
                        }).catch((error) => {
                            if (error.response) {
                                if (error.response.status == 400) {
                                    alert("Ошибка в заполнении формы")
                                } else if (error.response.status == 409) {
                                    alert("Место занято")
                                } else {
                                    alert("Неизвестная ошибка. Проверьте выбранные Тарифы!")
                                }
                            }
                        })
                    }
                })
            }
        },
        update_resident_visited_today_status(resident) {
            if (resident.visited_today) {
                resident.visited_times++
            }
            else {
                resident.visited_times--

                if (resident.visited_times < 0) {
                    resident.visited_times = 0
                }
            }

            axios.post("/resident/update_resident_visited_today_status/", {"resident_id": resident.id}, {headers: {
                        "X-CSRFToken": $cookies.get("csrftoken"),
                    }})
        },
        update_booked_place_info(booked_place, field, value) {
            axios.post("/booking/update_booked_place_info/",
                {"booked_place_id": booked_place.id, "field_for_updating": field, "new_value": value}, {
                    headers: {
                        "X-CSRFToken": $cookies.get("csrftoken"),
                    }
                }).then((response) => {
                    if (field in this.editable_booked_place_fields) {
                        this.editable_booked_place_fields[field]["enabled"] = false
                    }
                    booked_place[field] = value
                })
        },
        update_resident_info(resident, field, value) {
            if (field == "locker") {
                for (var i = 0; i < this.residents.length; i++) {
                    if (this.residents[i] != resident) {
                        if (this.residents[i].locker == value) {
                            alert(this.residents[i].fullname + " занял(a) локер " + value)
                            return
                        }
                    }
                }
            }
            axios.post("/resident/update_resident_info/",
                {"resident_id": resident.id, "field_for_updating": field, "new_value": value}, {
                    headers: {
                        "X-CSRFToken": $cookies.get("csrftoken"),
                    }
                }).then((response) => {
                    if (field in this.editable_resident_fields) {
                        this.editable_resident_fields[field]["enabled"] = false
                    }
                    resident[field] = value
                })
        },
        open_resident_details_window(resident) {
            window.location.hash = "resident_details_window"
            this.current_opened_resident = resident
            this.editable_resident_fields = {
                fullname: {
                    enabled: false,
                    value_before_editing: null
                },
                phone_number: {
                    enabled: false,
                    value_before_editing: null
                },
                profession: {
                    enabled: false,
                    value_before_editing: null
                },
                paper_count: {
                    enabled: false,
                    value_before_editing: null
                },
                locker: {
                    enabled: false,
                    value_before_editing: null
                }
            }
        },
        open_booked_place_details_window(booked_place) {
            window.location.hash = "booked_place_details_window"
            this.current_opened_booked_place = booked_place
            this.editable_booked_place_fields = {
                consumer_fullname: {
                    enabled: false,
                    value_before_editing: null
                },
                consumer_phone_number: {
                    enabled: false,
                    value_before_editing: null
                },
                deposit: {
                    enabled: false,
                    value_before_editing: null
                }
            }
        },
        open_deleted_resident_details_window(deleted_resident) {
            window.location.hash = "deleted_resident_details_window"
            this.current_opened_deleted_resident = deleted_resident
        },
        open_deleted_booked_place_details_window(deleted_booked_place) {
            window.location.hash = "deleted_booked_place_details_window"
            this.current_opened_deleted_booked_place = deleted_booked_place
        },
        enable_booked_place_field(field, value_before_editing) {
            field["enabled"] = true
            field["value_before_editing"] = value_before_editing
        },
        enable_resident_field(field, value_before_editing) {
            field["enabled"] = true
            field["value_before_editing"] = value_before_editing
        },
        cancel_booked_place_field_editing(field) {
            this.editable_booked_place_fields[field]["enabled"] = false
            this.current_opened_booked_place[field] = this.editable_booked_place_fields[field]["value_before_editing"]
        },
        cancel_resident_field_editing(field) {
            this.editable_resident_fields[field]["enabled"] = false
            this.current_opened_resident[field] = this.editable_resident_fields[field]["value_before_editing"]
        },
        delete_booked_place(booked_place) {
            swal({
              title: "Подтвердите ваше действия. Вы точно хотите удалить забронированное место?",
              icon: "warning",
              buttons: true,
              dangerMode: true,
            })
            .then((will) => {
              if (will) {
                axios.post("/booking/delete_booked_place/", {"booked_place_id": booked_place.id}, {
                    headers: {
                        "X-CSRFToken": $cookies.get("csrftoken"),
                    }
                }).then((response) => {
                    this.booked_places.splice(this.booked_places.indexOf(booked_place), 1)
                    window.location.hash = ""
                })
              }
            });
        },
        delete_resident(resident) {
            swal({
              title: "Подтвердите ваше действия. Вы точно хотите удалить резидента?",
              icon: "warning",
              buttons: true,
              dangerMode: true,
            })
            .then((will) => {
              if (will) {
                axios.post("/resident/delete_resident/", {"resident_id": resident.id}, {
                    headers: {
                        "X-CSRFToken": $cookies.get("csrftoken"),
                    }
                }).then((response) => {
                    this.residents.splice(this.residents.indexOf(resident), 1)
                    window.location.hash = ""
                })
              }
            });
        },
        open_renew_resident_form(resident) {
            window.location.hash = "renew_resident-zatemnenie"
            this.renew_resident_form = {
                resident: resident,
                resident_id: resident.id,
                duration: 1,
                term: "hours",
                time_type: "daytime",
                price: 0,
                used_discount: 0,
                payment_type: "cashless",
                submit_function: "calculate_price",
                window: 0
            }
        },
        submit_renew_resident_form() {
            if (this.renew_resident_form["submit_function"] == "calculate_price") {
                axios.get("/resident/calculate_resident_renewing_price/", {params: this.renew_resident_form}).then((response) => {
                    this.renew_resident_form["price"] = response.data["price"]
                    this.renew_resident_form["submit_function"] = "add_resident"
                }).catch((error) => {
                    if (error.response) {
                        if (error.response.status == 400) {
                            alert("Ошибка в заполнении формы")
                        } else if (error.response.status == 409) {
                            alert("Место занято")
                        } else {
                            alert("Неизвестная ошибка. Проверьте выбранные Тарифы!")
                        }
                    }
                })
            } else {
                swal({
                  title: "Подтвердите ваше действия. Вы точно хотите продлить дата просрочки резидента?",
                  icon: "warning",
                  buttons: true,
                  dangerMode: true,
                }).then((will) => {
                    if (will) {
                        axios.post("/resident/renew_resident/", this.renew_resident_form, {
                            headers: {
                                "X-CSRFToken": $cookies.get("csrftoken"),
                            }
                        }).then((response) => {
                            alert("Дата просрочки успешно продлен!")
                            window.location.hash = ""
                            if (this.current_chosen_section == "residents_list") {
                                this.get_residents_list()
                            }
                            this.residents.splice(this.residents.indexOf(this.renew_resident_form["resident"]), 1)
                        }).catch((error) => {
                            if (error.response) {
                                if (error.response.status == 400) {
                                    alert("Ошибка в заполнении формы")
                                } else if (error.response.status == 409) {
                                    alert("Место занято")
                                } else {
                                    alert("Неизвестная ошибка. Проверьте выбранные Тарифы!")
                                }
                            }
                        })
                    }
                })
            }
        },
        open_renew_booked_place_form(booked_place) {
            window.location.hash = "renew_booked_place-zatemnenie"
            this.renew_booked_place_form = {
                booked_place: booked_place,
                booked_place_id: booked_place.id,
                duration: 1,
                term: "hours",
                time_type: "daytime",
                discount: 0,
                price: 0,
                type: booked_place.type,
                deposit: 0,
                window: 0
            }
        },
        submit_renew_booked_place_form() {
            swal({
                title: "Подтвердите ваше действия. Вы точно хотите продлить дата просрочки бронирование?",
                icon: "warning",
                buttons: true,
                dangerMode: true,
            }).then((will) => {
                if (will) {
                    axios.post("/booking/renew_booked_place/", this.renew_booked_place_form, {
                        headers: {
                            "X-CSRFToken": $cookies.get("csrftoken"),
                        }
                    }).then((response) => {
                        alert("Дата просрочки успешно продлен!")
                        window.location.hash = ""
                        if (this.current_chosen_section == "booked_places_list") {
                            this.get_booked_places_list()
                        }
                        this.booked_places.splice(this.booked_places.indexOf(this.renew_booked_place_form["booked_place"]), 1)
                   }).catch((error) => {
                        if (error.response) {
                            if (error.response.status == 400) {
                                alert("Ошибка в заполнении формы")
                            } else if (error.response.status == 409) {
                                alert("Место занято")
                            } else {
                                alert("Неизвестная ошибка. Проверьте выбранные Тарифы!")
                            }
                        }
                    })
                }
            })
        },
        from_booking_request_to_booked_place(booking_request) {
            window.location.hash = "add-zatemnenie"
            this.which_one_add = "booked_place"
            this.add_booked_place_form["booking_request"] = booking_request
            this.add_booked_place_form["booking_request_id"] = booking_request.id
            this.add_booked_place_form["consumer_fullname"] = booking_request.consumer_fullname
            this.add_booked_place_form["consumer_phone_number"] = booking_request.consumer_phone_number
        },
        from_booked_place_to_resident(booked_place) {
            window.location.hash = "add-zatemnenie"
            this.which_one_add = "resident"
            this.add_resident_form["booked_place_id"] = booked_place.id
            this.add_resident_form["booked_place"] = booked_place
            this.add_resident_form["fullname"] = booked_place.consumer_fullname
            this.add_resident_form["phone_number"] = booked_place.consumer_phone_number
            this.add_resident_form["place_number"] = booked_place.number
            this.add_resident_form["place_type"] = booked_place.type
            this.add_resident_form["duration"] = booked_place.duration
            this.add_resident_form["term"] = booked_place.term
            this.add_resident_form["time_type"] = booked_place.time_type
            this.add_resident_form["used_discount"] = booked_place.discount
            this.add_resident_form["window"] = booked_place.window
            this.add_resident_form["price"] = booked_place.price - booked_place.deposit
            this.add_resident_form["starts_at"] = moment(booked_place.starts_at, "DD.MM.YYYY, HH:mm").format("yyyy-MM-DDTHH:mm")
            this.add_resident_form["submit_function"] = "calculate_price"
        },
        open_booking_request_rejection_form(booking_request) {
            window.location.hash = "booking_request_rejection_form-zatemnenie"
            this.booking_request_rejection_form = {
                booking_request: booking_request,
                rejection_reason: ""
            }
        },
        submit_booking_request_rejection_form() {
            axios.post("/booking/make_booking_request_rejected/", {
                booking_request_id: this.booking_request_rejection_form["booking_request"].id,
                rejection_reason: this.booking_request_rejection_form["rejection_reason"]
            }, {
                headers: {
                    "X-CSRFToken": $cookies.get("csrftoken"),
                }
            }).then((response) => {
                window.location.hash = ""
                this.booking_request_rejection_form["booking_request"].is_accepted = false
                this.booking_request_rejection_form["booking_request"].answered_at = moment.tz("Asia/Almaty").format("DD.MM.YYYY, HH:mm")

                if (this.new_booking_requests_count != 0) {
                    this.booking_requests_not_answered_requests_count -= 1
                    this.new_booking_requests_count = this.booking_requests_not_answered_requests_count
                }
            })
        },
        check_booked_places_status(booked_places) {
            booked_places.forEach((booked_place) => {
                if (booked_place.status == "active" || booked_place.status == "expired") {
                    var status = ""

                    var booked_place_expires_at = moment(booked_place.expires_at, "DD.MM.YYYY, HH:mm")
                    var datetime_now = moment(moment.tz("Asia/Almaty").format("DD.MM.YYYY, HH:mm"), "DD.MM.YYYY, HH:mm")

                    if (booked_place_expires_at.isAfter(datetime_now)) {
                        status = "active"
                    } else {
                        var duration = moment.duration(datetime_now.diff(booked_place_expires_at));
                        var minutes = duration.asMinutes();
                        
                        if (minutes >= 5) {
                            status = "deleted"
                            this.booked_places.splice(this.booked_places.indexOf(booked_place), 1)
                        } else {
                            status = "expired"
                        }
                    }

                    if (status != booked_place.status) {
                        this.update_booked_place_info(booked_place, "status", status)
                    }
                } else {
                    this.booked_places.splice(this.booked_places.indexOf(booked_place), 1)
                }
            })
        },
        check_residents_status(residents) {
            residents.forEach((resident) => {
                if (resident.status == "active" || resident.status == "expired") {
                    var status = ""
                
                    var resident_expires_at = moment(resident.expires_at, "DD.MM.YYYY, HH:mm")
                    var datetime_now = moment(moment.tz("Asia/Almaty").format("DD.MM.YYYY, HH:mm"), "DD.MM.YYYY, HH:mm")

                    if (resident_expires_at.isAfter(datetime_now)) {
                        status = "active"
                    } else {
                        var duration = moment.duration(datetime_now.diff(resident_expires_at));
                        var minutes = duration.asMinutes();
                        
                        if (minutes >= 5) {
                            status = "deleted"
                            this.residents.splice(this.residents.indexOf(resident), 1)
                        } else {
                            status = "expired"
                        }
                    }

                    if (status != resident.status) {
                        this.update_resident_info(resident, "status", status)
                    }
                } else {
                    this.residents.splice(this.residents.indexOf(resident), 1)
                }
            })
        },
        residents_order_by(field) {
            if (this.residents_order_by_column != field && this.residents_order_by_column != '-' + field) {
                this.residents_order_by_column = field
            } else {
                if (this.residents_order_by_column[0] == '-') {
                    this.residents_order_by_column = field
                } else {
                    this.residents_order_by_column = "-" + field
                }
            }

            this.residents.sort((resident1, resident2) => {
                if (this.residents_order_by_column[0] == "-") {
                    return resident1[field] == resident2[field] ? 0 : resident1.compare(field, resident2[field], true)
                }
                return resident1[field] == resident2[field] ? 0 : resident1.compare(field, resident2[field])
            })
        },
        booked_places_order_by(field) {
            if (this.booked_places_order_by_column != field && this.booked_places_order_by_column != '-' + field) {
                this.booked_places_order_by_column = field
            } else {
                if (this.booked_places_order_by_column[0] == '-') {
                    this.booked_places_order_by_column = field
                } else {
                    this.booked_places_order_by_column = "-" + field
                }
            }

            this.booked_places.sort((booked_place1, booked_place2) => {
                if (this.booked_places_order_by_column[0] == "-") {
                    return booked_place1[field] == booked_place2[field] ? 0 : booked_place1.compare(field, booked_place2[field], true)
                }
                return booked_place1[field] == booked_place2[field] ? 0 : booked_place1.compare(field, booked_place2[field])
            })
        },
        repeat_order(order) {
            this.add_booked_place_form = {
                "payment_type": order["payment_type"],
                "time_type": order["time_type"],
                "starts_at": moment(order.starts_at, "DD.MM.YYYY, HH:mm").format("yyyy-MM-DDTHH:mm"),
                "duration": order["duration"],
                "term": order["term"],
            }
            this.add_resident_form = {
                "payment_type": order["payment_type"],
                "time_type": order["time_type"],
                "starts_at": moment(order.starts_at, "DD.MM.YYYY, HH:mm").format("yyyy-MM-DDTHH:mm"),
                "duration": order["duration"],
                "term": order["term"],
            }

            if (order instanceof Resident || order instanceof DeletedResident) {
                this.add_resident_form["fullname"] = order["fullname"]
                this.add_resident_form["phone_number"] = order["phone_number"]
                this.add_resident_form["profession"] = order["profession"]
                this.add_resident_form["submit_function"] = "calculate_price"
                this.add_resident_form["place_number"] = order["place_number"]
                this.add_resident_form["place_type"] = order["place_type"]
                this.add_resident_form["used_discount"] = order["used_discount"]
                this.add_resident_form["price"] = 0
                this.add_resident_form["window"] = order["window"]

                this.add_booked_place_form["consumer_fullname"] = order["fullname"]
                this.add_booked_place_form["consumer_phone_number"] = order["phone_number"]
                this.add_booked_place_form["number"] = order["place_number"]
                this.add_booked_place_form["type"] = order["place_type"]
                this.add_booked_place_form["deposit"] = 0
                this.add_booked_place_form["discount"] = 0
                this.add_booked_place_form["price"] = 0
                this.add_booked_place_form["window"] = order["window"]

                this.open_add_form()
            } else {
                this.add_resident_form["fullname"] = order["consumer_fullname"]
                this.add_resident_form["phone_number"] = order["consumer_phone_number"]
                this.add_resident_form["profession"] = ""
                this.add_resident_form["submit_function"] = "calculate_price"
                this.add_resident_form["place_number"] = order["number"]
                this.add_resident_form["place_type"] = order["type"]
                this.add_resident_form["window"] = order["window"]
                this.add_resident_form["used_discount"] = 0
                this.add_resident_form["price"] = 0

                this.add_booked_place_form["consumer_fullname"] = order["consumer_fullname"]
                this.add_booked_place_form["consumer_phone_number"] = order["consumer_phone_number"]
                this.add_booked_place_form["number"] = order["number"]
                this.add_booked_place_form["type"] = order["type"]
                this.add_booked_place_form["deposit"] = order["deposit"]
                this.add_booked_place_form["discount"] = order["discount"]
                this.add_booked_place_form["window"] = order["window"]
                this.add_booked_place_form["price"] = 0

                this.open_add_form()
                this.which_one_add = "booked_place"
            }
        },
        export_to_excel(excels_urls) {
            for (var i = 0; i < excels_urls.length; i++) {
                axios({
                  url: excels_urls[i],
                  method: 'GET',
                  responseType: 'blob', // important
                }).then((response) => {
                  const url = window.URL.createObjectURL(new Blob([response.data]));
                  const link = document.createElement('a');
                  link.href = url;
                  link.setAttribute('download', response.headers["content-disposition"].slice(18, -1));
                  document.body.appendChild(link);
                  link.click();
                  link.remove();
                });
            }
        },
        search() {
            if (this.search_input == "") {
                if (this.lists_before_searching[this.current_chosen_section]["is_already_searching"]) {
                    this[this.current_chosen_section.replace("_list", "")] = this.lists_before_searching[this.current_chosen_section]["list"]
                }
                this.lists_before_searching[this.current_chosen_section]["list"] = []
                this.lists_before_searching[this.current_chosen_section]["is_already_searching"] = false
            } else {
                if (!this.lists_before_searching[this.current_chosen_section]["is_already_searching"]) {
                    this.lists_before_searching[this.current_chosen_section]["list"] = this[this.current_chosen_section.replace("_list", "")]
                    this.lists_before_searching[this.current_chosen_section]["is_already_searching"] = true
                }

                var result_list = []

                this.lists_before_searching[this.current_chosen_section]["list"].forEach((item) => {
                    if (item[this.lists_before_searching[this.current_chosen_section]["field_for_searching"]].trim().toLowerCase().includes(this.search_input.trim().toLowerCase())) {
                        result_list.push(item)
                    }
                })

                this[this.current_chosen_section.replace("_list", "")] = result_list

            }
        },
        booking_search_by_fullname() {
            axios.get("/booking/search_by_fullname/?fullname=" + this.add_booked_place_form.consumer_fullname.trim()).then((response) => {
                this.add_booked_place_form.consumer_phone_number = response.data["phone_number"]
            })
        },
        booking_search_by_phone_number() {
            axios.get("/booking/search_by_phone_number/?phone_number=" + this.add_booked_place_form.consumer_phone_number.trim()).then((response) => {
                this.add_booked_place_form.consumer_fullname = response.data["fullname"]
            })
        },
        resident_search_by_fullname() {
            axios.get("/resident/search_by_fullname/?fullname=" + this.add_resident_form.fullname.trim()).then((response) => {
                this.add_resident_form.phone_number = response.data["phone_number"]
                this.add_resident_form.profession = response.data["profession"]
            })
        },
        resident_search_by_phone_number() {
            axios.get("/resident/search_by_phone_number/?phone_number=" + this.add_resident_form.phone_number.trim()).then((response) => {
                this.add_resident_form.fullname = response.data["fullname"]
                this.add_resident_form.profession = response.data["profession"]
            })
        },
    },
    beforeMount() {
        setInterval(this.get_new_booking_requests_count, 60000)
        setInterval(() => { this.check_booked_places_status(this.booked_places) }, 600000)
        setInterval(() => { this.check_residents_status(this.residents) }, 600000)
    }
})

main_section_app.config.compilerOptions.delimiters = ["${", "}"];
