const nbrCategories = document.getElementById("nbrCategories");
const nbrUsers = document.getElementById("nbrUsers");
const nbrCourses = document.getElementById("nbrCourses");
const nbrVideos = document.getElementById("nbrVideos");

async function fetchStatistics() {
	try {
		const response = await axios.get(`${baseUrl}/stats`);
		const data = response.data;

		// Update the DOM elements with the fetched data
		nbrCategories.textContent = data.numberOfCategories;
		nbrUsers.textContent = data.numberOfUsers;
		nbrCourses.textContent = data.numberOfCourses;
		nbrVideos.textContent = data.numberOfVideos;
	} catch (error) {
		console.error("Error fetching statistics:", error);
		// Handle error (you might want to display a message to the user)
	}
}
window.addEventListener("load", function () {
	fetchStatistics();
});

