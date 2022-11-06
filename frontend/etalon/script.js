
document.addEventListener('DOMContentLoaded', () => {
    let references = JSON.parse(sessionStorage.getItem('references'))
    
    let etalons = document.querySelector('#etalons')

    let html = ''

    for (let i = 0; i < references.length; i++) {
        let ref_house = references[i]
        
        html += '<p><input name="model" type="radio" value="' + i + '">'
        html += ref_house.location + ' (' + ref_house.floor + ' этаж из ' + ref_house.floors_count + ')'
        html += '</input></p>'

        etalons.innerHTML = html + etalons.innerHTML
    }

    document.querySelector('#select-btn').addEventListener('click', (ev) => {
        let index = document.querySelector('input[type=radio]:checked').value

        sessionStorage.setItem('curr_ref', JSON.stringify(references[index]))

        window.location.href = '/correction'
        ev.preventDefault()
    })
})
