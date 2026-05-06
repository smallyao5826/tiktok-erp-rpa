<template>
  <div class="h-full flex flex-col animate-fade-up gap-5 selection:bg-primary/10">
    
    <header class="flex justify-between items-end shrink-0 px-1">
      <div>
        <h2 class="text-3xl font-black text-heading tracking-tighter uppercase italic">
          Pre <span class="text-primary italic">Launch</span>
        </h2>
        <p class="text-xs text-slate-400 font-bold mt-1 tracking-widest uppercase">
          预上线仓库统计
        </p>
      </div>
    </header>

    <div class="bg-surface rounded-xl p-6 shadow-main border border-white shrink-0 relative z-10">
      <h3 class="text-lg font-black text-heading mb-6">筛选条件</h3>
      
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div>
          <label class="block text-xs font-black text-slate-400 uppercase mb-1.5">01. 店铺</label>
          <ShopSelector v-model="formData.shop_ids" mode="multiple" class="h-[48px]" />
        </div>
        <div>
          <label class="block text-xs font-black text-slate-400 uppercase mb-1.5">02. 开始时间</label>
          <DatePicker v-model="formData.start_time" />
        </div>
        <div>
          <label class="block text-xs font-black text-slate-400 uppercase mb-1.5">03. 结束时间</label>
          <DatePicker v-model="formData.end_time" />
        </div>
        <div class="flex items-end">
          <Button 
            variant="primary" 
            size="medium" 
            @click="fetchData"
            :loading="loading"
            class="h-[48px] w-full"
          >
            查询
          </Button>
        </div>
      </div>
      
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
        <div>
          <label class="block text-xs font-black text-slate-400 uppercase mb-1.5">04. 仓库</label>
          <Select 
            v-model="formData.warehouse" 
            :options="warehouseOptions"
            placeholder="选择仓库"
            :disabled="!hasData"
          />
        </div>
        <div>
          <label class="block text-xs font-black text-slate-400 uppercase mb-1.5">05. Seller SKU</label>
          <Select 
            v-model="formData.seller_sku" 
            :options="sellerSkuOptions"
            placeholder="选择 Seller SKU"
            :disabled="!hasData"
          />
        </div>
      </div>
    </div>

    <div class="bg-surface rounded-xl shadow-main border border-white flex-1 flex flex-col min-h-0 relative overflow-hidden">
      <div class="bg-slate-50/80 border-b border-slate-100 overflow-hidden">
        <table class="w-full table-fixed">
          <thead>
            <tr class="text-[11px] font-black text-slate-500 tracking-widest uppercase text-center">
              <th class="py-4 w-[60px]">
                <input 
                  type="checkbox" 
                  v-model="selectAll" 
                  @change="toggleSelectAll"
                />
              </th>
              <th class="py-4 w-[50%]">仓库</th>
              <th class="py-4 w-[50%]">订单数</th>
            </tr>
          </thead>
        </table>
      </div>

      <div class="flex-1 overflow-y-auto custom-scrollbar">
        <table class="w-full table-fixed">
          <tbody v-if="summaryData.warehouse_counts && summaryData.warehouse_counts.length > 0">
            <tr v-for="item in summaryData.warehouse_counts" :key="item.warehouse" class="group hover:bg-slate-50/40 border-b border-slate-50 last:border-none transition-all relative">
              <td class="py-3.5 text-center w-[60px]">
                <input 
                  type="checkbox" 
                  :checked="selectedWarehouses.includes(item.warehouse)"
                  @change="toggleWarehouse(item.warehouse)"
                />
              </td>
              <td class="py-3.5 text-center w-[50%]">
                <span class="font-bold text-sm text-heading">{{ item.warehouse }}</span>
              </td>
              <td class="py-3.5 text-center w-[50%]">
                <span class="text-sm font-black">{{ item.count }}</span>
              </td>
            </tr>
          </tbody>
          <tbody v-else>
            <tr>
              <td colspan="3" class="py-20 text-center text-slate-300">
                <p class="text-xs font-black tracking-widest uppercase">未检索到数据</p>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="bg-surface rounded-xl p-6 shadow-main border border-white shrink-0 relative z-10">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="bg-slate-50 rounded-lg p-4 border border-slate-100">
          <p class="text-xs text-slate-400 font-black uppercase tracking-widest mb-1">总订单数</p>
          <p class="text-2xl font-black text-heading">{{ selectedTotalOrders || 0 }}</p>
        </div>
        <div class="bg-slate-50 rounded-lg p-4 border border-slate-100">
          <p class="text-xs text-slate-400 font-black uppercase tracking-widest mb-1">仓库总数</p>
          <p class="text-2xl font-black text-heading">{{ selectedWarehouseCount || 0 }}</p>
        </div>
        <div class="bg-slate-50 rounded-lg p-4 border border-slate-100">
          <p class="text-xs text-slate-400 font-black uppercase tracking-widest mb-1">数据日期</p>
          <p class="text-2xl font-black text-heading">{{ formattedDate }}</p>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import ShopSelector from '../../components/ShopSelector.vue';
import Button from '../../components/common/Button.vue';
import Select from '../../components/common/Select.vue';
import DatePicker from '../../components/DatePicker.vue';
import { useNotification } from '../../composables/useNotification';
import { orderApi } from '../../api/order';

const notify = useNotification();

// 表单数据
const formData = ref({
  shop_ids: [] as string[],
  start_time: '',
  end_time: '',
  warehouse: '',
  seller_sku: ''
});

// 加载状态
const loading = ref(false);

// 汇总数据
const summaryData = ref({
  total_orders: 0,
  warehouse_count: 0,
  warehouse_counts: [] as Array<{ warehouse: string; count: number; percentage: number }>
});

// 选中的仓库
const selectedWarehouses = ref([] as string[]);
const selectAll = ref(false);

// 选项数据
const warehouseOptions = ref([] as Array<{ value: string; label: string }>);
const sellerSkuOptions = ref([] as Array<{ value: string; label: string }>);

// 计算属性
const hasData = computed(() => summaryData.value.warehouse_counts.length > 0);
const formattedDate = computed(() => {
  const now = new Date();
  return now.toLocaleDateString('zh-CN');
});

// 计算选中仓库的总订单数
const selectedTotalOrders = computed(() => {
  return summaryData.value.warehouse_counts
    .filter(item => selectedWarehouses.value.includes(item.warehouse))
    .reduce((total, item) => total + item.count, 0);
});

// 计算选中仓库的数量
const selectedWarehouseCount = computed(() => {
  return selectedWarehouses.value.length;
});

// 切换仓库选中状态
const toggleWarehouse = (warehouse: string) => {
  const index = selectedWarehouses.value.indexOf(warehouse);
  if (index > -1) {
    selectedWarehouses.value.splice(index, 1);
  } else {
    selectedWarehouses.value.push(warehouse);
  }
  // 更新全选状态
  updateSelectAllStatus();
};

// 切换全选状态
const toggleSelectAll = () => {
  if (selectAll.value) {
    // 全选
    selectedWarehouses.value = summaryData.value.warehouse_counts.map(item => item.warehouse);
  } else {
    // 取消全选
    selectedWarehouses.value = [];
  }
};

// 更新全选状态
const updateSelectAllStatus = () => {
  selectAll.value = selectedWarehouses.value.length === summaryData.value.warehouse_counts.length && summaryData.value.warehouse_counts.length > 0;
};

// 获取数据
const fetchData = async () => {
  loading.value = true;
  try {
    const res = await orderApi.getWarehouseSummary({
      shop_ids: formData.value.shop_ids,
      start_time: formData.value.start_time,
      end_time: formData.value.end_time,
      warehouse: formData.value.warehouse,
      seller_sku: formData.value.seller_sku
    });
    
    if (res.data.code === 200) {
      const backendData = res.data.data;
      
      // 转换后端数据结构为前端期望的格式
      const warehouseCounts = Object.entries(backendData.stats).map(([warehouse, count]) => ({
        warehouse,
        count: Number(count),
        percentage: 0 // 不再需要计算占比
      }));
      
      summaryData.value = {
        total_orders: backendData.total_orders,
        warehouse_count: backendData.total_warehouses,
        warehouse_counts: warehouseCounts
      };
      
      // 提取仓库选项
      warehouseOptions.value = warehouseCounts.map(item => ({
        value: item.warehouse,
        label: item.warehouse
      }));
      
      // 提取seller_sku选项
      if (backendData.seller_skus) {
        sellerSkuOptions.value = backendData.seller_skus.map((sku: string) => ({
          value: sku,
          label: sku
        }));
      } else {
        sellerSkuOptions.value = [];
      }
      
      // 默认全选所有仓库
      selectedWarehouses.value = summaryData.value.warehouse_counts.map(item => item.warehouse);
      selectAll.value = true;
    } else {
      notify.error('操作失败', res.data.msg || '获取数据失败');
    }
  } catch (error) {
    if (error.code === 'ECONNABORTED') {
      notify.error('请求超时', '后端处理时间过长，请稍后再试');
    } else {
      notify.error('通信异常', '获取数据失败');
    }
  } finally {
    loading.value = false;
  }
};

// 初始加载
onMounted(() => {
  // 可以在这里添加默认数据加载逻辑
});
</script>

<style scoped>
/* 自定义复选框样式 */
input[type="checkbox"] {
  width: 16px;
  height: 16px;
  border: 2px solid #e2e8f0;
  border-radius: 4px;
  outline: none;
  cursor: pointer;
  transition: all 0.2s ease;
  appearance: none;
  -webkit-appearance: none;
  position: relative;
}

input[type="checkbox"]:checked {
  background-color: #FE2C55;
  border-color: #FE2C55;
}

input[type="checkbox"]:checked::after {
  content: '✓';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: white;
  font-size: 12px;
  font-weight: bold;
}

input[type="checkbox"]:hover {
  border-color: #FE2C55;
}

input[type="checkbox"]:focus {
  box-shadow: 0 0 0 2px rgba(254, 44, 85, 0.2);
}
</style>
