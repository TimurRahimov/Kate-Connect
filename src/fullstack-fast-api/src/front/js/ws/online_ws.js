import {users_online} from "../observers.js";
import {get_last_time_text} from "../utils.js";
import {stub_async} from "./_stub_async.js";

let online_ws;

export async function start_online_ws() {
    online_ws = new WebSocket("ws://" + document.location.host + "/ws/v1/online")

    online_ws.addEventListener("message", async function (event) {
        const online_dict = JSON.parse(event.data);
        const user_people_avatars = document.getElementsByClassName("avatar-in-people")
        const user_page_avatars = document.getElementsByClassName("avatar-in-user-page")
        const last_time_online = document.getElementsByClassName('last_time_online')

        for (let user_people of user_people_avatars) {
            const user_id = user_people.getAttribute('user_id')
            const user_online_dict = online_dict[user_id]
            if (user_online_dict != null) {
                users_online[user_id] = user_online_dict
                if (user_online_dict['online'] === true) {
                    user_people.classList.add('online-in-people')
                } else {
                    user_people.classList.remove('online-in-people')
                }
            }
        }

        for (let user_page of user_page_avatars) {
            const user_id = user_page.getAttribute('user_id')
            const user_online_dict = online_dict[user_id]
            if (user_online_dict != null) {
                users_online[user_id] = user_online_dict
                if (user_online_dict['online'] === true) {
                    user_page.classList.add('online-in-user-page')
                } else {
                    user_page.classList.remove('online-in-user-page')
                }
            }
        }

        if (last_time_online.length > 0) {
            const user_id = last_time_online[0].getAttribute('user_id')
            if (users_online[user_id]['online'] === true) {
                last_time_online[0].textContent = "Онлайн"
            } else {
                last_time_online[0].textContent = await get_last_time_text(users_online[user_id]['last_time_online'])
            }
        }

        await stub_async()
    })

    online_ws.onclose = async function () {
        setTimeout(async () => await start_online_ws(), 500)
    }

    setInterval(() => {
        if (online_ws.readyState === 1)
            online_ws.send(JSON.stringify({
                users_for_check: Array.from(users_online.keys())
            }))
    }, 300)
}
