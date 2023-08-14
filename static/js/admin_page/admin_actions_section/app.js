const admin_actions_app = Vue.createApp({
    data() {
        return {
            starts_at: null,
            ends_at: null,
            admin_actions: [],
            current_opened_admin_action: null,
        }
    },
    methods: {
        get_admin_actions() {
            axios.get("/admin_actions/get_admin_actions/", {
                params: {
                    starts_at: this.starts_at,
                    ends_at: this.ends_at
                }
            }).then((response) => {
                this.admin_actions = response.data
            })
        },
        open_admin_action_details_window(admin_action) {
            this.current_opened_admin_action = admin_action
            window.location.hash = "admin_action_details_window"
        },
        get_admin_action_created_at_dt(admin_action) {
            return moment(admin_action.created_at).utc().format("DD.MM.YYYY, HH:mm")
        }
    },
    computed: {
    }
})



admin_actions_app.config.compilerOptions.delimiters = ["${", "}"];
mounted_admin_actions_app = admin_actions_app.mount("#admin_actions_section")

