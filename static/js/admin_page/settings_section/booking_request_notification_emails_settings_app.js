booking_request_notification_emails_settings_app = Vue.createApp({
    data() {
        return {
            emails: "",
            is_editing: false,
            emails_before_editing: ""
        }
    },
    methods: {
        get_emails() {
            this.emails = ""
            axios.get("/site_settings/get_booking_request_notification_emails/").then((response) => {
                response.data["booking_request_notification_emails"].forEach(email => this.emails += email + "\n")
            })
        },
        save_emails() {
            var emails = this.emails.split("\n")
            axios.post("/site_settings/save_booking_request_notification_emails/", {emails: emails}, {
                headers: {
                    "X-CSRFToken": $cookies.get("csrftoken"),
                }
            }).then((response) => {
                this.is_editing = false
            })
        },
        cancel_emails_editing() {
            this.emails = this.emails_before_editing
            this.is_editing = false
        }
    }
})

booking_request_notification_emails_settings_app.config.compilerOptions.delimiters = ["${", "}"];
mounted_booking_request_notification_emails_settings_app = booking_request_notification_emails_settings_app.mount("#booking_request_notification_emails_settings")
