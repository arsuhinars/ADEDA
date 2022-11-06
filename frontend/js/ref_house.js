import { getToken } from "./auth.js"

/**
 * Метод загрузки таблицы с эталонами
 * @param {*} fileInput HTML элемент поля с выбранным файлом
 * @return промис с событием успешной загрузки таблицы. При успешной загрузке
 * первым аргументом будет передан список с объектами квартир
 */
export function loadTable(fileInput) {
    return new Promise((resolve, reject) => {
        let url = '/api/table/parse?token='
        url += encodeURIComponent(getToken())

        let data = new FormData()
        data.append('file', fileInput.files[0])

        fetch(url, {
            method: 'POST',
            body: data
        }).then((response) => {
            return response.json()
        }).then((json) => {
            if (json.error) {
                console.error('Error occured while loading table: \n', json)
                reject()
            } else {
                resolve(json)
            }
        }).catch((reason) => {
            console.error('Error occured while loading table: \n', reason)
            reject()
        })
    })
}
