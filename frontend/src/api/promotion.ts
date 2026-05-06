import request from './request';

export const promotionApi = {
  // --- 1. 促销活动核心 ---
  createFlashSale: (data: any) => request.post('/api/promotion/flash-sale/create', data),
  addUpdateProducts: (data: any) => request.post('/api/promotion/product/add-update', data),
  copyPromotion: (data: any) => request.post('/api/promotion/copy', data),
  deactivatePromotions: (data: any) => request.post('/api/promotion/deactivate', data),
  appendProducts: (data: any) => request.post('/api/promotion/append', data),
  getPromotionList: (params: { 
    shop_id: string, 
    status?: string, 
    title?: string, 
    page_no?: number, 
    page_size?: number 
  }) => request.get('/api/promotion/list', { params }),

  // --- 2. 定价策略 (Strategy) ---
  getStrategies: (shop_id: string, keyword: string = '') => request.get(`/api/promotion/strategy/list?shop_id=${shop_id}&keyword=${encodeURIComponent(keyword)}`),
  saveStrategy: (data: any) => request.post('/api/promotion/strategy/save', data),
  deleteStrategy: (strategy_id: number) => request.delete(`/api/promotion/strategy/delete?strategy_id=${strategy_id}`),

  // --- 3. SKU 覆盖 (Override) ---
  searchSkus: (shop_id: string, platform_item_id: string) => 
    request.get(`/api/promotion/sku/search?shop_id=${shop_id}&platform_item_id=${platform_item_id}`),
  saveSkuOverride: (data: any) => request.post('/api/promotion/sku-override/save', data),
  getSkuOverrides: (shop_id: string) => request.get(`/api/promotion/sku-override/list?shop_id=${shop_id}`)
};