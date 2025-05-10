import http from 'k6/http';
import { check } from 'k6';
import { randomString } from 'https://jslib.k6.io/k6-utils/1.2.0/index.js';

export let options = {
    vus: 10,
    duration: '30s',
};

export default function () {
    const url = 'https://api.asfes.ru/v1/user/set_permissions';

    const headers = {
        'Content-Type': 'application/json',
        'Cookie': `token=${randomString(8)}`,
    };

    const payload = JSON.stringify({
        login: 'targetuser',
        permission: 'set_permissions',
        value: true,
    });

    let res = http.patch(url, payload, { headers: headers });

    check(res, { 'status is 200 or 403': (r) => r.status === 200 || r.status === 403 });
    check(res, {
            'status is 200, 403 or 404': (r) =>
            r.status === 200 || r.status === 403 || r.status === 404,
        });
}
