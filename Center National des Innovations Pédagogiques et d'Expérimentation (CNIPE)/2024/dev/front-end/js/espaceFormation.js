searchInput.addEventListener("input", () => {
	filterContainers("formationName");
});

const webContainer = document.querySelector(".weContainerFormations");

async function isAdminOrOwner() {
	try {
		// Make sure to include the token in the headers
		const token = localStorage.getItem("userToken"); // or wherever you store your token
		const response = await axios.get(`${baseUrl}/userRole`, {
			headers: {
				Authorization: `Bearer ${token}`,
			},
		});

		const data = response.data;

		// Check the user's role
		return data.role !== "normal";
	} catch (error) {
		// Handle error and display message
		if (error.response && error.response.data && error.response.data.message) {
			throw { message: error.response.data.message, type: "warning" };
		} else {
			throw { message: "An unexpected error occurred.", type: "danger" };
		}
	}
}
async function getHtmlStructure(formation) {
	let adminContent = "";

	if (await isAdminOrOwner()) {
		adminContent = `
	 						<div class="controlContainer">
							<button class="edit">Edit</button>
							<button class="delete">Delete</button>
						</div>
	 
	 `;
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

	for(formation of data) {
	  await	pushFormationToDom(formation);
	};
}

async function test() {}

window.addEventListener("load", async function () {
	try {
		await manageGetFormations();

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
