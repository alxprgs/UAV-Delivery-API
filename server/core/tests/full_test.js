import http from 'k6/http';
import { check } from 'k6';
import { randomString } from 'https://jslib.k6.io/k6-utils/1.2.0/index.js';

export let options = { vus: 10, duration: '30s' };

export default function () {
    const jar = http.cookieJar();
    const login = `user_${randomString(8)}`, mail = `${login}@test.com`;
    let res = http.post('https://api.asfes.ru/v1/user/registration', JSON.stringify({ login, mail, phone: '+79569689556', password: 'zxc1245351981', repetition_password: 'zxc1245351981' }), { headers: { 'Content-Type': 'application/json' } });
    check(res, { 'reg 201/409': (r) => r.status === 201 || r.status === 409 });

    res = http.post('https://api.asfes.ru/v1/user/login', JSON.stringify({ login, password: 'zxc1245351981' }), { headers: {'Content-Type': 'application/json', 'Cookie': `token=${randomString(8)}`} });
    check(res, { 'login 200/401': (r) => r.status === 200 || r.status === 401 });

    res = http.patch('https://api.asfes.ru/v1/user/set_permissions', JSON.stringify({ login, permission: 'all', value: true }), { headers: {'Content-Type': 'application/json', 'Cookie': `token=${randomString(8)}`} });
    check(res, { 'set_perm 200/403/404': (r) => [200,403,404].includes(r.status) });

    res = http.get('https://api.asfes.ru/v1/user/check_auth', { headers: {'Content-Type': 'application/json', 'Cookie': `token=${randomString(8)}`} });
    check(res, { 'auth check': (r) => [true, false].includes(r.json()) });

    res = http.get('https://api.asfes.ru/v1/user/check_permissions?permission=all', { headers: {'Content-Type': 'application/json', 'Cookie': `token=${randomString(8)}`} });
    check(res, { 'perm check': (r) => [true, false].includes(r.json()) });
}
