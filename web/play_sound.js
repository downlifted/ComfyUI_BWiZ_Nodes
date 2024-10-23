import { app } from '../../../scripts/app.js'
import { playSound, appQueueIsEmpty } from './util.js'

app.registerExtension({
    name: 'Notifications.PlaySound',
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === 'BWIZ_NotificationSound') {
            const onExecuted = nodeType.prototype.onExecuted
            nodeType.prototype.onExecuted = async function (message) {
                onExecuted?.apply(this, arguments)
                
                if (message?.ui?.data) {
                    const data = JSON.parse(message.ui.data)
                    if (data.type === 'notification_sound') {
                        const { file, volume, mode } = data.data
                        if (mode === 'always' || (mode === 'on empty queue' && await appQueueIsEmpty(app))) {
                            playSound(file, volume)
                        }
                    }
                }
            }
        }
    },
})