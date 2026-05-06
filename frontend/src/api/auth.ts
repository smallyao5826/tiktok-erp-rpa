import request from './request';

export const authApi = {
  login: (data: any) => request.post('/api/auth/login', data),
  getCookie: () => request.get('/api/auth/cookie'),
  getAccountInfo: () => request.get('/api/auth/account/info')
};