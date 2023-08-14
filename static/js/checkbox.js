const checkbox = document.querySelector('.checkbox_input')
const rus = document.querySelector('.rus_block')
const kaz = document.querySelector('.kz_block')
let value = 0;


checkbox.addEventListener("click", function () {
	value++;

	if(value%2 == 0){
		rus.style.display = "block";
		kaz.style.display = "none";
	}else if(value%2 == 1){
		rus.style.display = "none";
		kaz.style.display = "block";
	}
})