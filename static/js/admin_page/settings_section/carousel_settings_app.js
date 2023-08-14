carousel_settings_app = Vue.createApp({
    data() {
        return {
            carousel_images: [],
        }
    },
    methods: {
        get_carousel_images() {
            this.carousel_images = []
            axios.get("/site_settings/get_carousel_images/").then((response) => {
                response.data["carousel_images"].forEach(image => this.carousel_images.push(new CarouselImage(image)))
            })
            document.getElementById("carousel_images_editing_block").style.display = "none"
            document.getElementById("carousel_images_preview_block").style.display = "block"
        },
        handle_file_upload(carousel_image, event) {
            carousel_image.file = event.target.files[0]

        },
        save_carousel_images_editing() {
            var images = []
            var formData = new FormData();

            this.carousel_images.forEach((image, index) => {
                if (image.name != "") {
                    var name = image.name
                } else {
                    var name = "no name"
                }
                images.push({
                    serial_number: index + 1,
                    name: name,
                })
                if (!image.file) {
                    images[images.length - 1]["url"] = image.url
                } else {
                    formData.append((index + 1) + ". " + name, image.file)
                }
            })

            formData.append("images", JSON.stringify(images))

            axios.post('/site_settings/save_carousel_images/', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                    "X-CSRFToken": $cookies.get("csrftoken"),
                }
              }
            ).then((response) => {
                this.cancel_carousel_images_editing()
            }).catch((error) => {
                if (error.response) {
                    alert("Правильно заполните форму!")
                }
            })

        },

        open_carousel_images_editing_block() {
            document.getElementById("carousel_images_editing_block").style.display = "block"
            document.getElementById("carousel_images_preview_block").style.display = "none"
        },
        delete_carousel_image(carousel_image) {
            this.carousel_images.splice(this.carousel_images.indexOf(carousel_image), 1)

        },
        add_carousel_image() {
            this.carousel_images.push(new CarouselImage())

        },
        cancel_carousel_images_editing() {
            this.get_carousel_images()
            document.getElementById("carousel_images_editing_block").style.display = "none"
            document.getElementById("carousel_images_preview_block").style.display = "block"
        }
    }
})

carousel_settings_app.config.compilerOptions.delimiters = ["${", "}"];
mounted_carousel_settings_app = carousel_settings_app.mount("#carousel_settings")