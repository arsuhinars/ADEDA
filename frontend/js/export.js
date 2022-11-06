import { getToken } from "./auth.js"

/**
 * Функция конвертации и скачивания в виде таблицы полученные результаты
 * @param {*} ref_house объект квартиры-эталона
 * @param {*} analogs список объектов аналогов.
 * 
 * Формат объекта аналога:
 * - Поле `house` - объект квартира-аналога
 * - Поле `adjustments` - объект, содержащий значения корректировок. Если та или
 * иная корректирвока не используется, то она просто равна 0.
 * 
 * @returns Промис, который вызывает resolve при успешной загрузке, reject - если
 * произошла ошибка
 */
export function saveToTable(ref_house, analogs) {
    return new Promise((resolve, reject) => {
        let url = '/api/table/create?token='
        url += encodeURIComponent(getToken())

        fetch(url, {
            method: 'POST',
            body: JSON.stringify({reference: ref_house, analogs: analogs}),
            headers: {
                'Content-Type': 'application/json'
            }
        }).then((response) => {
            if (response.ok) {
                return response.blob()
            }

            response.json().then((err) => {
                console.error('Error occured while exporting table: \n', err)
            })

            reject()
        }).then((file) => {
            if (file) {
                let fileURL = URL.createObjectURL(file)

                let a = document.createElement('a')
                a.href = fileURL
                a.setAttribute('download', 'export.xlsx')
                a.click()
                
                resolve()
            }
        }).catch((reason) => {
            console.error('Error occured while exporting table: \n', reason)
            reject()
        })
    })
}
