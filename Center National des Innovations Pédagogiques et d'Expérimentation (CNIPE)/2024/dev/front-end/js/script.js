const toggleMenu = document.getElementById("toggleMenu");
const navBar = document.querySelector("header ul");
const passwordPattern = /^(?=.*[0-9])(?=.*[!@#$%^&*().?/])[a-zA-Z0-9!@#$%^&*().?/]{6,}$/;
const emailPattern = /^[\w\.-]+@[\w\.-]+\.\w+$/;

const baseUrl = "http://127.0.0.1:5000";

if (toggleMenu) {
	toggleMenu.onclick = function (event) {
		event.stopPropagation();
		navBar.classList.toggle("activeNav");
	};

	document.onclick = function (event) {
		if (!navBar.contains(event.target) && !toggleMenu.contains(event.target)) {
			navBar.classList.remove("activeNav");
		}
	};
}

const loginBtn = document.getElementById("loginBtn");
if (loginBtn) {
	loginBtn.onclick = function () {
		this.querySelector("a").click();
	};
}

let ul = document.querySelector("header ul");
function scrollToTopHard() {
	document.body.scrollTop = 0; // For Safari
	document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE, and Opera
}
function scrollToTopSmooth() {
	window.scrollTo({
		top: 0,
		behavior: "smooth",
	});
}

function goTHome() {
	if (location.pathname != "/index.html" && location.pathname != "/") location.href = "/";
}

function goToLoginPage() {
	if (location.pathname != "/login.html") location.href = "login.html";
}

let navBarImgs = document.querySelectorAll(".logoContainer img");
if (navBarImgs.length != 0) {
	let navBarImg1 = navBarImgs[0];
	let navBarImg2 = navBarImgs[1];
	navBarImg1.onclick = goTHome;
	navBarImg2.onclick = goTHome;
}

function getProfileImg() {
	return localStorage.getItem("profileImg");
}
function setProfileImg(value) {
	return localStorage.setItem("profileImg", value);
}

// confirm
function setUiLoginStat() {
	let LoginBtn = document.getElementById("loginBtn");
	if (loginBtn) {
		let profileImg = getProfileImg();

		loginBtn.innerText = "sign out";
		loginBtn.id = "signOutBtn";
		let htmlStructure = `
	<li class="profile" >
	<div class="imgContainer ProfileImg">
	<img src="${profileImg}" alt="navbar icon" />
</div>
</li>

	`;

		ul.innerHTML += htmlStructure;
	}
}

function isCoursePage() {
	return location.pathname == "/course.html";
}
function isProfilePage() {
	return location.pathname == "/course.html";
}
function goTHome() {
	if (location.pathname != "/index.html" && location.pathname != "/") location.href = "/";
}
function setUiGuestStat() {
	let signOutBtn = document.getElementById("signOutBtn");
	if (signOutBtn) {
		signOutBtn.innerHTML = `<a href="/login.html">Login</a>`;
		signOutBtn.id = "loginBtn";

		let profile = document.querySelector("ul li.profile");
		profile.remove();
		dropUserFromLocalSt();

		if (isCoursePage() || isProfilePage()) {
			goTHome();
		}
	}
}

function dropUserFromLocalSt() {
	localStorage.removeItem("userToken");
	localStorage.removeItem("username");
	localStorage.removeItem("profileImg");
}

// function addLoginStatClasses() {
// 	document.querySelector("ul").classList.add("isLogin");
// 	document.querySelector("ul .rightNavBarContent").classList.add("isLogin");
// }

// function removeLoginStatClasses() {
// 	document.querySelector("nav").classList.remove("isLogin");
// 	document.querySelector("nav .rightNavBarContent").classList.remove("isLogin");
// }
function goToProfilePage() {
	if (location.pathname != "/profile.html") {
		location.href = "profile.html";
	}
}

function isLogin() {
	return localStorage.getItem("userToken") && localStorage.getItem("username");
}

function getURLParameters() {
	var searchParams = new URLSearchParams(window.location.search);
	var params = {};

	// Iterate over all the query parameters
	for (let [key, value] of searchParams) {
		params[key] = value;
	}
	return params;
}

function changeURLWithoutLoad(newUrl) {
	// Change the URL without reloading the page
	window.history.replaceState({ path: newUrl }, "", newUrl);
}

function handelVisibilityPassword(passwordInput, togglePassword) {
	// Toggle the type attribute
	const type = passwordInput.getAttribute("type") === "password" ? "text" : "password";
	passwordInput.setAttribute("type", type);

	// Toggle the icon
	togglePassword.classList.toggle("fa-eye");
	togglePassword.classList.toggle("fa-eye-slash");
}

async function alertHint(msg, mode) {
	const section = document.querySelector("section.hint ");
	const divAlter = document.querySelector("section.hint > div");
	const alterTitle = document.querySelector("section.hint .alert-title");
	const alterContent = document.querySelector("section.hint .alert-content");

	divAlter.classList.add(`alert-${mode}`);
	alterTitle.innerHTML = mode;
	alterContent.innerText = msg;

	section.classList.add("ActiveAlter");

	await wait(100);
	divAlter.id = "ActiveAlter";

	await wait(4000);
	divAlter.id = "";
	section.classList.remove("ActiveAlter");
}
function wait(time) {
	return new Promise((resolve) => setTimeout(resolve, time));
}

function getUsername() {
	let username = "";
	if ((user = localStorage.getItem("username"))) return user;
	else return "user";
}

function checkIfIsAValidPassword(password) {
	/*
	 the password must start with at least 5 letters, followed by at least one digit
	 , and can contain any characters after that.
*/
	return passwordPattern.test(password);
}

function checkRegex(password) {
	const numberPattern = /\d/;
	const specialCharacterPattern = /[^a-zA-Z0-9]/;
	const minLength = 5;
	const maxLength = 20;

	if (numberPattern.test(password)) {
		if (specialCharacterPattern.test(password)) {
			if (password.length >= minLength && password.length <= maxLength) {
				return 6;
			}
			return 5;
		}
		if (password.length >= minLength && password.length <= maxLength) {
			return 4;
		}
		return 3;
	}
	if (password.length >= minLength && password.length <= maxLength) {
		return 2;
	}
	if (specialCharacterPattern.test(password)) return 1;
	return 0;
}

function ChangeHint(value) {
	let Charhint = document.getElementById("charSize").style;
	let numBool = document.getElementById("numExi").style;
	let speCharBool = document.getElementById("charExi").style;
	switch (value) {
		case 6:
			Charhint.color = "green";
			numBool.color = "green";
			speCharBool.color = "green";
			break;
		case 5:
			Charhint.color = "red";
			numBool.color = "green";
			speCharBool.color = "green";
			break;
		case 4:
			Charhint.color = "green";
			numBool.color = "green";
			speCharBool.color = "red";
			break;
		case 3:
			Charhint.color = "red";
			numBool.color = "green";
			speCharBool.color = "red";
			break;
		case 2:
			Charhint.color = "green";
			numBool.color = "red";
			speCharBool.color = "red";
			break;
		case 1:
			Charhint.color = "red";
			numBool.color = "red";
			speCharBool.color = "green";
			break;
		default:
			Charhint.color = "red";
			numBool.color = "red";
			speCharBool.color = "red";
			break;
	}
}

function verifyDispBubbl(bool) {
	let hintBubble = document.getElementById("hintBubbl");
	if (bool) hintBubble.style.display = "flex";
	else hintBubble.style.display = "none";
}

function updateURLWithoutReload(url) {
	// Use pushState to update the URL without reloading the page
	history.pushState(null, null, url);
}

document.addEventListener("click", (event) => {
	if (event.target.id == "signOutBtn") {
		setUiGuestStat();
	}
	if (event.target == document.querySelector(".profile .ProfileImg img")) {
		goToProfilePage();
	}
});

window.addEventListener("load", function () {
	if (isLogin()) {
		setUiLoginStat();
	} else {
		setUiGuestStat();
	}
});

let boxesContainer = document.querySelectorAll(".domainContent");
let searchInput = document.querySelector(".searchContainer input");

function filterCards(domain, attName) {
	domain.querySelectorAll(".domainContent .card").forEach((card) => {
		if (card.getAttribute(attName) && !card.getAttribute(attName).toLowerCase().trim().includes(searchInput.value.toLowerCase().trim())) {
			card.style.display = "none";
		} else {
			card.style.display = "flex";
		}
	});
}

function filterContainers(attName) {
	boxesContainer.forEach((domain) => {
		filterCards(domain, attName);
	});
}
let searchContainer = document.querySelector(".searchContainer .content");
