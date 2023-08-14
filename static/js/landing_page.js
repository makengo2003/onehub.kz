window.location.hash = "";

function onsubmit_of_leave_booking_request_form(event) {
    event.preventDefault()
    var formData = new FormData(this)

    axios.post("/leave_booking_request/", formData, {
        headers: {
            "X-CSRFToken": $cookies.get("csrftoken"),
        }
    }).then((response) => {
        if (response.data["success"]) {
                swal({
                  title: "Ваша заявка принята. Ждите ответа от наших менеджеров))",
                  button: "Окей",
                }).then(() => {
                    window.location.reload()
                })
            } else {
                swal({
                  title: 'Номер должен начинаться с "+7" и введите настоящий номер',
                  button: "Окей",
                })
            }
    }).catch((error) => {
        if (error.response) {
            swal({
              title: 'Возникла какая-та ошибка, не удалось оставить заявку. Перезагрузите страницу или свяжитесь с нами',
              button: "Окей",
            })
        }
    })
}

$("#leave_booking_request_form1").submit(onsubmit_of_leave_booking_request_form)
$("#leave_booking_request_form2").submit(onsubmit_of_leave_booking_request_form)





$("#login_form form").submit(function (event) {
    event.preventDefault()
    var formData = new FormData(this)

    axios.post("login/", formData, {
        headers: {
            "X-CSRFToken": $cookies.get("csrftoken"),
        }
    }).then((response) => {
        if (response.data["success"]) {
            window.location.href = '/admin/'
        } else {
            swal({
              title: 'Введите правильные данные аккаунта',
              button: "Окей",
            })
        }
    }).catch((error) => {
        if (error.response) {
          swal({
              title: 'Возникла какая-та ошибка, не удалось войти в сайт. Перезагрузите страницу или свяжитесь с нами',
              button: "Окей",
            })
        }
    })
})


function open_prices() {
    document.getElementById("prices_block").style.display = "block"
    document.getElementById("main_page_block").style.display = "none"
}

function close_prices() {
    document.getElementById("prices_block").style.display = "none"
    document.getElementById("main_page_block").style.display = "block"
}

place_type_options = document.getElementById("booking_form").getElementsByTagName("option")
select_input = document.getElementById("booking_form").getElementsByTagName("select")[0]
//function open_leave_booking_request_form_window(place_type) {
//    window.location.hash = 'booking_form';
//
//    if (place_type != "all" && place_type != "meeting_room") {
//        select_input.parentElement.style.display = "none"
//        select_input.value = place_type
//    } else {
//        select_input.parentElement.style.display = "initial"
//        select_input.value = place_type_options[0].value
//
//        for (var i = 0; i < place_type_options.length; i++) {
//            if (place_type == "all") {
//                place_type_options[i].style.display = "initial"
//            }
//            else {
//                if (place_type_options[i].getAttribute("data-place_type") == place_type) {
//                    place_type_options[i].style.display = "initial"
//                    select_input.value = place_type_options[i].value
//                } else {
//                    place_type_options[i].style.display = "none"
//                }
//            }
//        }
//    }
//}