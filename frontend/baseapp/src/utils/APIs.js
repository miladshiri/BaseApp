export const loginAPI = async (username, password) => {
    const res = await fetch('http://127.0.0.1:8000/user/token/', {
        method: 'post',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify({
            "username": username,
            "password": password
        }),
    })
    return res
}

export const registerAPI = async (firstname, lastname, email, password, passwordConfirm) => {
    const res = await fetch('http://127.0.0.1:8000/user/register/', {
        method: 'post',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify({
            "username": email,
            "password": password,
            "password2": passwordConfirm,
            "email": email,
            "first_name": firstname,
            "last_name": lastname
        }),
    })
    return res
}

export const verifyTokenAPI = async (userAccessToken) => {
    const res = await fetch('http://127.0.0.1:8000/user/token/verify/', {
        method: 'post',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify({
            "token": userAccessToken
        }),
    })
    return res
}


export const requestAPI = async(channelUrl, userAccessToken=null) => {
    const headers = {
        'Content-Type':'application/json',
    }
    if (userAccessToken && userAccessToken != '') {
        headers['Authorization'] = `Bearer ${userAccessToken}`
    }
    const res = await fetch('http://127.0.0.1:8000/report/request', {
        method: 'post',
        headers: headers,
        body: JSON.stringify({
            "url": channelUrl
        }),
    })
    return res
}

export const reportAPI = async(reportID) => {
    const res = await fetch(`http://127.0.0.1:8000/report/detail/${reportID}`)
    return res
}