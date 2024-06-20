import {cancel_friend, confirm_friend, delete_notification} from "./requests.js";
import {notifications_read_observer} from "./observers.js";
import {create_date_string} from "./text_creator.js";

const html_body = document.getElementsByTagName('body')[0]
const owner_user_id = html_body.getAttribute('user_id')


export async function create_notification_li(notification) {
    let notification_li = document.createElement("li");
    notification_li.setAttribute("notification_id", notification["notification_id"])

    const notification_delete_button = document.createElement("button");
    notification_li.appendChild(notification_delete_button)

    notification_delete_button.type = "button"
    notification_delete_button.classList.add("delete_notifications_button")
    notification_delete_button.setAttribute("aria-label", "Закрыть")

    const trash_icon = document.createElement("i")
    trash_icon.classList.add("bx", "bx-trash")

    notification_delete_button.appendChild(trash_icon)
    notification_delete_button.addEventListener("click", async () => {
            if (await delete_notification(notification["notification_id"])) {
                const notifications = document.getElementById("notifications-ul");
                const notifications_li = notifications.getElementsByTagName("li")
                const notifications_hr = notifications.getElementsByTagName("hr")

                for (let i in notifications_li) {
                    let notification_li = notifications_li[i]
                    if (notification_li.getAttribute("notification_id") === notification["notification_id"]) {
                        notifications.removeChild(notification_li)
                        const int_i = parseInt(i)
                        if (int_i !== notifications_li.length) {
                            notifications.removeChild(notifications_hr[int_i])
                        } else {
                            if (int_i !== 0) {
                                notifications.removeChild(notifications_hr[int_i - 1])
                            }
                        }
                        break
                    }
                }
            }
        }
    )

    const notification_div = document.createElement("div");
    notification_li.appendChild(notification_div)
    notification_div.classList.add("notification-div");

    const notification_text = document.createElement("span");
    notification_div.appendChild(notification_text)

    if (notification['notification_type'] === 1) {
        const user_link = document.createElement("a")
        notification_text.appendChild(user_link)
        user_link.href = "/" + notification['data']['friend_id']
        user_link.textContent = notification['data']['nickname']

        const text = document.createElement("span")
        notification_text.appendChild(text)
        text.textContent = " отправил заявку в друзья"

        const friend_buttons = document.createElement("div");
        friend_buttons.classList.add("user-in-notifications-buttons");

        const add_friend = document.createElement("button");
        add_friend.classList.add("btn", "btn-light", "btn-outline-success", "me-2", "button-in-people-buttons");
        add_friend.type = "button"
        add_friend.textContent = "Принять"
        add_friend.addEventListener("click", () => {
            confirm_friend(notification['data']['friend_id'])
        })

        const no_friend = document.createElement("button");
        no_friend.classList.add("btn", "btn-light", "btn-outline-danger", "me-2", "button-in-people-buttons");
        no_friend.type = "button"
        no_friend.textContent = "Отменить"
        no_friend.addEventListener("click", () => {
            cancel_friend(notification['data']['friend_id'])
        })

        friend_buttons.appendChild(add_friend)
        friend_buttons.appendChild(no_friend)

        notification_div.appendChild(friend_buttons)
    }

    const notification_time = document.createElement('span')
    notification_time.classList.add("notifications-time-span")
    notification_time.textContent = new Date(notification['timestamp']).toLocaleString()

    notification_li.appendChild(notification_time)

    if (notification["shown"] === "False") {
        notification_li.classList.add("unshown_message")
        notifications_read_observer.observe(notification_li)
    }

    return notification_li
}

export async function create_message_li(message_id, from_user, timestamp, message_text,
                                        without_avatar, without_nickname) {
    let message_li = document.createElement("li");
    const timestamp_date = new Date(timestamp)
    const date_string = timestamp_date.toLocaleDateString('ru-ru', {
        year: "numeric",
        month: "long",
        day: "numeric",
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    })
    const time_string = timestamp_date.toLocaleTimeString('ru-ru', {
        hour: '2-digit',
        minute: '2-digit',
    })
    message_li.setAttribute("message_id", message_id)
    message_li.setAttribute("timestamp", timestamp)
    message_li.setAttribute("from_id", from_user["user_id"])

    let message_div = document.createElement('div')
    message_div.classList.add("rounded-4", "shadow", "message_div")
    message_li.appendChild(message_div)

    if (from_user['user_id'] === owner_user_id) {
        message_li.style.alignSelf = "flex-end"
    } else {
        if (without_avatar !== true) {
            const message_avatar_img = document.createElement('img')
            message_avatar_img.src = from_user['avatar_link'] ? from_user['avatar_link'] : "/images/default_avatar.jpg"
            message_avatar_img.height = 40
            message_avatar_img.width = 40
            message_div.appendChild(message_avatar_img)
        }
    }

    if (without_nickname !== true) {
        const message_nickname_a = document.createElement('a')
        message_nickname_a.classList.add("message_nickname_a")
        message_nickname_a.textContent = from_user['nickname']
        message_nickname_a.href = "/" + from_user["user_id"]
        message_div.appendChild(message_nickname_a)
    }

    const message_text_span = document.createElement('span')
    message_text_span.classList.add("message_text_span")
    message_text_span.textContent = message_text
    message_div.appendChild(message_text_span)

    const message_timestamp_span = document.createElement('span')
    message_timestamp_span.classList.add("message_timestamp_span")
    message_timestamp_span.textContent = time_string
    message_timestamp_span.title = date_string
    message_div.appendChild(message_timestamp_span)

    return message_li
}

export async function create_chat_li(chat_id, chat_title, last_message_text,
                                     last_message_timestamp, chat_avatar_url,
                                     active_chat) {
    let chat_li = document.createElement("li");
    chat_li.setAttribute("chat_id", chat_id)
    chat_li.setAttribute("last_message_timestamp", last_message_timestamp)

    const chat_div = document.createElement("div")
    chat_div.classList.add("chat_div", "rounded-4")

    if (active_chat === true) {
        chat_div.classList.add("active_chat_div")
    }

    const chat_img = document.createElement("img")
    chat_img.src = chat_avatar_url ? chat_avatar_url : "/images/default_avatar.jpg"
    chat_img.height = 40
    chat_img.width = 40
    chat_div.appendChild(chat_img)

    const chat_title_message_div = document.createElement("div")
    chat_title_message_div.classList.add("chat_title_message_div")

    const chat_title_span = document.createElement("span")
    chat_title_span.classList.add("chat_title_span")
    chat_title_span.textContent = chat_title
    chat_title_message_div.appendChild(chat_title_span)

    const chat_message_text_span = document.createElement("span")
    chat_message_text_span.classList.add("chat_message_text_span")
    chat_message_text_span.textContent = last_message_text
    chat_title_message_div.appendChild(chat_message_text_span)

    chat_div.appendChild(chat_title_message_div)
    chat_li.appendChild(chat_div)

    return chat_li
}

export async function create_date_li(timestamp) {
    let date_li = document.createElement("li");
    date_li.classList.add("date_li")
    const date_div = document.createElement('div')
    date_div.classList.add("date_div", "rounded-4")
    date_div.textContent = create_date_string(new Date(timestamp))
    date_li.appendChild(date_div)
    return date_li
}