import {notifications_read_observer, user_online_observer, users_online} from "./observers.js"
import {button_handlers} from "./button_handlers.js"
import {input_handlers} from "./input_handlers.js"
import {create_people_kaleidoscope} from "./people.js";
import {delete_notification} from "./requests.js";
import {create_notification_li} from "./elements_factory.js";
import {get_last_time_text} from "./utils.js";
import {start_notification_ws} from "./ws/notification_ws.js";
import {start_online_ws} from "./ws/online_ws.js";
import {add_query_chats, add_query_messages, start_main_ws} from "./ws/main_ws.js";


// document.addEventListener("DOMContentLoaded", async function() {
//     let users_time_online = document.getElementsByClassName("last_time_online")
//     for (let user_time_online of users_time_online) {
//         const user_id = user_time_online.getAttribute('user_id')
//
//     }
// })

document.addEventListener("DOMContentLoaded", async function () {
    let users_avatars = document.getElementsByClassName("avatar-in-people")
    for (let user_avatar of users_avatars) {
        user_online_observer.observe(user_avatar)
    }
})

console.log("123")

document.addEventListener("DOMContentLoaded", async function () {
    await button_handlers()
    await input_handlers()
    const html_body = document.getElementsByTagName('body')[0]
    const owner_user_id = html_body.getAttribute('user_id')

    await first_fill_user_page()
    await create_people_kaleidoscope()

    if (owner_user_id == null) {
        return
    }

    await first_fill_notifications()

    let user_page_avatars = document.getElementsByClassName("avatar-in-user-page")
    if (user_page_avatars.length > 0) {
        users_online.set(user_page_avatars[0].getAttribute('user_id'), {online: false})
    }

    await start_notification_ws()
    await start_online_ws()
    await start_main_ws()
    await add_query_chats()
    //
    if (window.location.pathname.startsWith('/connect')) {
        let messages_ul = document.getElementById("messages_ul")
        if (messages_ul !== null) {
            const chat_id = messages_ul.getAttribute('chat_id')
            if (chat_id !== "") {
                await add_query_messages(chat_id, "", 0, -1)
            }
        }
    }
    // await start_message_ws()
    console.log(window.location.pathname)

    let notifications_ul = document.getElementById("notifications-ul");
    if (notifications_ul != null) {
        notifications_ul.onclick = function (event) {
            event.stopPropagation();
        }
    }
});


async function stub_async() {
}



const notification_type = {
    1: "ADD_FRIEND",  // О запросе дружбы
    2: "CONFIRMED_FRIEND",  // О подтверждении дружбы
    3: "DELETE_FRIEND"  // Об удалении из списка друзей
}

async function first_fill_notifications() {
    let url = "/api/v1/notifications?";
    url += ("limit=" + 10 + "&")
    url += ("offset=" + 0 + "&")
    url += ("order=" + true)

    let response = await fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })

    let notifications_list = JSON.parse(await response.text())
    await fill_notifications(notifications_list)
}

async function first_fill_people() {
    let url = "/api/v1/online?";
    url += ("limit=" + 10 + "&")
    url += ("offset=" + 0 + "&")
    url += ("order=" + true)

    let response = await fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })


}

async function first_fill_user_page() {
    const user_page_avatars = document.getElementsByClassName("avatar-in-user-page")
    const last_time_online = document.getElementsByClassName('last_time_online')

    if (user_page_avatars.length === 0) {
        return
    }

    const user_id = user_page_avatars[0].getAttribute('user_id')

    let response = await fetch("/api/v1/users/" + user_id + "/online", {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })

    users_online[user_id] = JSON.parse(await response.text())

    if (users_online[user_id]['online'] === true) {
        user_page_avatars[0].classList.add('online-in-user-page')
        if (last_time_online.length > 0)
            last_time_online[0].textContent = "Онлайн"
    } else {
        user_page_avatars[0].classList.remove('online-in-user-page')
        if (last_time_online.length > 0)
            last_time_online[0].textContent = await get_last_time_text(users_online[user_id]['last_time_online'])
    }
}



async function fill_notifications(notifications_list) {
    const notifications = document.getElementById("notifications-ul");
    if (notifications == null) {
        return
    }

    notifications.innerHTML = ""
    const notification_count = notifications_list.length
    let unshown_count = 0

    for (let i in notifications_list) {
        let notification = notifications_list[i]

        if (notification["shown"] === "False") {
            unshown_count++
        }

        let notification_li = await create_notification_li(notification)

        notifications.appendChild(notification_li)

        if (parseInt(i) !== notification_count - 1) {
            const notifications_hr = document.createElement('hr')
            notifications_hr.classList.add("notifications_hr")
            notifications.appendChild(notifications_hr)
        }
    }

    document.getElementById("notification-count").textContent = unshown_count.toString()
    document.getElementById("notification-count").hidden = unshown_count === 0;
}

