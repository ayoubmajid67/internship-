let isFull = { username: false, email: false, password: false, confirmation: false };
let inputBox = [document.getElementById("username"), document.getElementById("email"), document.getElementById("password"), document.getElementById("confirmPassword")];
let regButton = document.getElementById("submit");
let otherBtn = document.getElementById("login");
const loginForm = document.forms[0];

let isPass = { eightChar: false, hasNum: false, hasSpcChar: false };
const eventMessage = document.getElementById("eventMessage");

otherBtn.addEventListener("click", () => {
	goToLoginPage();
});
regButton.disabled = true;

let PassBox = inputBox[3];
PassBox.disabled = true;

function verifyInputToDisBtn() {
	if (isFull.username && isFull.email && isFull.password && isFull.confirmation) regButton.disabled = false;
	else regButton.disabled = true;
}

function verifyPass() {
	if (isFull.password) PassBox.disabled = false;
	else PassBox.disabled = true;
}
// check length and remove disable from button and confirm password input
function checkIfIsAValidPassword(password) {
	/*
	 the password must start with at least 5 letters, followed by at least one digit
	 , and can contain any characters after that.
*/
	return passwordPattern.test(password);
}

function checkIfIsAValidUsername(username) {
	return username.trim() != "";
}
function checkIfIsAValidEmail(email) {
	return emailPattern.test(email);
}

inputBox[0].addEventListener("input", function () {
	this.value = this.value.trim();
	isFull.username = checkIfIsAValidUsername(this.value) ? true : false;
	verifyInputToDisBtn();
});

inputBox[1].addEventListener("input", function () {
	this.value = this.value.trim();
	isFull.email = checkIfIsAValidEmail(this.value);
	verifyInputToDisBtn();
});

inputBox[2].addEventListener("input", function () {
	this.value = this.value.trim();
	isFull.password = checkIfIsAValidPassword(this.value) ? true : false;
	verifyInputToDisBtn();
	verifyPass();
	ChangeHint(checkRegex(this.value));
	verifyDispBubbl(!isFull.password);
});

inputBox[2].addEventListener("focusin", function () {
	verifyDispBubbl(true);
});

inputBox[2].addEventListener("focusout", function () {
	verifyDispBubbl(false);
});

inputBox[3].addEventListener("input", function () {
	this.value = this.value.trim();
	isFull.confirmation = this.value === inputBox[2].value;
	verifyInputToDisBtn();
});

function getRegisterInfo() {
	return [inputBox[0].value, inputBox[1].value, inputBox[2].value];
}

async function register(username, email, password) {
	try {
		const response = await axios.post(`${baseUrl}/register`, {
			username: username,
			email: email,
			password: password,
		});

		const data = response.data;

		window.location = `login.html?email=${email}&password=${password}`;
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

window.addEventListener("load", () => {
	if (isLogin()) goToHome();
});

loginForm.addEventListener("submit", async function (event) {
	event.preventDefault();
	regButton.disabled = true;
	let [username, email, password] = getRegisterInfo();
	console.log(username, email, password);
	try {
		await register(username, email, password);
	} catch (error) {
		alertHint(error.message, error.type);
		return false;
	}

	regButton.disabled = false;
});

const passwordInput = inputBox[2];
const conformPassword = inputBox[3];
const togglePassword = document.getElementById("togglePassword");
const toggleConformPassword = document.getElementById("toggleConfirm");

togglePassword.addEventListener("click", function () {
	handelVisibilityPassword(passwordInput, this);
});
toggleConformPassword.addEventListener("click", function () {
	handelVisibilityPassword(conformPassword, this);
});
