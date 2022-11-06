ymaps.ready(init);
function init(){
    var myMap = new ymaps.Map("map", {
        center: [55.76, 37.64],
        zoom: 12
    });
    var placemark = new ymaps.Placemark([55.755804, 37.614608], {
        hintContent: 'Запомните все!',
        balloonContent: 'Здесь охотный ряд!'
    });
    myMap.geoObjects.add(placemark);
}