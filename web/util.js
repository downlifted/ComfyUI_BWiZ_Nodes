export const playSound = (file, volume) => {
    if (!file) {
        file = 'notify.mp3'
    }
    if (!file.startsWith('http')) {
        if (!file.includes('/')) {
            file = 'sounds/' + file
        }
        file = new URL(file, import.meta.url).href
    }
    const audio = new Audio(file)
    audio.volume = volume
    audio.play()
}

export const appQueueIsEmpty = async (app) => {
    if (app.ui.lastQueueSize !== 0) {
        await new Promise((r) => setTimeout(r, 500))
    }
    if (app.ui.lastQueueSize !== 0) {
        return false
    }
    return true
}