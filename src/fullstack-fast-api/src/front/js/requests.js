function getCookie(name) {
    let matches = document.cookie.match(new RegExp(
        "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ));
    return matches ? decodeURIComponent(matches[1]) : undefined;
}

export async function set_avatar_url(new_avatar_url) {
    let userId = getCookie("userId")

    let url = "/api/v1/users/" + userId + "/avatar";
    let request = {
        avatar_link: new_avatar_url
    }

    let response = await fetch(url, {
        method: 'POST',
        body: JSON.stringify(request),
        headers: {
            'Content-Type': 'application/json'
        }
    })

    if (response.status === 200) {
        window.location.reload()
    }
}

export async function edit_nickname(new_nickname) {
    let userId = getCookie("userId")
    let url = "/api/v1/users/" + userId + "/nickname"

    let response = await fetch(url, {
        method: 'PUT',
        body: "\"" + new_nickname + "\"",
        headers: {
            'Content-Type': 'application/json'
        }
    })

    return JSON.parse(await response.text())
}

export async function edit_avatar_link(new_avatar_link) {
    let userId = getCookie("userId")
    let url = "/api/v1/users/" + userId + "/avatar_link"

    let response = await fetch(url, {
        method: 'PUT',
        body: "\"" + new_avatar_link + "\"",
        headers: {
            'Content-Type': 'application/json'
        }
    })

    if (response.status === 200) {
        window.location.reload()
    }

    return JSON.parse(await response.text())
}

export async function add_friend(friend_id) {
    let userId = getCookie("userId")
    let url = "/api/v1/users/" + userId + "/friends";

    let response = await fetch(url, {
        method: 'POST',
        body: "\"" + friend_id + "\"",
        headers: {
            'Content-Type': 'application/json'
        }
    })

    return JSON.parse(await response.text())
}

export async function confirm_friend(friend_id) {
    let userId = getCookie("userId")
    let url = "/api/v1/users/" + userId + "/friends";
    let request = {
        friend_id: friend_id,
        confirmed: true
    }

    let response = await fetch(url, {
        method: 'PUT',
        body: JSON.stringify(request),
        headers: {
            'Content-Type': 'application/json'
        }
    })

    return JSON.parse(await response.text())
}

export async function delete_friend(friend_id) {
    let userId = getCookie("userId")
    let url = "/api/v1/users/" + userId + "/friends";

    let response = await fetch(url, {
        method: 'DELETE',
        body: "\"" + friend_id + "\"",
        headers: {
            'Content-Type': 'application/json'
        }
    })

    return JSON.parse(await response.text())
}

export async function get_friends(user_id) {
    let url = "/api/v1/users/" + user_id + "/friends"
    let response = await fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    return JSON.parse(await response.text());
}

export async function cancel_friend(friend_id) {
    let userId = getCookie("userId")
    let url = "/api/v1/users/" + userId + "/friends";

    location.reload()
}

export async function delete_notification(notification_id) {
    let url = "/api/v1/notifications";

    let response = await fetch(url, {
        method: 'DELETE',
        body: "\"" + notification_id + "\"",
        headers: {
            'Content-Type': 'application/json'
        }
    })

    return response.status === 200;
}

export async function shown_notification(notification_id) {
    let url = "/api/v1/notifications";

    let response = await fetch(url, {
        method: 'PUT',
        body: "\"" + notification_id + "\"",
        headers: {
            'Content-Type': 'application/json'
        }
    })

    return response.status === 200;
}

export async function get_random_people(count) {
    let url = "/api/v1/people?count=" + count.toString();

    let response = await fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })

    return JSON.parse(await response.text());
}

export async function auth(method) {
    let login = document.getElementById("login").value
    let password = document.getElementById("password").value

    let user = {
        login: login,
        password: password
    }
    let url;

    if (method === "register")
        url = "/api/v1/users/register"
    else if (method === "login")
        url = "/api/v1/users/login"
    else
        throw "Method not allowed"

    let response = await fetch(url, {
        method: 'POST',
        body: JSON.stringify(user),
        headers: {
            'Content-Type': 'application/json'
        }
    })

    if (response.status === 200) {
        let current_user = JSON.parse(await response.text())
        let session_id = current_user['session']['session_id']

        let user_id_cookie = "userId=" + current_user['user_id'] + ";"
        let session_id_cookie = "sessionId=" + session_id + ";"

        if (current_user['session']['expires'] !== null) {
            user_id_cookie += ("max-age=" + current_user['session']['expires'] + ";path=/;")
            session_id_cookie += ("max-age=" + current_user['session']['expires'] + ";path=/;")
        } else {
            user_id_cookie += "max-age=2678400;path=/;"
            session_id_cookie += "max-age=2678400;path=/;"
        }

        document.cookie = user_id_cookie
        document.cookie = session_id_cookie

        await new Audio("/sounds/usb_in.wav").play()
        await new Promise(resolve => setTimeout(resolve, 1200))
        window.location.reload()
    } else {
        alert(await response.text())
    }
}


export async function logout() {
    let response = await fetch('/api/v1/users/logout')

    if (response.status !== 200) {
        alert(await response.text())
    } else {
        await new Audio("/sounds/usb_out.wav").play()
        await new Promise(resolve => setTimeout(resolve, 1000))
        window.location.reload()
    }
}

export async function search_users(nickname) {
    let url = '/api/v1/search/users?search_string=' + nickname;
    let response = await fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })

    return JSON.parse(await response.text());
}

export async function send_message(chat_id, encodings) {
    let url = '/api/v1/messages/send';
    let request = {
        chat_id: chat_id,
        encodings: encodings
    }
    let response = await fetch(url, {
        method: 'POST',
        body: JSON.stringify(request),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    return JSON.parse(await response.text());
}

export async function get_chat(chat_id) {
    let url = '/api/v1/chats?chat_id=' + chat_id;
    let response = await fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })

    return JSON.parse(await response.text());
}