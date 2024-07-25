const webContainer = document.querySelector(".domainContent");
const blackDrop = document.querySelector(".blackDrop");
const deletePopUpBox = document.querySelector(".deletePopup");
const deleteDomainNameBox = deletePopUpBox.querySelector(".popUpDomainName");
const deletePopUpBtn = deletePopUpBox.querySelector(".popupButtonDelete");
const boxModeClass = "activeBox";
const editStatClass = "editStat";
const addPopUpBox = document.querySelector(".addPopup");
const addPopUpNameInput = addPopUpBox.querySelector(".domainTitleInput");
const addPopUpDescriptionInput = addPopUpBox.querySelector(".descriptionInput");
const addPopUpFileInput = addPopUpBox.querySelector("input[type='file']");

function setDisablePopUpBoxMode() {
	deletePopUpBox.classList.remove(boxModeClass);
	addPopUpBox.classList.remove(boxModeClass);
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
function setEnableAddDomainMode() {
	blackDrop.classList.add(boxModeClass);
	addPopUpBox.classList.add(boxModeClass);

	let scrollTop = window.pageYOffset || document.documentElement.scrollTop;
	window.onscroll = function () {
		scrollToPositionHard(scrollTop);
	};
}

window.addEventListener("click", function (event) {
	if (event.target == blackDrop || event.target.classList.contains("popupButtonCancel")) {
		setDisablePopUpBoxMode();
		window.onscroll = function () {};
	}
});

function setUpDeleteBoxToShow(domainName) {
	deletePopUpBox.setAttribute("categoryName", domainName);
	deleteDomainNameBox.textContent = domainName;
}

let beforeEditInfo = {
	imgContainerContent: "",
	title: "",
	description: "",
};

let cardChangedFiledInfo = {
	domainImg: false,
	domainTitle: false,
	domainDescription: false,
};
let saveValuesInfo = {
	domainImg: "",
	domainTitle: "",
	domainDescription: "",
	imgUrl: "",
};

function setUpEditCardUi(card) {
	if (card) {
		card.classList.add(editStatClass);
		let imgContainer = card.querySelector(".imgContainer");
		let cardTitleBox = card.querySelector(".domainName");
		let cardDescriptionBox = card.querySelector(".description");

		beforeEditInfo.imgContainerContent = imgContainer.innerHTML;
		imgContainer.innerHTML = `	<div class="content">
										<h4>Choose a File</h4>
										<img  src="imgs/addPost.svg" alt="add-image" />
									</div>
									<input type="file" name="image" accept="image/*" onchange="manageImgFileChange(event)" />`;
		beforeEditInfo.title = cardTitleBox.textContent;
		beforeEditInfo.description = cardDescriptionBox.textContent;

		cardTitleBox.innerHTML = `<input type="text" class="domainNameInput" placeholder="nom de formation"   value=${beforeEditInfo.title} onInput="manageDomainNameChange(event)">`;
		cardDescriptionBox.innerHTML = `<textarea class="descriptionInput" placeholder="description de formation" oninput="manageDescriptionChange(event)" >${beforeEditInfo.description}</textarea>`;

		autoResize(document.querySelector(".card .descriptionInput"));
	}
}
function clearEditInfo() {
	beforeEditInfo.imgContainerContent = "";
	beforeEditInfo.title = "";
	beforeEditInfo.description = "";

	cardChangedFiledInfo.domainImg = false;
	cardChangedFiledInfo.domainTitle = false;
	cardChangedFiledInfo.domainDescription = false;

	saveValuesInfo.domainImg = "";
	saveValuesInfo.domainTitle = "";
	saveValuesInfo.domainDescription = "";
	saveValuesInfo.imgUrl = "";
}

function setOffEditCardUi(card) {
	if (card) {
		card.classList.remove(editStatClass);
		let imgContainer = card.querySelector(".imgContainer");
		let cardTitleBox = card.querySelector(".domainName");
		let cardDescriptionBox = card.querySelector(".description");

		imgContainer.innerHTML = beforeEditInfo.imgContainerContent;

		let beforeContent = imgContainer.querySelector(".beforeContent");
		let beforeContentText = beforeContent.querySelector("h4");

		card.setAttribute("categoryName", beforeEditInfo.title);
		beforeContent.setAttribute("categoryName", beforeEditInfo.title);
		beforeContentText.textContent = beforeEditInfo.title;

		imgContainer.style.backgroundImage = "unset";
		cardTitleBox.textContent = beforeEditInfo.title;

		cardDescriptionBox.textContent = beforeEditInfo.description;

		if (cardChangedFiledInfo.domainImg && saveValuesInfo.imgUrl) {
			let thumbnailImg = imgContainer.querySelector("img");
			thumbnailImg.setAttribute("src", saveValuesInfo.imgUrl);
		}

		clearEditInfo();
	}
}

function setOffEditedCardBoxes() {
	let editStatCards = document.querySelectorAll(`.card.${editStatClass}`);
	editStatCards.forEach((card) => {
		card.querySelector("button.cancel").click();
	});
}

async function manageEditCard(event) {
	setOffEditedCardBoxes();
	const editBtn = event.target;
	const targetCard = editBtn.parentElement.parentElement;

	switchBtnHandler(editBtn, "cancel", "cancel", "cancelEditCard(event)");
	const deleteBtn = targetCard.querySelector("button.delete");
	switchBtnHandler(deleteBtn, "save", "save", "manageSaveEditCard(event)");
	deleteBtn.disabled = true;

	setUpEditCardUi(targetCard);
}

function cancelEditCard(event) {
	const cancelBtn = event.target;
	const targetCard = cancelBtn.parentElement.parentElement;

	switchBtnHandler(cancelBtn, "edit", "edit", "manageEditCard(event)");
	const saveEditBtn = targetCard.querySelector("button.save");
	saveEditBtn.disabled = false;

	setOffEditCardUi(targetCard);

	switchBtnHandler(saveEditBtn, "delete", "delete", "manageDeleteCard(event)");
}

function updateFileBackground(event) {
	const fileInput = event.target;
	const imgContainer = fileInput.closest(".imgContainer");
	const imgContainerContent = imgContainer.querySelector(".content");

	if (fileInput.files.length > 0) {
		const reader = new FileReader();

		reader.onload = function (e) {
			imgContainer.style.backgroundImage = `url(${e.target.result})`;
			saveValuesInfo.imgUrl = e.target.result;
		};

		reader.readAsDataURL(fileInput.files[0]);
		imgContainerContent.style.display = "none";
	} else {
		imgContainer.style.backgroundImage = `none`;
		imgContainerContent.style.display = "block";
	}
}

function isChangeDomainTitle(newTitle) {
	return beforeEditInfo.title != newTitle;
}
function isChangeDomainDescription(newDescription) {
	return beforeEditInfo.description != newDescription;
}

function manageDomainNameChange(event) {
	saveValuesInfo.domainTitle = event.target.value.trim().toLowerCase();
	if (isChangeDomainTitle(saveValuesInfo.domainTitle)) cardChangedFiledInfo.domainTitle = true;
	else cardChangedFiledInfo.domainTitle = false;
	handelDeleteCardStat(event);
}

function manageDescriptionChange(event) {
	autoResize(event.target);

	saveValuesInfo.domainDescription = event.target.value.trim();

	if (isChangeDomainDescription(saveValuesInfo.domainDescription)) cardChangedFiledInfo.domainDescription = true;
	else cardChangedFiledInfo.domainDescription = false;
	handelDeleteCardStat(event);
}
function manageImgFileChange(event) {
	updateFileBackground(event);
	const fileInput = event.target;
	if (fileInput.files.length > 0) {
		cardChangedFiledInfo.domainImg = true;
		saveValuesInfo.domainImg = fileInput.files[0];
	} else {
		cardChangedFiledInfo.domainImg = false;
		saveValuesInfo.domainImg = "";
		saveValuesInfo.imgUrl = "";
	}
	handelDeleteCardStat(event);
}

function manageAddDomainImgFileChange(event) {
	updateFileBackground(event);
}
function isAllowToSave() {
	return cardChangedFiledInfo.domainTitle || cardChangedFiledInfo.domainDescription || cardChangedFiledInfo.domainImg;
}

async function editFormationResponse(categoryName) {
	try {
		if (!isLogin()) {
			setUiGuestStat();
			throw "Invalid User login";
		}
		const token = localStorage.getItem("userToken");

		// Create a FormData object
		const formData = new FormData();

		// Append only changed fields
		if (cardChangedFiledInfo.domainImg) {
			formData.append("thumbnail", saveValuesInfo.domainImg);
		}
		if (cardChangedFiledInfo.domainTitle) {
			formData.append("newCategoryName", saveValuesInfo.domainTitle);
		}
		if (cardChangedFiledInfo.domainDescription) {
			formData.append("newDescription", saveValuesInfo.domainDescription);
		}

		const response = await axios.put(`${baseUrl}/formations/${categoryName}`, formData, {
			headers: {
				Authorization: `Bearer ${token}`,
				"Content-Type": "multipart/form-data",
			},
		});

		const data = response.data;

		return data;
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
function updateBeforeTextContent() {
	if (saveValuesInfo.domainTitle) beforeEditInfo.title = saveValuesInfo.domainTitle;
	if (saveValuesInfo.domainDescription) beforeEditInfo.description = saveValuesInfo.domainDescription;
}
async function manageSaveEditCard(event) {
	const saveEditBtn = event.target;
	saveEditBtn.disabled = true;
	if (!isAllowToSave()) return;
	const card = event.target.closest(".card");

	try {
		let categoryName = "";
		if (card) categoryName = card.getAttribute("categoryName");
		data = await editFormationResponse(categoryName);

		const cancelBtn = card.querySelector("button.cancel");

		switchBtnHandler(saveEditBtn, "delete", "Delete", "manageDeleteCard(event)");
		switchBtnHandler(cancelBtn, "edit", "Edit", "manageEditCard(event)");
		if (isChangeDomainDescription() || isChangeDomainTitle()) updateBeforeTextContent();

		setOffEditCardUi(card, data.thumbnail);

		alertHint(data.message, "success");
	} catch (error) {
		alertHint(error.message, error.type);
	}
	saveEditBtn.disabled = false;
}
function handelDeleteCardStat(event) {
	const saveBtn = event.target.closest(".card").querySelector("button.save");
	if (isAllowToSave()) {
		saveBtn.disabled = false;
	} else {
		saveBtn.disabled = true;
	}
}

function manageAddDomain(event) {
	const addBtn = event.target;

	setEnableAddDomainMode();
}

function manageAddFormationDescriptionChange(event) {
	autoResize(event.target);
}

async function addFormationResponse(inputsData) {
	try {
		if (!isLogin()) {
			setUiGuestStat();
			throw "Invalid User login";
		}
		const token = localStorage.getItem("userToken");

		// Create a FormData object
		const formData = new FormData();

		formData.append("categoryName", inputsData.domainTitle);

		formData.append("description", inputsData.domainDescription);

		// Append only changed fields
		if (inputsData.domainImg) {
			formData.append("thumbnail", inputsData.domainImg);
		}

		const response = await axios.post(`${baseUrl}/formations`, formData, {
			headers: {
				Authorization: `Bearer ${token}`,
				"Content-Type": "multipart/form-data",
			},
		});

		const data = response.data;

		return data.formationData;
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
async function addFormation(event) {
	event.target.disabled = true;
	const titleValue = addPopUpNameInput.value;
	const descriptionValue = addPopUpDescriptionInput.value;
	const imgFile = addPopUpFileInput.files;

	if (titleValue == "" || descriptionValue == "") {
		if (titleValue != "" && descriptionValue == "") addPopUpDescriptionInput.focus();
		else addPopUpNameInput.focus();

		await alertHint("title and description are required ", "warning");
	} else {
		let data = {
			domainTitle: titleValue,
			domainDescription: descriptionValue,
		};
		if (imgFile.length >= 1) data.domainImg = imgFile[0];

		try {
			const formationData = await addFormationResponse(data);
			setDisablePopUpBoxMode();
			formationData.videos = {
				totalLikes: 0,
				numberOfVideos: 0,
			};

			pushFormationToDom(formationData);
			scrollToPositionSmooth(webContainer.scrollHeight - 50);
		} catch (error) {
			await alertHint(error.message, error.type);
		}
	}

	event.target.disabled = false;
}
