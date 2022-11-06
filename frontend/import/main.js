import { checkAuthorization } from "../js/auth.js"
import { loadTable } from "../js/ref_house.js"

document.addEventListener('DOMContentLoaded', () => {
    if (!checkAuthorization()) {
        window.location.href = '/errors/error401.html'
        return
    }
    
    let fileInput = document.querySelector('#upload-file')

    document.querySelector('#import-btn').addEventListener('click', (ev) => {
        fileInput.click()
    })
    fileInput.addEventListener('change', (ev) => {
        loadTable(fileInput)
            .then((houses) => {
                sessionStorage.setItem('references', JSON.stringify(houses))
                window.location.href = '/analog'
            })
            .catch(() => {
                alert('Произошла ошибка при импорте таблицы')
            })
    })
})
