export const Ws_request_type = {
    CHAT: 'chat',
    MESSAGE: 'message',
    NOTIFICATION: 'notification',
    ONLINE: 'online',
}

export const Ws_request_action = {
    SEND: 'send',
    GET: 'get',
}

export class Ws_request_chat_data {
    constructor(chat_id, oldest_message_id, offset, count) {
        this.chat_id = chat_id
        this.oldest_message_id = oldest_message_id
        this.offset = offset
        this.count = count
    }
}

export class Ws_request_message_data {
    constructor(chat_id, encodings) {
        this.chat_id = chat_id
        this.encodings = encodings
    }
}

export class Ws_request_notification_data {
    constructor(newest_notification_id) {
        this.newest_notification_id = newest_notification_id
    }
}

export class Ws_request {
    constructor(command_type, action, data) {
        this.command_type = command_type
        this.action = action
        this.data = data
    }

    get json_string() {
        return JSON.stringify({
            command_type: this.command_type,
            action: this.action,
            data: this.data
        })
    }
}