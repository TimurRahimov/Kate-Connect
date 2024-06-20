import * as rq from "./requests.js"

const state_flow = {
    'cancel_friend': 'add_friend',
    'delete_friend': 'add_friend',
    'confirm_friend': 'delete_friend',
    'add_friend': 'cancel_friend'
}


export async function button_style_reload(button, onclick_type) {
    if (onclick_type === undefined)
        onclick_type = button.getAttribute('onclick_type')
    switch (onclick_type) {
        case 'cancel_friend':
            button.classList.remove(...button.classList)
            button.classList.add('btn', 'me-2', 'button-in-people-buttons', 'btn-dark', 'btn-outline-danger')
            button.innerHTML = "Отменить заявку"
            break
        case 'delete_friend':
            button.classList.remove(...button.classList)
            button.classList.add('btn', 'me-2', 'button-in-people-buttons', 'btn-dark', 'btn-outline-danger')
            button.innerHTML = "Удалить из друзей"
            break
        case 'confirm_friend':
            button.classList.remove(...button.classList)
            button.classList.add('btn', 'me-2', 'button-in-people-buttons', 'btn-dark', 'btn-outline-success')
            button.innerHTML = "Принять заявку"
            break
        case 'add_friend':
            button.classList.remove(...button.classList)
            button.classList.add('btn', 'me-2', 'button-in-people-buttons', 'btn-dark')
            button.innerHTML = "Добавить в друзья"
            break
        case 'connect':
            button.classList.remove(...button.classList)
            button.classList.add('btn', 'me-2', 'button-in-people-buttons', 'btn-dark')
            if (button.getAttribute('self') === '') {
                button.innerHTML = "Написать сообщение себе"
            } else {
                button.innerHTML = "Написать сообщение"
            }
            break
        case 'send_message':
            button.classList.remove(...button.classList)
            button.classList.add('btn', 'me-2', 'button-in-people-buttons', 'btn-dark')
            if (button.getAttribute('self') === '') {
                button.innerHTML = "На память"
            } else {
                button.innerHTML = "Отправить"
            }
    }
}

export async function button_handler(button) {
    // let friend_id = button.getAttribute('friend_id')
    const onclick_type = button.getAttribute('onclick_type')
    await button_style_reload(button, onclick_type)
    switch (onclick_type) {
        case 'cancel_friend':
            button.onclick = async () => {
                const friend_id = button.getAttribute('friend_id')
                if (await rq.delete_friend(friend_id)) {
                    button.setAttribute('onclick_type', state_flow[onclick_type])
                    await button_style_reload(button, state_flow[onclick_type])
                    await button_handler(button)
                }
            }
            break
        case 'delete_friend':
            button.onclick = async () => {
                const friend_id = button.getAttribute('friend_id')
                if (await rq.delete_friend(friend_id)) {
                    button.setAttribute('onclick_type', state_flow[onclick_type])
                    await button_style_reload(button, state_flow[onclick_type])
                    await button_handler(button)
                }
            }
            break
        case 'confirm_friend':
            button.onclick = async () => {
                const friend_id = button.getAttribute('friend_id')
                if (await rq.confirm_friend(friend_id)) {
                    button.setAttribute('onclick_type', state_flow[onclick_type])
                    await button_style_reload(button, state_flow[onclick_type])
                    await button_handler(button)
                }
            }
            break
        case 'add_friend':
            button.onclick = async () => {
                const friend_id = button.getAttribute('friend_id')
                if (await rq.add_friend(friend_id)) {
                    button.setAttribute('onclick_type', state_flow[onclick_type])
                    await button_style_reload(button, state_flow[onclick_type])
                    await button_handler(button)
                }
            }
            break
        case 'login':
            button.onclick = async function () {
                await rq.auth('login')
            }
            break
        case 'register':
            button.onclick = async function () {
                await rq.auth('register')
            }
            break
        case 'logout':
            button.onclick = async function () {
                await rq.logout()
            }
            break
        case 'connect':
            button.onclick = async function () {
                const friend_id = button.getAttribute('friend_id')
                window.location.href = "/connect?_with=" + friend_id
            }
            break
        case 'send_message':
            button.onclick = async function () {
                let input_message = document.getElementById('input_message')
                if (input_message.value === "") {
                    return
                }
                const chat_id = button.getAttribute('chat_id')
                const chat = await rq.get_chat(chat_id)
                let encodings = {}
                for (let member_user of chat["members"]) {
                    console.log(member_user)
                    encodings[member_user["user_id"]] = input_message.value
                }

                await rq.send_message(chat_id, encodings)
                input_message.value = ""
                // window.location.reload()
            }
            break
        case 'change':
            button.onclick = async function () {
                if (button.getAttribute('edit') != null) {
                    button.classList.remove("btn-outline-success")
                    button.removeAttribute('edit')
                    button.textContent = "Изменить"
                } else {
                    button.classList.add("btn-outline-success")
                    button.setAttribute('edit', '')
                    button.textContent = "Сохранить"
                }
                switch (button.getAttribute('change_type')) {
                    case 'nickname':
                        const edit_nickname = document.getElementById("settings_nickname")
                        if (button.getAttribute('edit') != null) {
                            edit_nickname.removeAttribute('disabled')
                        } else {
                            if (await rq.edit_nickname(edit_nickname.value) === true) {
                                edit_nickname.setAttribute('disabled', '')
                            }
                        }
                        break
                    case 'password':
                        break
                    case 'avatar_link':
                        const edit_avatar_link = document.getElementById("settings_avatar_link")
                        if (button.getAttribute('edit') != null) {
                            edit_avatar_link.removeAttribute('disabled')
                        } else {
                            if (await rq.edit_avatar_link(edit_avatar_link.value) === true) {
                                edit_avatar_link.setAttribute('disabled', '')
                            }
                        }
                        break
                }
            }
            break
        case 'return_to_chats':
            button.onclick = async function () {
                const active_chat_div = document.getElementsByClassName('active_chat_div')[0]
                if (active_chat_div !== undefined) {
                    active_chat_div.classList.remove("active_chat_div")
                }
                window.history.pushState('connect', '', '/connect')
                document.getElementById("chat_title").textContent = ""
                document.getElementById("send_message").setAttribute('chat_id', '')
                document.getElementById("messages_ul").setAttribute('chat_id', '')
                document.getElementById("messages_ul").innerHTML = ""

                document.getElementById('chats_window').classList.remove('show_messages_window')
                document.getElementById('messages_window').classList.remove('show_messages_window')
                document.getElementById('mobile_return_to_chats').classList.add('show_messages_window')

                document.getElementById('chats_window').classList.add('show_chats_window')
                document.getElementById('messages_window').classList.add('show_chats_window')
                document.getElementById('mobile_return_to_chats').classList.add('show_chats_window')

            }
            break
    }
}

export async function button_handlers() {
    for (let button of document.getElementsByTagName('button')) {
        await button_handler(button)
    }
}
