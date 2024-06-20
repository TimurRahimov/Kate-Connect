import * as rq from "./requests.js"
import {user_online_observer} from "./observers.js"
import {button_handler} from "./button_handlers.js";
import {create_people_kaleidoscope} from "./people.js";


export async function input_handlers() {
    const inputs = document.getElementsByTagName('input')
    const text_areas = document.getElementsByTagName('textarea')
    for (let input of inputs) {
        let entity_type = input.getAttribute('entity_type')
        switch (entity_type) {
            case 'users':
                input.addEventListener("input", async () => {
                    let search_string = input.value
                    document.getElementById("kaleidoscope_container").hidden = !(search_string === "")
                    document.getElementById("people_container").hidden = (search_string === "")
                    if (input.value === "") {
                        await create_people_kaleidoscope()
                        return
                    }
                    let body = document.getElementsByTagName('body')[0]
                    let owner_id = body.getAttribute('user_id')
                    let owner_friends = await rq.get_friends(owner_id)
                    let users = await rq.search_users(search_string)
                    console.log(owner_friends)
                    console.log(users)

                    const people_container = document.getElementById('people_container')
                    people_container.innerHTML = ""

                    const yandexMusicRegExp = /https:\/\/music\.yandex\.ru\/album\/([0-9]+)\/track\/([0-9]+)/g
                    const yandexMusicExec = yandexMusicRegExp.exec(search_string)
                    if (yandexMusicExec !== null) {
                        const album_id = yandexMusicExec.at(1)
                        const track_id = yandexMusicExec.at(2)
                        const iframe_div = document.createElement('div')
                        iframe_div.classList.add('container')
                        people_container.appendChild(iframe_div)

                        const iframe = document.createElement('iframe')
                        iframe_div.appendChild(iframe)

                        iframe.style.border = 'none'
                        iframe.style.width = '100%'
                        iframe.style.height = '210px'
                        iframe.width = "100%"
                        iframe.height = "210px"
                        iframe.src = "https://music.yandex.ru/iframe/track/" + track_id + "/" + album_id

                        iframe.onload = (e) => {
                            console.log(e)
                            console.log(iframe)
                        }
                        return
                    }

                    for (let user of users) {
                        let user_template = document.getElementById('user_in_people_tmpl')
                        let user_row = document.createElement('div')
                        user_row.appendChild(user_template.content.cloneNode(true))
                        user_row.classList.add('container', 'people-list')
                        people_container.appendChild(user_row)
                        let user_a = user_row.getElementsByTagName('a')[0]
                        user_a.href += user['user_id']
                        let user_div = user_a.getElementsByTagName('div')[0]
                        user_div.setAttribute('user_id', user['user_id'])
                        let user_img = user_div.getElementsByTagName('img')[0]
                        user_online_observer.observe(user_div)
                        if (user['online'] === true) {
                            user_div.classList.add('online-in-people')
                        } else {
                            user_div.classList.remove('online-in-people')
                        }
                        if (user['avatar_link'] !== "") {
                            user_img.src = user['avatar_link']
                        }
                        let user_h4 = user_a.querySelector('h4')
                        user_h4.innerHTML = user['nickname']

                        let buttons_div = user_row.getElementsByClassName('user-in-people-buttons')[0]
                        let button_template = document.getElementById('button_in_people_tmpl')

                        let message_btn_node = button_template.content.cloneNode(true)
                        let message_btn = message_btn_node.querySelector('button')

                        if (owner_id !== user['user_id']) {
                            message_btn.setAttribute('onclick_type', 'connect')
                            message_btn.setAttribute('friend_id', user['user_id'])

                            let friend_btn_node = button_template.content.cloneNode(true)
                            let friend_btn = friend_btn_node.querySelector('button')
                            friend_btn.classList.add('btn-light')
                            friend_btn.setAttribute('friend_id', user['user_id'])
                            if (user['user_id'] in owner_friends) {
                                if (owner_friends[user['user_id']]['confirmed']) {
                                    friend_btn.setAttribute('onclick_type', 'delete_friend')
                                } else if (owner_friends[user['user_id']]['request']) {
                                    friend_btn.setAttribute('onclick_type', 'confirm_friend')
                                } else {
                                    friend_btn.setAttribute('onclick_type', 'cancel_friend')
                                }
                            } else {
                                friend_btn.setAttribute('onclick_type', 'add_friend')
                            }
                            await button_handler(friend_btn)
                            buttons_div.appendChild(friend_btn)
                        } else {
                            message_btn.setAttribute('onclick_type', 'connect')
                            message_btn.setAttribute('friend_id', user['user_id'])
                            message_btn.setAttribute('self', '')
                        }
                        await button_handler(message_btn)
                        buttons_div.appendChild(message_btn_node)
                    }
                })
                break
        }
    }
    for (let text_area of text_areas) {
        let entity_type = text_area.getAttribute('entity_type')
        switch (entity_type) {
            case 'messages':
                text_area.addEventListener("keydown", (e) => {
                    if (e.ctrlKey && e.key === 'Enter') {
                        e.preventDefault();
                        return true
                    } else if (e.key === 'Enter') {
                        e.preventDefault();
                        document.getElementById('send_message').click()
                    }
                })
                break
        }
    }
}