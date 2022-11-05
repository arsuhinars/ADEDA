
const AREA_RANGES = [30, 50, 65, 90, 120]
const AREA_TABLE = [
    [0, -6, -12, -17, -22, -24],
    [6, 0, -7, -12, -17, -19],
    [14, 7, 0, -6, -11, -13],
    [21, 14, 6, 0, -6, -8],
    [28, 21, 13, 6, 0, -3],
    [31, 24, 16, 9, 3, 0]
]
const KITCHEN_RANGES = [7, 10]
const KITCHEN_TABLE = [
    [0, 3, 9],
    [-2.9, 0, 5.8],
    [-8.3, -5.5, 0]
]
const METRO_RANGES = [5, 10, 15, 30, 60]
const METRO_TABLE = [
    [0, -7, -11, -15, -19, -22],
    [7, 0, -4, -8, -13, -17],
    [12, 4, 0, -5, -10, -13],
    [17, 9, 5, 0, -6, -9],
    [24, 15, 11, 6, 0, -4],
    [29, 20, 15, 10, 4, 0]
]

function findRange(x, range) {
    for (let i = 0; i < range.length; i++) {
        if (x < range[i]) {
            return i;
        }
    }
    return range.length;
}

/** Перечисление сегмента дома */
export const HouseSegment = {
    NEW: 'new',
    MODERN: 'modern',
    OLD: 'old',
}

/** Человеко-читаемое представление сегмента дома */
export const VerboseHouseSegment = {
    [HouseSegment.NEW]: 'Новостройка',
    [HouseSegment.MODERN]: 'Современное жилье',
    [HouseSegment.OLD]: 'Старый жилой фонд',
}

/** Перечисление материала стен дома */
export const HouseMaterial = {
    BRICK: 'brick',
    PANEL: 'panel',
    MONOLIT: 'monolit',
}

/** Человеко-читаемое представление материала стен */
export const VerboseHouseMaterial = {
    [HouseMaterial.BRICK]: 'Кирпич',
    [HouseMaterial.PANEL]: 'Панель',
    [HouseMaterial.MONOLIT]: 'Монолит',
}

/** Перечисление состояний дома */
export const HouseState = {
    NO_DECORATION: 'no',
    STATE_DECORATION: 'state',
    MODERN_DECORATION: 'modern',
}

/** Человеко-читаемое представление состояний дома */
export const VerboseHouseState = {
    [HouseState.NO_DECORATION]: 'Без отделки',
    [HouseState.STATE_DECORATION]: 'Муниципальный ремонт',
    [HouseState.MODERN_DECORATION]: 'Современная отделка'
}

/** Перечисление источника данных */
export const SourceService = {
    AVITO: 'avito',
    CIAN: 'cian',
}

/** Человеко-читаемое представление источника данных */
export const VerboseSourceService = {
    [SourceService.AVITO]: 'Avito',
    [SourceService.CIAN]: 'Циан',
}

/** 
 * Объект корректировок дома. Корректировки записаны в процентах
*/
export class HouseAdjustments {
    constructor(
        trade=0, area=0, metro=0, floor=0,
        kitchen_area=0, balcony=0, repairs=0
        ) {
        this.trade = trade
        this.area = area
        this.metro = metro
        this.floor = floor
        this.kitchen_area = kitchen_area
        this.balcony = balcony
        this.repairs = repairs
    }

    /**
     * Вычислить корректировки для аналога
     * @param {*} reference объект квартиры - эталона
     * @param {*} analog объект квартиры - аналога
     * @param {*} check_list объект, у которого к каждому полю корректировки
     * соотвествует булевое значение, соотвествующее тому, используется ли она
     * или нет
     * @returns объект корректировок
     */
    static calcFor(reference, analog, check_list) {
        let adjustments = new HouseAdjustments()

        // Корректировка на торг
        if (check_list.trade) {
            adjustments.trade = -4.5
        }

        // Корректировка на этаж
        if (check_list.floor && reference.floor != analog.floor) {
            if (analog.floor == 1) {
                adjustments.floor = 
                    (reference.floor == reference.floors_count) ?
                    3.2 : 7.5;
            } else if (analog.floor == analog.floors_count) {
                adjustments.floor = 
                    (reference.floor == 1) ? 3.2 : 7.5;
            }
            else {
                adjustments.floor =
                    (reference.floor == 1) ? -7 : -4;
            }
        }

        // Корректировка на площадь
        if (check_list.area) {
            adjustments.area = AREA_TABLE[
                findRange(analog.flat_area, AREA_RANGES)
            ][
                findRange(reference.flat_area, AREA_RANGES)
            ]
        }

        // Корректировка на площадь кухни
        if (check_list.kitchen_area) {
            adjustments.kitchen_area = KITCHEN_TABLE[
                findRange(analog.kitchen_area, KITCHEN_RANGES)
            ][
                findRange(reference.kitchen_area, KITCHEN_RANGES)
            ]
        }

        // Корректировка на наличие балкона/лоджии
        if (check_list.balcony) {
            if (analog.has_balcony && !reference.has_balcony) {
                adjustments.balcony = -5
            } else if (!analog.has_balcony && reference.has_balcony) {
                adjustments.balcony = 5.3
            }
        }

        // Корректировка на удаленность от метро
        if (check_list.metro) {
            adjustments.metro = METRO_TABLE[
                findRange(analog.metro_distance, METRO_RANGES)
            ][
                findRange(reference.metro_distance, METRO_RANGES)
            ]
        }

        // Корректировка на ремонт
        if (check_list.repairs && analog.state != reference.state) {
            switch (analog.state) {
                case HouseState.NO_DECORATION:
                    adjustments.repairs = 
                        (reference.state == HouseState.STATE_DECORATION) ?
                        13400 : 20100;
                    break
                case HouseState.STATE_DECORATION:
                    adjustments.repairs = 
                        (reference.state == HouseState.NO_DECORATION) ?
                        -1300 : 6700;
                    break
                case HouseState.MODERN_DECORATION:
                    adjustments.repairs = 
                        (reference.state == HouseState.NO_DECORATION) ?
                        -20100 : -6700;
                    break
            }
        }

        return adjustments
    }

    /**
     * Вычислить процент корректировки на ремонт с учетом цены аналога
     * @param analog объект квартиры-аналога, у которого берем цену
     */
    calcRepairs(analog) {
        let t = 1;
        t *= 1 + this.trade/100
        t *= 1 + this.area/100
        t *= 1 + this.metro/100
        t *= 1 + this.floor/100
        t *= 1 + this.kitchen_area/100
        t += 1 + this.balcony/100

        return this.repairs * analog.flat_area / (analog.price * t) * 100
    }

    /**
    * Вычислить общий размер корректировок в процентах
    * @param {*} analog объект квартиры-аналога, для которого вычисляем 
    * корректировки
    * @returns размер примененных корректировок в процентах
    */
    calcSize(analog) {
        return Math.abs(this.trade) +
            Math.abs(this.area) +
            Math.abs(this.metro) +
            Math.abs(this.floor) +
            Math.abs(this.kitchen_area) +
            Math.abs(this.balcony) +
            Math.abs(this.calcRepairs(analog));
    }

    /**
    * Метод применения корректировок к аналогу
    * @param {*} analog объект квартиры-аналога
    * @returns возвращает объект с полями корректировок, но вместо значений
    * указана полная цена квартиры с учетом данной корректировки
    */
    applyTo(analog) {
        let output = {};

        output.trade = analog.price * (1 + this.trade/100)
        output.area = output.trade * (1 + this.area/100)
        output.metro = output.area * (1 + this.metro/100)
        output.floor = output.metro * (1 + this.floor/100)
        output.kitchen_area = output.floor * (1 + this.kitchen_area/100)
        output.balcony = output.kitchen_area * (1 + this.balcony/100)
        output.repairs = output.balcony * (1 + this.calcRepairs(analog)/100)

        return output
    }
    
    /**
     * Метод вычисления весов каждого аналога
     * @param {*} analogs список аналогов
     * @param {*} adjustments список соответствующих им объектов корректировок
     * @returns список, где каждый элемент равен весу соответствующей квартиры
     */
    static calcWeights(analogs, adjustments) {
        let sizes = adjustments.map((adj, i) => {
            return adj.calcSize(analogs[i])
        })

        let t = sizes.reduce((prev, curr) => {
            return prev + 1/curr
        }, 0)

        return sizes.map((size) => 1/size/t)
    }
}
