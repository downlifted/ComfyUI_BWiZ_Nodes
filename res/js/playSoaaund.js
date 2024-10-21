import { app } from "../../../scripts/app.js";

app.registerExtension({
	name: "BWIZ.PlaySound",
	
	async beforeRegisterNodeDef(nodeType, nodeData, app) {
		if (nodeData.name === "🧙🏼 BWIZ | Notification Sound (Navi)") {
			const onExecuted = nodeType.prototype.onExecuted;

			nodeType.prototype.onExecuted = async function () {
				onExecuted?.apply(this, arguments);

				let soundSource = this.widgets[2].value || "default";
				let playErrorSound = this.widgets[3].value || false;

				if (playErrorSound) {
					playSound("https://github.com/downlifted/ComfyUI_BWiZ_Nodes/raw/refs/heads/main/res/navi/error.mp3");
					return;
				}

				if (isValidUrl(soundSource)) {
					playSound(soundSource);
				} else {
					const soundFiles = await fetchSoundFiles(soundSource);
					if (soundFiles.length === 0) {
						console.error("No sound files found in the directory");
						return;
					}

					const randomSoundFile = soundFiles[Math.floor(Math.random() * soundFiles.length)];
					playSound(`${soundSource}/${randomSoundFile}`);
				}
			};
		}
	},
});
function isValidUrl(string) {
	try {
		new URL(string);
		return true;
	} catch (_) {
		return false;
	}
}

async function fetchSoundFiles(directory) {
	// Simulate fetching sound files from the directory
	// Replace this with actual logic if needed
	return ["navi1.mp3", "navi2.mp3"];
}

function playSound(filePath) {
	const audio = new Audio(filePath);
	audio.play().catch(error => console.error('Error playing sound:', error));
}