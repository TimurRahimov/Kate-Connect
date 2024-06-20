import {get_random_people} from "./requests.js";


export async function create_people_kaleidoscope() {
    let people = await get_random_people(16)
    const kaleidoscope_element = document.getElementById('kaleidoscope')
    if (kaleidoscope_element === null) {
        return
    }
    kaleidoscope_element.innerHTML = ""
    let milk_background_div = document.createElement('div')
    let milk_background_img = document.createElement('img')
    milk_background_div.classList.add('milk-background')
    milk_background_div.appendChild(milk_background_img)
    milk_background_img.classList.add('milk-background')
    milk_background_img.src = "/images/milk.png"
    kaleidoscope_element.appendChild(milk_background_div)
    for (let element of await create_kaleidoscope(people)) {
        kaleidoscope_element.appendChild(element)
    }
}

async function create_kaleidoscope(users) {
    if (users.length >= 16) {
        users = users.slice(0, 16)
    } else if (users.length >= 11) {
        users = users.slice(0, 11)
    } else if (users.length >= 7) {
        users = users.slice(0, 7)
    } else if (users.length >= 0) {
        users = users.slice(0, users.length)
    }

    let version = users.length

    let kaleidoscope = []

    for (let user_index in users) {
        const element_number = parseInt(user_index) + 1
        const user_element = document.createElement('div')
        const u_img = document.createElement('img')
        user_element.classList.add("kaleidoscope-absolute")
        u_img.src = users[user_index]['avatar_link']
        if (users[user_index]['avatar_link'] === '') {
            u_img.src = "/images/default_avatar.jpg"
        }
        if (version <= 4) {
            u_img.classList.add("kaleidoscope-element-default")
            user_element.classList.add("kaleidoscope-" + version + "-" + element_number)
        } else if (version === 5) {
            u_img.classList.add("kaleidoscope-element-default")
            user_element.classList.add("kaleidoscope-5-" + (element_number + 1))
        } else if (version === 6) {
            u_img.classList.add("kaleidoscope-element-default")
            user_element.classList.add("kaleidoscope-7-" + (element_number + 1))
        } else if (version === 7) {
            u_img.classList.add("kaleidoscope-element-default")
            user_element.classList.add("kaleidoscope-7-" + element_number)
        } else if (version === 11) {
            if (element_number <= 6) {
                u_img.classList.add("kaleidoscope-element-default")
                user_element.classList.add("kaleidoscope-5-" + element_number)
            } else {
                u_img.classList.add("kaleidoscope-element-medium")
                user_element.classList.add("kaleidoscope-11-" + element_number)
            }
        } else if (version === 16) {
            if (element_number <= 6) {
                u_img.classList.add("kaleidoscope-element-default")
                user_element.classList.add("kaleidoscope-5-" + element_number)
            } else if (element_number <= 11) {
                u_img.classList.add("kaleidoscope-element-medium")
                user_element.classList.add("kaleidoscope-11-" + element_number)
            } else {
                u_img.classList.add("kaleidoscope-element-small")
                user_element.classList.add("kaleidoscope-11-" + element_number)
            }
        }
        const a = document.createElement('a')
        a.href = users[user_index]['user_id']
        a.title = users[user_index]['nickname']
        a.appendChild(u_img)
        user_element.appendChild(a)
        kaleidoscope.push(user_element)
    }
    return kaleidoscope
}