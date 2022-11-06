import { checkAuthorization } from "../js/auth.js"
import { loadTable } from "../js/ref_house.js"

document.addEventListener('DOMContentLoaded', () => {
    if (!checkAuthorization()) {
        window.location.href = '/errors/error401.html'
        return
    }

    document.querySelector('#import-btn').addEventListener('click', (ev) => {
        let input = document.querySelector('#upload-file')
        input.click()

        loadTable(input)
            .then((houses) => {
                sessionStorage.setItem('references', JSON.stringify(houses))
                window.location.href = '/analog'
            })
            .catch(() => {
                alert('Произошла ошибка при импорте таблицы')
            })
    })
})
