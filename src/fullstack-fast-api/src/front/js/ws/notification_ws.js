import {create_notification_li} from "../elements_factory.js";
import {stub_async} from "./_stub_async.js";

let notification_ws;

export async function start_notification_ws() {
    notification_ws = new WebSocket("ws://" + document.location.host + "/ws/v1/notifications")

    notification_ws.addEventListener("message", async function (event) {
        const notifications_list = JSON.parse(event.data);
        const last_notification = notifications_list[0]

        if (last_notification !== undefined) {
            const toastLiveExample = document.getElementById('liveToast')
            const toastBootstrap = bootstrap.Toast.getOrCreateInstance(toastLiveExample)

            const notification_top = document.getElementById('notification-top')
            const notification_body = document.getElementById('notification-body')

            notification_top.textContent = "Kate Connect"
            notification_body.textContent = last_notification["notification_text"]

            toastBootstrap.show()
            await prepend_notifications(notifications_list)

            await new Audio("/sounds/notification1.wav").play()
            await new Promise(resolve => setTimeout(resolve, 1200))

            await stub_async()
        }
    });

    notification_ws.onclose = async function () {
        setTimeout(async () => await start_notification_ws(), 500)
    }

    setInterval(() => {
        if (notification_ws.readyState === 1)
            notification_ws_send_in_socket(notification_ws)
    }, 300)
}

function notification_ws_send_in_socket(notification_ws) {
    let newest_notification_id = null;
    const notifications = document.getElementById("notifications-ul");
    const notifications_li = notifications.getElementsByTagName("li")

    if (notifications_li.length !== 0) {
        newest_notification_id = notifications_li[0].getAttribute("notification_id")
    }

    notification_ws.send(JSON.stringify({
        newest_notification_id: newest_notification_id,
    }))
}

async function prepend_notifications(newest_notifications_list) {
    newest_notifications_list.reverse()
    const notifications = document.getElementById("notifications-ul");
    const notification_count_element = document.getElementById("notification-count")
    let unshown_count = 0

    if (!notification_count_element.hidden) {
        unshown_count = parseInt(notification_count_element.textContent)
    }

    for (let i in newest_notifications_list) {
        let notification = newest_notifications_list[i]

        if (notification["shown"] === "False") {
            unshown_count++
        }

        let notification_li = await create_notification_li(notification)

        if (notifications.childNodes.length > 0) {
            const notifications_hr = document.createElement('hr')
            notifications_hr.classList.add("notifications_hr")
            notifications.prepend(notifications_hr)
        }

        notifications.prepend(notification_li)
    }

    notification_count_element.textContent = unshown_count.toString()
    notification_count_element.hidden = unshown_count === 0;
}
