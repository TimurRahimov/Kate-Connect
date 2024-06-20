export async function get_last_time_text(time = null) {
    let text_online = "Был(а) недавно"

    if (time == null || time === "") {
        return
    }

    let last_time_online = new Date(time)
    const diff = Math.ceil(Math.abs(last_time_online.getTime() - new Date().getTime()) / (1000 * 60))

    // console.log(diff)
    if (diff < 60) {
        text_online = "Был(а) онлайн " + diff
        if (diff === 0) {
            text_online = "Был(а) онлайн только что"
        } else if (diff === 1) {
            text_online = text_online + " минуту назад"
        } else if (diff === 2 || diff === 3 || diff === 4) {
            text_online = text_online + " минуты назад"
        } else if (diff <= 20) {
            text_online = text_online + " минут назад"
        } else {
            if (diff % 10 === 1) {
                text_online = text_online + " минуту назад"
            } else if (diff % 10 <= 4) {
                text_online = text_online + " минуты назад"
            } else {
                text_online = text_online + " минут назад"
            }
        }
    } else if (diff < 1440) {
        if (diff < 120) {
            text_online = "Был(а) онлайн час назад"
        } else {
            for (let i = 2; i < 30; i++) {
                if (diff > 60 * i) {
                    text_online = "Был(а) онлайн " + i
                    if (i === 2 || i === 3 || i === 4) {
                        text_online = text_online + " часа назад"
                    } else if (i <= 20) {
                        text_online = text_online + " часов назад"
                    } else {
                        if (i % 10 === 1) {
                            text_online = text_online + " час назад"
                        } else if (i % 10 <= 4) {
                            text_online = text_online + " часа назад"
                        } else {
                            text_online = text_online + " часов назад"
                        }
                    }
                }
            }
        }
    } else {
        const options = {
            month: 'long',
            day: 'numeric',
            timezone: 'UTC',
            hour: 'numeric',
            minute: 'numeric',
        };

        text_online = "Был(а) онлайн " + last_time_online.toLocaleString("ru", options)
    }

    return text_online
}

export async function get_short_text(text, max_width) {
    let size_div = document.getElementById('_calc_text_size')
    size_div.removeAttribute('hidden')
    size_div.innerHTML = text
    let last_message_text_length = text.length

    while (size_div.offsetWidth > max_width) {
        size_div.innerHTML = text.slice(0, --last_message_text_length)
    }

    size_div.setAttribute('hidden', '')
    return size_div.innerHTML
}