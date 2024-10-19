import { app } from "../../../scripts/app.js";

app.registerExtension({
	name: "BWIZ.PlaySound",
	
	async beforeRegisterNodeDef(nodeType, nodeData, app) {
		if (nodeData.name === "🧙🏼 BWIZ | Notification (Navi)") {
			const onExecuted = nodeType.prototype.onExecuted;

			nodeType.prototype.onExecuted = async function () {
				onExecuted?.apply(this, arguments);

				let soundDirectory = "custom_nodes/ComfyUI_BWiZ_Nodes/res/navi";
				let playErrorSound = this.widgets[3].value || false;

				if (playErrorSound) {
					playSound("error.mp3", soundDirectory);
					return;
				}

				const soundFiles = await fetchSoundFiles(soundDirectory);
				if (soundFiles.length === 0) {
					console.error("No sound files found in the directory");
					return;
				}

				const randomSoundFile = soundFiles[Math.floor(Math.random() * soundFiles.length)];
				playSound(randomSoundFile, soundDirectory);
			};
		}
	},
});

async function fetchSoundFiles(directory) {
	// Simulate fetching sound files from the directory
	// Replace this with actual logic if needed
	return ["loz_navi_hey_listen.mp3", "oot_navi_hello.mp3"];
}

function playSound(fileName, directory) {
	let filePath = `${directory}/${fileName}`;
	if (!filePath.startsWith("http")) {
		filePath = new URL(filePath, import.meta.url);
	}

	const audio = new Audio(filePath);
	audio.play().catch(error => console.error('Error playing sound:', error));
}