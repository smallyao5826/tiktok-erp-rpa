import request from './request';

export const shopApi = {
  getShops: () => request.get('/api/shop/list'),
  getShopDetail: (shopId: string) => request.get(`/api/shop/info?shop_id=${shopId}`)
};