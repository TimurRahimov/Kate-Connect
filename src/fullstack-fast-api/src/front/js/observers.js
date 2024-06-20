// ===== Notification Read Observer =====
import {shown_notification} from "./requests.js";

const notifications_read_options = {
    root: null,
    threshold: 0.75,
};
const notifications_read_callback = async function (entries, observer) {
    for (let entry of entries) {
        if (entry.isIntersecting) {
            if (entry.target.getAttribute('shown') == null) {
                const notification_id = entry.target.getAttribute('notification_id')
                await shown_notification(notification_id)
                const notification_count_element = document.getElementById("notification-count")
                let unshown_count = parseInt(notification_count_element.textContent)
                unshown_count--
                notification_count_element.textContent = unshown_count.toString()
                notification_count_element.hidden = unshown_count === 0;
                entry.target.setAttribute('shown', "")

                setTimeout(function () {
                    const notifications = document.getElementById("notifications-ul");
                    const notifications_li = notifications.getElementsByTagName("li")
                    for (let n of notifications_li) {
                        if (n.getAttribute("notification_id") === notification_id) {
                            n.classList.remove("unshown_message")
                        }
                    }
                }, 3000)
            }
        }
    }
};

export let notifications_read_observer = new IntersectionObserver(
    notifications_read_callback,
    notifications_read_options);

// ===== User Online Observer =====
const user_online_options = {
    root: null,
    threshold: 0.75,
};
const user_online_callback = async function (entries, observer) {
    for (let entry of entries) {
        if (entry.isIntersecting) {
            if (entry.target.getAttribute('shown') == null) {
                users_online.set(entry.target.getAttribute('user_id'), false)
                // users_for_check.add(entry.target.getAttribute('user_id'))
            }
        }
    }
}
export let users_online = new Map()

export let user_online_observer = new IntersectionObserver(
    user_online_callback,
    user_online_options);