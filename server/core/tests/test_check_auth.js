import http from 'k6/http';
import { check } from 'k6';
import { randomString } from 'https://jslib.k6.io/k6-utils/1.2.0/index.js';

export let options = {
    vus: 10,
    duration: '30s',
};

export default function () {
    const url = 'https://api.asfes.ru/v1/user/check_auth';

    const headers = {
        'Content-Type': 'application/json',
        'Cookie': `token=${randomString(8)}`,
    };

    let res = http.get(url, { headers: headers });

    check(res, {
        'status is 200 or 403': (r) => r.status === 200 || r.status === 403,
    });
}
