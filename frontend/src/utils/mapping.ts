// 1. 站点名称映射
export const siteMap: Record<string, string> = {
  'BR': '巴西',
  'US': '美国',
  'JP': '日本',
  'RU': '俄罗斯',
  'ID': '印度尼西亚',
  'MY': '马来西亚',
  'TH': '泰国',
  'VN': '越南',
  'PH': '菲律宾',
  'SG': '新加坡',
  'GB': '英国',
  'DE': '德国',
  'FR': '法国',
  'IT': '意大利',
  'ES': '西班牙',
  'CA': '加拿大',
  'MX': '墨西哥'
};

// 2. 站点颜色映射 (基于国旗主色调)
export const siteColorMap: Record<string, string> = {
  'BR': '#059669', // 巴西绿
  'US': '#1e40af', // 美国蓝
  'JP': '#e11d48', // 日本红
  'RU': '#2563eb', // 俄罗蓝
  'ID': '#dc2626', // 印尼红
  'MY': '#1d4ed8', // 马来蓝
  'TH': '#2e10ff', // 泰国蓝
  'VN': '#facc15', // 越南金/红
  'PH': '#3b82f6', // 菲律宾蓝
  'SG': '#f43f5e', // 新加坡红
  'GB': '#1e3a8a', // 英国深蓝
  'DE': '#b45309', // 德国金/棕
  'FR': '#2563eb', // 法国蓝
  'IT': '#15803d', // 意大利绿
  'ES': '#ea580c', // 西班牙红/橙
  'CA': '#ef4444', // 加拿大红
  'MX': '#16a34a', // 墨西哥绿
};

// 获取名称：有映射显映射，无则显原代码
export const getSiteName = (code: string) => {
  if (!code) return '未知';
  return siteMap[code.toUpperCase()] || code.toUpperCase();
};

// 获取颜色：默认 slate-500
export const getSiteColor = (code: string) => {
  if (!code) return '#64748b';
  return siteColorMap[code.toUpperCase()] || '#64748b';
};