

const emailInput = document.querySelector('input[type="email"]');
const passwordInput = document.querySelector('input[type="password"]');
const loginBtnInput = document.querySelector('input[type="submit"]');
const loginForm = document.querySelector("form");



async function login(email, password) {
	try {
		const response = await axios.post(`${baseUrl}/login`, {
			email: email,
			password: password,
		});

		const data = response.data;

		// Store the token and email in localStorage
		localStorage.setItem("userToken", data.token);
		localStorage.setItem("username", data.username);
		setProfileImg(data.profileImg);

		goToHome();
	} catch (error) {
		// Handle error and display message
		if (error.response && error.response.data && error.response.data.error) {
			throw { message: error.response.data.error, type: "warning" };
		} else {
			console.log(error);
			throw { message: "An unexpected error occurred.", type: "danger" };
		}
	}
}

function clearLoginInputs() {
	emailInput.value = "";
	passwordInput.value = "";
}

loginForm.addEventListener("submit", async function (event) {
	// This will be called if the form is valid
	if (!this.checkValidity()) {
		// The form is invalid; HTML5 validation will handle showing error messages
		return;
	}

	event.preventDefault();

	const email = emailInput.value.toLowerCase().trim();
	const password = passwordInput.value.trim();

	loginBtnInput.disabled = true;

	try {
		await login(email, password);
	} catch (error) {
		alertHint(error.message, error.type);
	}

	passwordInput.focus();
	loginBtnInput.disabled = false;
});

const togglePassword = document.getElementById("togglePassword");
togglePassword.addEventListener("click", function () {
	handelVisibilityPassword(passwordInput, this);
});

window.addEventListener('load',function(){
	if (isLogin()) {
		window.location = "/index.html";
	}	
		const urlParams = getURLParameters();
			// Check if the email and password are in the URL parameters
			if (urlParams.hasOwnProperty("email") && urlParams.hasOwnProperty("password")) {
				emailInput.value = urlParams.email;
				passwordInput .value = urlParams.password;
				updateURLWithoutReload(location.pathname);
			}
	
})
