import http from 'k6/http';
import { check } from 'k6';
import { randomString } from 'https://jslib.k6.io/k6-utils/1.2.0/index.js';

export let options = {
    vus: 10,
    duration: '30s'
};

export default function () {
    const url = 'https://api.asfes.ru/v1/user/login';

    const headers = {
        'Content-Type': 'application/json',
    };

    const payload = JSON.stringify({
        login: `user_${randomString(8)}`,
        password: 'password123',
    });

    let res = http.post(url, payload, { headers: headers });

    check(res, {
        'status is 200 or 401': (r) => r.status === 200 || r.status === 401,
    });
}
