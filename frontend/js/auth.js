
/**
 * Метод для попытки авторизации на сервере
 * @param {*} login логин для авторизации
 * @param {*} password пароль
 * @returns промис с событием авторизации
 */
export function tryToLogin(login, password) {
    return new Promise((resolve, reject) => {
        let url = '/api/auth/get_token?login='
        url += encodeURIComponent(login)
        url += '&password=' + encodeURIComponent(password)

        fetch(url)
            .then((response) => {
                return response.json()
            })
            .then((json) => {
                if (json.error) {
                    console.log('Error while logging in: \n', json)
                    reject()
                }
                else {
                    sessionStorage.setItem('auth_token', json.token)
                    resolve()
                }
            })
            .catch((reason) => {
                console.log('Error while logging in: \n', reason)
                reject()
            })
    })
}

/**
 * Метод проверки авторизации текущего пользователя
 * @returns булевое значения состояния авторизации
 */
export function checkAuthorization() {
    try {
        let jwt = parseJwt(sessionStorage.getItem('auth_token'))
        if (Date.now() / 1000 < jwt.exp) {
            return true
        }
    }
    catch { }
    return false
}

/**
 * Метод получения текущего токена авторизации
 */
export function getToken() {
    return sessionStorage.getItem('auth_token')
}

/**
 * Метод парсинга JWT токена
 * @param {*} token JWT токен
 * @returns JSON объект, хранящийся в токене
 */
export function parseJwt(token) {
    var base64Url = token.split('.')[1];
    var base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    var jsonPayload = decodeURIComponent(window.atob(base64).split('').map(function(c) {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));

    return JSON.parse(jsonPayload);
}
