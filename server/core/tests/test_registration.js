import http from 'k6/http';
import { check } from 'k6';
import { randomString } from 'https://jslib.k6.io/k6-utils/1.2.0/index.js';

export let options = {
    vus: 10,
    duration: '30s',
};

export default function () {
    const url = 'https://api.asfes.ru/v1/user/registration';

    const headers = {
        'Content-Type': 'application/json',
        'Cookie': `token=${randomString(8)}`,
    };

    const payload = JSON.stringify({
        login: `user_${randomString(8)}`,
        mail: `${uniqueLogin}@example.com`,
        phone: '+1234567890',
        password: 'password123',
        repetition_password: 'password123',
    });

    let res = http.post(url, payload, { headers: headers });

    check(res, {
        'status is 201': (r) => r.status === 201,
    });
}
