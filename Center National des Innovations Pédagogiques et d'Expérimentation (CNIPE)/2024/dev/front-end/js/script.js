const toggleMenuBtn = document.getElementById("toogleMenu");
const navBar = document.querySelector("header ul");
if (toggleMenuBtn) {
	toggleMenuBtn.onclick = function (event) {
		event.stopPropagation();
		navBar.classList.toggle("activeNav");
	};

	document.onclick = function (event) {
		if (!navBar.contains(event.target) && !toggleMenuBtn.contains(event.target)) {
			navBar.classList.remove("activeNav");
		}
	};
}
