export function create_date_string(date) {
    // date = new Date()
    const curr_date = new Date()

    if (curr_date.getDate() - date.getDate() === 0) {
        return "Сегодня"
    } else if (curr_date.getDate() - date.getDate() === 1) {
        return "Вчера"
    } else {
        const year_diff = date.getFullYear() - curr_date.getFullYear()
        let date_options = {day: 'numeric', month: 'long'}
        if (year_diff > 1) {
            date_options.year = 'numeric'
        }
        return date.toLocaleString('ru-ru', date_options)
    }
}