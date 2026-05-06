import request from './request';

export const productApi = {
  // 获取商品列表/搜索特定商品
  list: (data: { 
    shop_ids: string[], 
    status: string, 
    platform_item_id?: string, 
    page_no: number, 
    page_size: number 
  }) => request.post('/api/product/list', data),

  getOnsaleCount: (shop_id: string) => request.get(`/api/product/onsale-count?shop_id=${shop_id}`)
};