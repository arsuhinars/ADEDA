import { HouseAdjustments } from "../js/house.js"
import { AnalogSearcher } from "../js/analogs.js"
import { saveToTable } from "../js/export.js"

function createAnalogHTML(analog, adjustments) {
    return `
        <details>
        <summary>${analog.location} (${analog.floor} этаж из ${analog.floors_count}) ${analog.metro_distance} м. от ${analog.metro_station}</summary>
        <h1>Внесите корректировки</h1>
        <p>Площадь</p>
        <input name="flat_area" type="number" value="${adjustments.area}" />
        <p>Удаленность от метро</p>
        <input name="metro_distance" type="number" value="${adjustments.metro}" />
        <p>Площадь кухни</p>
        <input name="kitchen_area" type="number" value="${adjustments.kitchen_area}" />
        <p>Этаж</p>
        <input name="floor" type="number" value="${adjustments.floor}" />
        <p>Наличие балкона/лоджии</p>
        <input name="has_balcony" type="number" value="${adjustments.balcony}" />
        <p>Ремонт</p>
        <input name="renovation" type="number" value="${adjustments.repairs}" />
        </details>
    `
}

document.addEventListener('DOMContentLoaded', () => {
    let currRef = JSON.parse(sessionStorage.getItem('curr_ref'))
    let checkList = {
        trade: true,
        area: true,
        metro: true,
        floor: true,
        kitchen_area: true,
        balcony: true,
        repairs: true
    }

    let searcher = new AnalogSearcher(
        currRef,
        checkList
    )

    let analogElem = document.querySelector('div.analog')
    let currAnalogs

    let adjustments = new Map()
    searcher.onUpdate = (analogs) => {
        analogElem.innerHTML = ''

        currAnalogs = analogs

        for (let i = 0; i < analogs.length; i++) {
            if (!adjustments.has(analogs[i].id)) {
                adjustments.set(i, HouseAdjustments.calcFor(currRef, analogs[i], checkList))
            }

            analogElem.innerHTML += createAnalogHTML(analogs[i], adjustments.get(i))
        }
    }

    document.querySelector('#import-btn').addEventListener('click', (ev) => {
        saveToTable(currRef, currAnalogs.map((el, i) => {
            return {
                house: el,
                adjustments: adjustments.get(i)
            }
        }))
        ev.preventDefault()
    })
})