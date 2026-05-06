import axios from 'axios';

const request = axios.create({
  baseURL: 'http://127.0.0.1:5000', // 统一改为 5000 端口
  timeout: 30000, // 增加超时时间到30秒，适应后端15秒左右的处理时间
});

// 你可以在这里添加响应拦截器处理 401 自动跳转登录
request.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default request;