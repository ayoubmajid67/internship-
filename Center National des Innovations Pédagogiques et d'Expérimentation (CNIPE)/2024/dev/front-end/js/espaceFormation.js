searchInput.addEventListener("input", () => {
	filterContainers("categoryName");
});



async function getHtmlStructure(formation) {
	let adminContent = "";

	if (isLogin()) {
		if (await isAdminOrOwner()) {
			adminContent = `
	 						<div class="controlContainer">
							<button class="edit" onclick=manageEditCard(event)>Edit</button>
							<button class="delete" onclick=manageDeleteCard(event)>Delete</button>
						</div>
	 
	 `;
		}
	}

	return `
					<article categoryName=${formation.categoryName} class="card">
${adminContent}            
			<div class="imgContainer" >
						<img src=${formation.thumbnail}  type="image/webp" alt="portfolio 1" />

						
								<div class="beforeContent" categoryName=${formation.categoryName}>
                                    <h4 class="categoryName">${formation.categoryName}</h4>
								</div>
						</div>
						<h3 class="domainName">${formation.categoryName}</h3>
						<p class="description">${formation.description}</p>
						<div class="statistiques">
							<figure class="likesFigure">
								<img src="imgs/likes.png" alt="like img" />
								<h5>${formation.videos.totalLikes}</h5>
							</figure>
							<figure class="totalVideosFigure">
								<img src="imgs/videos.png" alt="video img" />
								<h5>${formation.videos.numberOfVideos}</h5>
							</figure>
						</div>
					</article>

	`;
}

async function pushFormationToDom(formation) {
	const htmlStructure = await getHtmlStructure(formation);

	webContainer.insertAdjacentHTML("beforeend", htmlStructure);
}

async function getFormationsResponse() {
	try {
		const response = await axios.get(`${baseUrl}/formations`);

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

async function manageGetFormations() {
	webContainer.innerHTML = "";
	data = await getFormationsResponse();

	for (formation of data) {
		await pushFormationToDom(formation);
	}
}

async function pushAddDomainFormation() {
	if (isLogin()) {
		if (await isAdminOrOwner()) {
			const addContentHtmlStructure = getDomainContentHtmlStructure();
			document.querySelector(".searchContainer").insertAdjacentHTML("afterend", addContentHtmlStructure);
		}
	}
}

window.addEventListener("load", async function () {
	try {
		await manageGetFormations();

		await pushAddDomainFormation();
	} catch (error) {
		alertHint(error.message, error.type);
	}
});

document.addEventListener("click", function (event) {
	if (event.target.classList.contains("beforeContent")) {
		const categoryName = event.target.getAttribute("categoryName");
		window.location = `formation.html?categoryName=${categoryName}`;
	}
});

async function deleteFormationResponse(categoryName) {
	try {
		if (!isLogin()) {
			setUiGuestStat();
			throw "Invalid User login";
		}
		const token = localStorage.getItem("userToken");

		const response = await axios.delete(`${baseUrl}/formations/${categoryName}`, {
			headers: {
				Authorization: `Bearer ${token}`,
			},
		});

		const data = response.data;

		return data.message;
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

async function manageDeleteCard(event) {
	deleteBtn = event.target;
	const targetCard = deleteBtn.parentElement.parentElement;
	const categoryName = targetCard.getAttribute("categoryname");

	setEnableDeleteMode(targetCard);
	setUpDeleteBoxToShow(categoryName);
}

deletePopUpBtn.addEventListener("click", async function () {
	let categoryName = deletePopUpBox.getAttribute("categoryName");
	try {
		if (categoryName) {
			let message = await deleteFormationResponse(categoryName);
			let targetCard = webContainer.querySelector(".card.deleteStatus");
			targetCard.remove();
			setDisablePopUpBoxMode();
			await alertHint(message, "success");
		}
	} catch (error) {
		setDisablePopUpBoxMode();
		alertHint(error.message, error.type);
	}
});
