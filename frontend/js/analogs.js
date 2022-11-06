import { getToken } from "./auth.js"

/**
 * Класс поисковика аналогов
 * 
 * Поля-обработчики событий:
 * - `onUpdate` - вызывается при обновлении списка аналогов.
 * Первый аргумент - обновленный список
 * - `onError` - вызывается при возникновении ошибок
 * - `onEnd` - вызывается, когда поиск был прекращен или все аналоги уже были
 * найдены
 */
export class AnalogSearcher {
    /**
     * Конструктор класса
     * @param {*} ref_house объект квартиры-эталона для поиска
     * @param {*} adjustments объект используемых корректировок, где каждому полю
     * корректировки соотвествует булевое значение её состояния
     */
    constructor(ref_house, adjustments) {
        let url = 'ws://' + window.location.hostname + ':8000'
        url += '/api/search_houses?token='
        url += encodeURIComponent(getToken())

        this.ws = new WebSocket(url)
        this.ws.onopen = (ev) => {
            let query = {
                house: ref_house,
                adjustments: adjustments,
                max_house_count: 10
            }

            this.ws.send(JSON.stringify(query))
        }
        this.ws.onmessage = (ev) => {
            let response = JSON.parse(ev.data)
            
            if (response.error) {
                if (typeof(this.onError) == 'function') {
                    console.error('Error while analog searching: \n', response)
                    this.onError()
                }
            } else {
                if (typeof(this.onUpdate) == 'function') {
                    this.onUpdate(response)
                }
            }
        }
        this.ws.onclose = (ev) => {
            if (typeof(this.onEnd) == 'function') {
                this.onEnd()
            }
        }
        this.ws.onerror = (error) => {
            console.error('Error while analog searching: \n', error)
        }
    }
}
