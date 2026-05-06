import request from './request';

export const orderApi = {
  // 获取仓库订单汇总
  getWarehouseSummary: (data: {
    shop_ids: string[];
    start_time: string;
    end_time: string;
    warehouse: string;
    seller_sku: string;
  }, config?: any) => request.post('/api/order/warehouse-summary', data, config)
};
