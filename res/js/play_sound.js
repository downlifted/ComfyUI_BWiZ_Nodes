import { app } from '../../../scripts/app.js'

app.registerExtension({
    name: 'Notifications.PlaySound',
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === '🧙🏼 BWIZ | Notification Sound (Navi)') {
            const onExecuted = nodeType.prototype.onExecuted
            nodeType.prototype.onExecuted = async function () {
                onExecuted?.apply(this, arguments)
                // Sound playing is now handled in the Python code
            }
        }
    },
})