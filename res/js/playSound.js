import { app } from "../../../scripts/app.js";

app.registerExtension({
	name: "BWIZ_UniversalNotification.PlaySound",
	async beforeRegisterNodeDef(nodeType, nodeData, app) {
		if (nodeData.name === "🧙🏼 BWIZ | Notification Sound (Navi)") {
			const onExecuted = nodeType.prototype.onExecuted;
			nodeType.prototype.onExecuted = async function () {
				onExecuted?.apply(this, arguments);
				if (this.widgets[0].value === "on empty queue") {
					if (app.ui.lastQueueSize !== 0) {
						await new Promise((r) => setTimeout(r, 500));
					}
					if (app.ui.lastQueueSize !== 0) {
						return;
					}
				}
				let file = this.widgets[2].value;
				if (!file) {
					file = "navi1.mp3";
				}
				if (!file.startsWith("http")) {
					if (!file.includes("/")) {
						file = "assets/" + file;
					}
					file = new URL(file, import.meta.url)
				}
				
				const url = new URL(file);
				const audio = new Audio(url);
				audio.volume = this.widgets[1].value;
				audio.play();
			};
		}
	},
});


