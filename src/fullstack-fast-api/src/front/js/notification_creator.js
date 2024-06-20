export async function play_notification(top_text, bottom_text, top_onclick, body_onclick) {
    const toastLiveExample = document.getElementById('liveToast')
    const toastBootstrap = bootstrap.Toast.getOrCreateInstance(toastLiveExample)

    const notification_top = document.getElementById('notification-top')
    const notification_body = document.getElementById('notification-body')

    notification_top.textContent = top_text
    notification_body.textContent = bottom_text

    if (top_onclick !== undefined) {
        notification_top.onclick = top_onclick
    }

    if (body_onclick !== undefined) {
        notification_body.onclick = body_onclick
    }
    toastLiveExample.addEventListener("hide.bs.toast", function () {
        notification_top.onclick = null
        notification_body.onclick = null
    })

    toastBootstrap.show()
    await new Audio("/sounds/notification1.wav").play()
    // await new Promise(resolve => setTimeout(resolve, 1200))
}