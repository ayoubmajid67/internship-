searchInput.addEventListener("input", () => {
	filterContainers("formationName");
});

const webContainer = document.querySelector(".weContainerFormations");

async function isAdminOrOwner() {
	return true;
}
function getHtmlStructure(formation) {
	let adminContent = "";

	if (isAdminOrOwner()) {
		adminContent = `
	 						<div class="controlContainer">
							<button class="edit">Edit</button>
							<button class="delete">Delete</button>
						</div>
	 
	 `;
	}

	return `
					<article formationName=${formation.categoryName} class="card">
${adminContent}
						<img src=${formation.thumbnail} type="image/webp" alt="portfolio 1" />
						<h3>${formation.categoryName}</h3>
						<p>${formation.description}</p>
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
						<div class="ProjectResource">
							<a href="formation.html?categoryName=${formation.categoryName}" class="WebtiseLink" target="_blank">Consulter</a>
						</div>
					</article>

	`;
}

function pushFormationToDom(formation) {
	const htmlStructure = getHtmlStructure(formation);

	webContainer.insertAdjacentHTML("beforeend", htmlStructure);
}


async function getFormationResponse(categoryName) {

    try {
		const response = await axios.get(`${baseUrl}/formations/${categoryName}`);

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
    let urlParams = getURLParameters();
	if (!urlParams.hasOwnProperty("categoryName")) goToEspaceFormation();
  

	webContainer.innerHTML = "";
	data = await getFormationResponse(urlParams.categoryName);

    console.log(data);

	// data.forEach((formation) => {
	// 	pushFormationToDom(formation);
	// });
}

async function test() {}

manageGetFormations();
