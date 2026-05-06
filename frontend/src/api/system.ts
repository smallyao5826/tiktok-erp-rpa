import request from './request';

export const systemApi = {
  // Webhook 相关操作
  getWebhookList: () => request.get('/api/system/webhook/list'),
  addWebhook: (url: string) => request.post('/api/system/webhook/add', url),
  updateWebhook: (webhook_id: number, url?: string, enabled?: boolean) => request.post('/api/system/webhook/update', { webhook_id, url, enabled }),
  deleteWebhook: (webhook_id: number) => request.post('/api/system/webhook/delete', webhook_id),
  // 系统状态检查
  checkSystemStatus: () => request.get('/')
};
