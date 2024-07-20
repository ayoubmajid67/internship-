const blackDrop = document.querySelector(".blackDrop");
const deletePopUpBox = document.querySelector(".deletePopup");
const deleteDomainNameBox = deletePopUpBox.querySelector(".popUpDomainName");
const deletePopUpBtn = deletePopUpBox.querySelector(".popupButtonDelete");
const boxModeClass = "activeBox";

function setDisablePopUpBoxMode() {
	deletePopUpBox.classList.remove(boxModeClass);
	blackDrop.classList.remove(boxModeClass);
	cardBox = webContainer.querySelector(".card.deleteStatus");
	if (cardBox) cardBox.classList.remove("deleteStatus");
	window.onscroll = function () {};
}

function setEnableDeleteMode(cardBox) {
	blackDrop.classList.add(boxModeClass);
	deletePopUpBox.classList.add(boxModeClass);
	cardBox.classList.add("deleteStatus");
	let scrollTop = window.pageYOffset || document.documentElement.scrollTop;
	window.onscroll = function () {
		scrollToPositionHard(scrollTop);
	};
}

window.addEventListener("click", function (event) {
	console.log(event.target);
	if (event.target == blackDrop || event.target.classList.contains("popupButtonCancel")) {
		setDisablePopUpBoxMode();
		window.onscroll = function () {};
	}
});

function setUpDeleteBoxToShow(domainName) {
	deletePopUpBox.setAttribute("categoryName", domainName);
	deleteDomainNameBox.textContent = domainName;
}
