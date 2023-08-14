login_change_app = Vue.createApp({
    data() {
        return {
            form: {
                username: null,
                old_password: "",
                new_password1: "",
                new_password2: "",
                errors: []
            }
        }
    },
    methods: {
        login_change_request() {
            this.form.errors = []
            axios.post("/onehub_admin/change_username_and_password/", this.form, {
                headers: {
                    "X-CSRFToken": $cookies.get("csrftoken"),
                }
            }).then((response) => {
                swal("Пароль успешно изменен")
                window.location.hash = '#'
                document.getElementById("request_user_username").innerText = this.form["username"]
                this.form = {
                    username: this.form["username"],
                    old_password: "",
                    new_password1: "",
                    new_password2: "",
                    errors: []
                }
            }).catch((error) => {
                if (error.response) {
                    if (error.response.status == 400) {
                        for (var key in error.response.data) {
                            for (var err in error.response.data[key]) {
                                this.form.errors.push(error.response.data[key][err])
                            }
                        }
                    } else {
                        swal("Упс", "Что-то пошло не так!")
                    }
                }
            })
        }
    },
    mounted() {
        this.form["username"] = username
    }
})

login_change_app.config.compilerOptions.delimiters = ["${", "}"];
mounted_login_change_app = login_change_app.mount("#login_change")