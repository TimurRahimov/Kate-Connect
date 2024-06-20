import {
    Ws_request,
    Ws_request_action,
    Ws_request_chat_data,
    Ws_request_message_data,
    Ws_request_type
} from "./requests/ws_request.js";
import {play_notification} from "../notification_creator.js";
import {create_chat_li, create_date_li, create_message_li} from "../elements_factory.js";
import {get_short_text} from "../utils.js";

let main_ws;

const ONCLOSE_TIMEOUT = 2000

const html_body = document.getElementsByTagName('body')[0]
const owner_user_id = html_body.getAttribute('user_id')

let message_list = [];
let message_first_load = true


export async function start_main_ws() {
    main_ws = new WebSocket("ws://" + document.location.host + "/ws/v1/")
    main_ws.onopen = async function () {
        // setInterval(async () => {
        //     query_messages()
        // }, 300)
    }
    main_ws.addEventListener("message", async function (event) {
        const message = JSON.parse(event.data)
        console.log(message)
        switch (message["event_type"]) {
            case "new_message":
                const messages_ul = document.getElementById("messages_ul")
                const chats_ul = document.getElementById("chats_ul")

                let page_chat_id = null
                let message_chat_id = message["data"]["chat"]["chat_id"]
                if (messages_ul === null) {
                } else {
                    page_chat_id = messages_ul.getAttribute('chat_id')
                    await append_message(messages_ul, message["data"])
                }

                let message_text = message["data"]["encoding"]
                let chat_find = false
                if (chats_ul !== null) {
                    let chats_li = chats_ul.querySelectorAll('li')
                    for (let chat_li of chats_li) {
                        if (message_chat_id === chat_li.getAttribute('chat_id')) {
                            let short_text = await get_short_text(message_text, 330)
                            if (short_text !== message_text)
                                short_text += "..."
                            chat_li.querySelector('span.chat_message_text_span').textContent = short_text
                            chat_li.setAttribute('last_message_timestamp', message["data"]["timestamp"])
                            chats_ul.insertBefore(chat_li, chats_ul.firstChild)
                            chat_find = true
                            break
                        }
                    }
                    if (chat_find === false) {
                        await append_chat(chats_ul, message["data"]["chat"], message["data"])
                    }
                }

                if (page_chat_id !== message_chat_id) {
                    if (message["data"]["from_user"]["user_id"] !== owner_user_id) {
                        await play_notification(
                            message["data"]["from_user"]["nickname"],
                            message["data"]["encoding"],
                            function () {
                                window.location.href = "/" + message["data"]["from_user"]["user_id"]
                            },
                            function () {
                                window.location.href = "/connect?_with=" + message["data"]["from_user"]["user_id"]
                            }
                        )
                    }
                }

                break
            case "get_message_result":
                const messages = message["data"]["messages"]
                await append_messages(messages)
                document.getElementById('messages_loading').hidden = true
                break
            case "get_chats_result":
                const chats = message["data"]["chats"]
                const last_messages = message["data"]["last_messages"]
                await append_chats(chats, last_messages)
                document.getElementById('chats_loading').hidden = true
                document.getElementById('chats_loading_boobs').hidden = true
                break
        }
    })
    main_ws.onclose = async function () {
        console.log("MAIN_WS close")
        setTimeout(async () => await start_main_ws(), ONCLOSE_TIMEOUT)
    }
}

export async function add_query_messages(chat_id, oldest_message_id, offset, count) {
    if (main_ws.readyState !== WebSocket.OPEN) {
        main_ws.addEventListener("open", function (event) {
            query_messages(chat_id, oldest_message_id, offset, count)
        })
    } else {
        query_messages(chat_id, oldest_message_id, offset, count)
    }
}

export async function add_query_chats() {
    if (main_ws.readyState !== WebSocket.OPEN) {
        main_ws.addEventListener("open", function (event) {
            query_chats()
        })
    } else {
        query_chats()
    }
}

async function append_message(message_container, message_event_model) {
    // console.log(messages.lastChild)
    const chat_id = message_container.getAttribute('chat_id')
    if (message_event_model["chat"]["chat_id"] !== chat_id)
        return
    let without_avatar = false
    let without_nickname = false
    if (message_container.childElementCount !== 0) {
        const last_message = message_container.lastChild
        const curr_date = new Date(message_event_model["timestamp"])
        const last_date = new Date(last_message.getAttribute('timestamp'))
        if (last_message.getAttribute('from_id') === message_event_model["from_user"]["user_id"]) {
            without_avatar = true
            without_nickname = true
        }
        if (curr_date.getFullYear() > last_date.getFullYear() ||
            curr_date.getMonth() > last_date.getMonth() ||
            curr_date.getDate() > last_date.getDate()) {
            without_avatar = false
            without_nickname = false
            message_container.append(await create_date_li(message_event_model["timestamp"]))
        }
    }
    const message_li = await create_message_li(
        message_event_model["message_id"],
        message_event_model["from_user"],
        message_event_model["timestamp"],
        message_event_model["encoding"],
        without_avatar,
        without_nickname
    )

    message_container.append(message_li)
    message_container.scrollTop = message_container.scrollHeight
}

async function append_messages(query_messages) {
    const messages = document.getElementById("messages_ul");
    if (messages === null)
        return
    for (let message of query_messages) {
        let without_avatar = false
        let without_nickname = false
        if (messages.childElementCount !== 0) {
            const last_message = messages.lastChild
            const curr_date = new Date(message["timestamp"])
            const last_date = new Date(last_message.getAttribute('timestamp'))
            if (last_message.getAttribute('from_id') === message["from_user"]["user_id"]) {
                without_avatar = true
                without_nickname = true
            }
            if (curr_date.getFullYear() > last_date.getFullYear() ||
                curr_date.getMonth() > last_date.getMonth() ||
                curr_date.getDate() > last_date.getDate()) {
                without_avatar = false
                without_nickname = false
                messages.append(await create_date_li(message["timestamp"]))
            }

            // console.log(curr_date.getFullYear())
            // console.log(curr_date.getMonth())
            // console.log(curr_date.getDate())
            // console.log(message["timestamp"])
            // console.log(last_message.getAttribute('timestamp'))
        }
        const message_li = await create_message_li(
            message["message_id"],
            message["from_user"],
            message["timestamp"],
            message["encodings"][owner_user_id]["encoding"],
            without_avatar,
            without_nickname
        )

        messages.append(message_li)
        messages.scrollTop = messages.scrollHeight
    }
}

async function append_chat(chats_container, chat, last_message) {
    let page_chat_id = null
    const chat_id = chat["chat_id"]
    let chat_title = chat["title"]
    let chat_avatar_url = chat["avatar_url"]
    let active_chat = false
    if (chat_title === null) {
        const members = chat["members"]
        if (members.length === 2) {
            if (members[0]["user_id"] !== owner_user_id) {
                chat_title = members[0]["nickname"]
                chat_avatar_url = members[0]["avatar_link"]
            } else {
                chat_title = members[1]["nickname"]
                chat_avatar_url = members[1]["avatar_link"]
            }
        }
    }

    let last_message_text = last_message["encoding"]
    let last_message_timestamp = last_message["timestamp"]

    let short_text = await get_short_text(last_message_text, 330)
    if (short_text !== last_message_text)
        short_text += "..."

    if (page_chat_id === chat_id) {
        active_chat = true
    }

    const chat_li = await create_chat_li(
        chat_id, chat_title, short_text, last_message_timestamp, chat_avatar_url, active_chat
    )
    chat_li.onclick = async function () {
        const new_chat_id = this.getAttribute('chat_id')
        window.history.pushState('connect', '', '/connect?_to_chat=' + new_chat_id)

        document.getElementById('chats_window').classList.remove('show_chats_window')
        document.getElementById('messages_window').classList.remove('show_chats_window')
        document.getElementById('mobile_return_to_chats').classList.remove('show_chats_window')

        document.getElementById('chats_window').classList.add('show_messages_window')
        document.getElementById('messages_window').classList.add('show_messages_window')
        document.getElementById('mobile_return_to_chats').classList.add('show_messages_window')

        document.getElementById("chat_title").textContent = this.querySelector('.chat_title_span').textContent

        const active_chat_div = document.getElementsByClassName('active_chat_div')[0]
        if (active_chat_div !== undefined) {
            active_chat_div.classList.remove("active_chat_div")
        }
        chat_li.querySelector('.chat_div').classList.add("active_chat_div")
        document.getElementById('send_message').setAttribute('chat_id', new_chat_id)

        const messages_ul = document.getElementById("messages_ul")
        messages_ul.innerHTML = ""
        messages_ul.setAttribute('chat_id', new_chat_id)

        document.getElementById('messages_loading').hidden = false
        await add_query_messages(new_chat_id, "", 0, -1)
    }
    if (chats_container.childElementCount === 0)
        chats_container.appendChild(chat_li)
    else
        chats_container.insertBefore(chat_li, chats_container.firstChild)
}

async function append_chats(query_chats, last_messages) {
    const chats_ul = document.getElementById("chats_ul")
    if (chats_ul === null)
        return

    const messages_ul = document.getElementById("messages_ul")
    let page_chat_id = null
    if (messages_ul !== null) {
        page_chat_id = messages_ul.getAttribute('chat_id')
    }

    if (query_chats.length > 1) {
        query_chats.sort(function (chat_1, chat_2) {
            if (chat_1["chat_id"] in last_messages && chat_2["chat_id"] in last_messages) {
                const chat_1_last_date = new Date(last_messages[chat_1["chat_id"]]["timestamp"])
                const chat_2_last_date = new Date(last_messages[chat_2["chat_id"]]["timestamp"])
                return chat_2_last_date - chat_1_last_date
            } else {
                return 0
            }
        })
    }

    for (let chat of query_chats) {
        const chat_id = chat["chat_id"]
        let chat_title = chat["title"]
        let chat_avatar_url = chat["avatar_url"]
        let active_chat = false
        if (chat_title === null) {
            const members = chat["members"]
            if (members.length === 2) {
                if (members[0]["user_id"] !== owner_user_id) {
                    chat_title = members[0]["nickname"]
                    chat_avatar_url = members[0]["avatar_link"]
                } else {
                    chat_title = members[1]["nickname"]
                    chat_avatar_url = members[1]["avatar_link"]
                }
            }
        }
        let last_message_text = "...None..."
        let last_message_timestamp = '1970-01-01T00:00:00Z'
        if (last_message_text.length !== 0) {
            if (chat_id in last_messages) {
                last_message_text = last_messages[chat_id]["encodings"][owner_user_id]["encoding"]
                last_message_timestamp = last_messages[chat_id]["timestamp"]
            }
        }

        let short_text = await get_short_text(last_message_text, 330)
        if (short_text !== last_message_text)
            short_text += "..."

        if (page_chat_id === chat_id) {
            active_chat = true
        }

        const chat_li = await create_chat_li(
            chat_id, chat_title, short_text, last_message_timestamp, chat_avatar_url, active_chat
        )
        chat_li.onclick = async function () {
            const new_chat_id = this.getAttribute('chat_id')
            window.history.pushState('connect', '', '/connect?_to_chat=' + new_chat_id)

            document.getElementById('chats_window').classList.remove('show_chats_window')
            document.getElementById('messages_window').classList.remove('show_chats_window')
            document.getElementById('mobile_return_to_chats').classList.remove('show_chats_window')

            document.getElementById('chats_window').classList.add('show_messages_window')
            document.getElementById('messages_window').classList.add('show_messages_window')
            document.getElementById('mobile_return_to_chats').classList.add('show_messages_window')

            document.getElementById("chat_title").textContent = this.querySelector('.chat_title_span').textContent

            const active_chat_div = document.getElementsByClassName('active_chat_div')[0]
            if (active_chat_div !== undefined) {
                active_chat_div.classList.remove("active_chat_div")
            }
            chat_li.querySelector('.chat_div').classList.add("active_chat_div")
            document.getElementById('send_message').setAttribute('chat_id', new_chat_id)

            messages_ul.innerHTML = ""
            messages_ul.setAttribute('chat_id', new_chat_id)
            document.getElementById('messages_loading').hidden = false

            await add_query_messages(new_chat_id, "", 0, -1)
        }

        chats_ul.append(chat_li)
    }
}

function query_messages(chat_id, oldest_message_id, offset, count) {
    const request = new Ws_request(
        Ws_request_type.MESSAGE,
        Ws_request_action.GET,
        new Ws_request_chat_data(
            chat_id,
            oldest_message_id,
            offset,
            count
        )
    )
    main_ws.send(request.json_string)
}

function query_chats() {
    const request = new Ws_request(
        Ws_request_type.CHAT,
        Ws_request_action.GET
    )
    main_ws.send(request.json_string)
}

export async function send_message(chat_id, encodings) {
    const request = new Ws_request(
        Ws_request_type.MESSAGE,
        Ws_request_action.SEND,
        new Ws_request_message_data(
            chat_id,
            encodings
        )
    )
}