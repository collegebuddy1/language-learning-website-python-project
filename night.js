let buttonImg;
let body;
let darkMode;
let figcaption;
let caption;
let svgElement;
let oddTableElements;
let button = document.querySelector("#night_mode");

button.addEventListener("click", nightToggle, false);

// On page load/reload, this checks local storage and ensures that the color scheme matches the stored values
document.addEventListener("DOMContentLoaded", function() {
	body = document.querySelector("body");
	buttonImg = document.querySelector("#night_mode > img");
	if (document.querySelectorAll("figcaption") !== null) {
		figcaption = document.querySelectorAll("figcaption");
	}
	if (document.querySelectorAll("caption") !== null) {
		caption = document.querySelectorAll("caption");
	}
	if (document.querySelector("#tone_image") !== null) {
		svgElement = document.querySelector("#tone_image");
	}
	darkMode = localStorage.getItem("darkMode");
	if (darkMode === "enabled") {
		buttonImg.classList.add("animation_down");
		body.classList.add("night-mode");
		for (let counter = 0; counter < figcaption.length; counter ++) {
			figcaption[counter].classList.add("night-general");
		}
		for (let counter = 0; counter < caption.length; counter ++) {
			caption[counter].classList.add("night-general");
		}
		if (svgElement !== undefined) {
			svgElement.src = "images/illustrations/tones_night.svg";
		}
	}
	else {
		buttonImg.classList.remove("animation_down");
		body.classList.remove("night-mode");
		for (let counter = 0; counter < figcaption.length; counter ++) {
			figcaption[counter].classList.remove("night-general");
		}
		for (let counter = 0; counter < caption.length; counter ++) {
			caption[counter].classList.remove("night-general");
		}
		if (svgElement !== undefined) {
			svgElement.src = "images/illustrations/tones.svg";
		}
	}
});

// Runs when the html button is pressed
function nightToggle() {
	buttonImg = document.querySelector("#night_mode > img");
	body = document.querySelector("body");
	caption = document.querySelectorAll("caption");
	figcaption = document.querySelectorAll("figcaption");
	// Creates the element only if something like it exists on the page. No errors were called for other elements if they did not exist.
	if (document.querySelector("#tone_image") !== null) {
		svgElement = document.querySelector("#tone_image");
	}
	if (document.querySelectorAll("tr") !== null) {
		oddTableElements = document.querySelectorAll("tr");
	}
	// Actual code
	let darkMode = localStorage.getItem("darkMode");
	if (darkMode !== "enabled") {
		enableDarkMode();
	}
	else {
		disableDarkMode();
	}
}

function enableDarkMode() {
	localStorage.setItem("darkMode", "enabled");
	buttonImg.classList.add("animation_down");
	body.classList.add("night-mode");
	for (let counter = 0; counter < figcaption.length; counter ++) {
		figcaption[counter].classList.add("night-general");
	}
	for (let counter = 0; counter < caption.length; counter ++) {
		caption[counter].classList.add("night-general");
	}
	for (let counter = 1; counter < oddTableElements.length; counter += 2) {
		oddTableElements[counter].classList.add("night-mode");
	}
	if (svgElement !== undefined) {
		svgElement.src = "images/illustrations/tones_night.svg";
	}
}

function disableDarkMode() {
	localStorage.setItem("darkMode", "disabled");
	buttonImg.classList.remove("animation_down");
	body.classList.remove("night-mode");
	for (let counter = 0; counter < figcaption.length; counter ++) {
		figcaption[counter].classList.remove("night-general");
	}
	for (let counter = 0; counter < caption.length; counter ++) {
		caption[counter].classList.remove("night-general");
	}
	for (let counter = 1; counter < oddTableElements.length; counter += 2) {
		oddTableElements[counter].classList.remove("night-mode");
	}
	if (svgElement !== undefined) {
		svgElement.src = "images/illustrations/tones.svg";
	}
}
