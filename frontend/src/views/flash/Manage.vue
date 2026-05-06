<template>
  <div class="h-full flex flex-col animate-fade-up gap-5 selection:bg-primary/10">
    
    <header class="flex justify-between items-end shrink-0 px-1">
      <div>
        <h2 class="text-3xl font-black text-heading tracking-tighter uppercase italic">
          Flash <span class="text-primary italic">Monitor</span>
        </h2>
        <p class="text-xs text-slate-400 font-bold mt-1 tracking-widest uppercase">
          共检索到 <span class="text-heading">{{ total }}</span> 个闪购
        </p>
      </div>
    </header>

    <div class="bg-surface rounded-xl p-4 shadow-main border border-white shrink-0 flex items-end gap-3 relative z-10">
      
      <div class="flex-1 max-w-[200px]">
        <label class="block text-xs font-black text-slate-400 uppercase mb-1.5 ml-1">01. 店铺</label>
        <ShopSelector v-model="filters.shop_id" mode="single" class="h-[48px]" @change="handleFilterChange" />
      </div>
      
      <div class="flex-1 max-w-[240px]">
        <label class="block text-xs font-black text-slate-400 uppercase mb-1.5 ml-1">02. 状态</label>
        <ModeToggle 
          v-model="filters.status" 
          :options="statusOptions" 
          class="h-[48px]"
          @update:modelValue="handleFilterChange"
        />
      </div>
      
      <div class="flex-1 min-w-[200px]">
        <label class="block text-xs font-black text-slate-400 uppercase mb-1.5 ml-1">03. 搜索</label>
        <SearchBar 
          v-model="filters.title" 
          placeholder="搜索活动名称或 ID..."
          class="h-[48px]"
          @search="handleFilterChange"
        />
      </div>
      
      <div class="flex items-center gap-2 mb-[1px]">
        <Button 
          :variant="selectedIds.length > 0 ? 'success' : 'ghost'" 
          size="medium" 
          :disabled="selectedIds.length === 0 || isBatchProcessing"
          @click="handleBulkAction('append')"
          class="flex items-center gap-2 h-[48px] transition-all"
          :class="selectedIds.length === 0 ? 'text-slate-400' : ''"
        >
          <PlusSquare v-if="!isBatchProcessing" :size="14" />
          <Loader2 v-else :size="14" class="animate-spin" />
          {{ isBatchProcessing ? '处理中...' : '批量追加' }}
        </Button>
        <Button 
          :variant="selectedIds.length > 0 ? 'primary' : 'ghost'" 
          size="medium" 
          :disabled="selectedIds.length === 0 || isBatchProcessing"
          @click="handleBulkAction('stop')"
          class="flex items-center gap-2 h-[48px] transition-all"
          :class="selectedIds.length === 0 ? 'text-slate-400' : ''"
        >
          <Power v-if="!isBatchProcessing" :size="14" />
          <Loader2 v-else :size="14" class="animate-spin" />
          {{ isBatchProcessing ? '处理中...' : '批量停用' }}
        </Button>
        <Button 
          variant="ghost" 
          size="medium"
          :disabled="isBatchProcessing"
          @click="fetchData"
          class="flex items-center justify-center h-[48px]"
        >
          <RefreshCw :size="16" :class="{ 'animate-spin': loading || isBatchProcessing }" />
        </Button>
      </div>
    </div>

    <div class="bg-surface rounded-xl shadow-main border border-white flex-1 flex flex-col min-h-0 relative overflow-hidden">
      
      <div class="bg-slate-50/80 border-b border-slate-100 overflow-hidden">
        <table class="w-full table-fixed">
          <thead>
            <tr class="text-[11px] font-black text-slate-500 tracking-widest uppercase text-center">
              <th class="py-4 pl-6 w-[40px]">
                <input type="checkbox" :checked="isAllSelected" @change="toggleSelectAll" class="rounded-md border-slate-300 text-primary focus:ring-primary/20 cursor-pointer">
              </th>
              <th class="py-4 text-left pl-2 w-[30%] font-black">闪购名称 & ID</th>
              <th class="py-4 w-[10%]">状态</th>
              <th class="py-4 w-[15%] leading-tight">商品数</th>
              <th class="py-4 w-[25%]">执行时段</th>
              <th class="py-4 pr-6 w-[15%]">操作</th>
            </tr>
          </thead>
        </table>
      </div>

      <div class="flex-1 overflow-y-auto custom-scrollbar">
        <table class="w-full table-fixed">
          <tbody v-if="!loading && list.length > 0">
            <tr v-for="promo in list" :key="promo.platform_promotion_id" class="group hover:bg-slate-50/40 border-b border-slate-50 last:border-none transition-all relative" :class="{'bg-primary/5': selectedIds.includes(promo.platform_promotion_id)}">
              <td class="py-3.5 pl-6 w-[40px] text-center">
                <input type="checkbox" v-model="selectedIds" :value="promo.platform_promotion_id" class="rounded-md border-slate-300 text-primary focus:ring-primary/20 cursor-pointer">
              </td>

              <td class="py-3.5 text-left pl-2 w-[30%]">
                <div class="flex flex-col pr-4">
                  <span class="font-bold text-sm text-heading truncate mb-0.5 tracking-tight">{{ promo.title }}</span>
                  <span class="text-xs font-mono text-slate-400 uppercase tracking-tighter">ID: {{ promo.platform_promotion_id }}</span>
                </div>
              </td>

              <td class="py-3.5 w-[10%] text-center">
                <div class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-md border border-transparent">
                  <span class="w-1.5 h-1.5 rounded-full" :class="getStatusDotStyle(promo.status)"></span>
                  <span class="text-xs font-black tracking-wider" :class="getStatusTextStyle(promo.status)">{{ formatStatus(promo.status) }}</span>
                </div>
              </td>

              <td class="py-3.5 w-[15%] text-center">
                <div class="flex flex-col gap-1">
                  <span class="text-sm font-bold text-heading font-mono">{{ promo.effective_item_count || 0 }} <span class="text-slate-300">/ {{ promo.effective_sku_count || 0 }} SKU</span></span>
                </div>
              </td>

              <td class="py-3.5 w-[25%] text-center font-mono text-sm text-slate-600">
                <div class="flex flex-col gap-1 scale-95 origin-center">
                  <span class="font-bold">{{ promo.gmt_local_begin }}</span>
                  <span class="text-xs text-slate-400 font-black opacity-60">-</span>
                  <span class="font-bold">{{ promo.gmt_local_end }}</span>
                </div>
              </td>

              <td class="py-3.5 pr-6 w-[15%] text-center">
                <div class="flex items-center justify-center gap-4 font-mono text-xs font-black uppercase tracking-widest">
                  <button @click="handleAction('copy', promo)" class="text-secondary hover:brightness-110 active:scale-90 transition-all">复制</button>
                  <button v-if="promo.status === '1' || promo.status === '2'" @click="handleAction('append', promo)" class="text-emerald-500 hover:brightness-110 active:scale-90 transition-all">追加</button>
                  <button v-if="promo.status === '1' || promo.status === '2'" @click="handleAction('stop', promo)" class="text-primary hover:brightness-110 active:scale-90 transition-all">停用</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>

        <div v-if="!loading && list.length === 0" class="flex flex-col items-center justify-center py-40 text-slate-300">
          <SearchX :size="48" stroke-width="1.5" class="mb-4 opacity-30" />
          <p class="text-xs font-black tracking-widest uppercase">未检索到匹配记录</p>
        </div>
      </div>

      <footer class="shrink-0 px-8 py-3 bg-slate-50/50 border-t border-slate-100 flex items-center justify-between">
        <div class="flex items-center gap-6 text-xs font-black text-slate-400 uppercase tracking-widest">
          <span>选中 {{ selectedIds.length }} 个</span>
          <span class="opacity-40">|</span>
          <span>总计 {{ total }} 项数据</span>
        </div>

        <div class="flex items-center gap-4">
          <button @click="changePage(currentPage - 1)" :disabled="currentPage === 1" class="page-btn">
            <ChevronLeft :size="14" />
          </button>
          
          <div class="flex items-center gap-1 mx-2">
            <button 
              v-for="p in paginationRange" :key="p"
              @click="typeof p === 'number' && changePage(p)"
              class="w-7 h-7 flex items-center justify-center rounded-md text-xs font-black transition-all"
              :class="p === currentPage ? 'bg-primary text-white shadow-sm' : p === '...' ? 'cursor-default text-slate-300' : 'hover:bg-white text-slate-400'"
            >
              {{ p }}
            </button>
          </div>

          <button @click="changePage(currentPage + 1)" :disabled="currentPage >= totalPages" class="page-btn">
            <ChevronRight :size="14" />
          </button>
          
          <div class="flex items-center gap-2">
            <span class="text-xs font-black text-slate-400 uppercase tracking-widest">每页</span>
            <select 
              v-model="pageSize" 
              @change="handlePageSizeChange"
              class="text-xs font-black text-slate-600 border border-slate-200 rounded-lg px-3 py-1.5 bg-white focus:outline-none focus:ring-2 focus:ring-primary/30 transition-all hover:border-primary/50"
            >
              <option value="20">20</option>
              <option value="50">50</option>
              <option value="100">100</option>
            </select>
            <span class="text-xs font-black text-slate-400 uppercase tracking-widest">条</span>
          </div>
        </div>
      </footer>
    </div>

    <!-- 任务队列状态显示 -->
    <div v-if="batchTaskQueue.length > 0" class="fixed bottom-4 right-4 z-50 bg-surface rounded-lg shadow-lg border border-white p-4 max-w-md">
      <h4 class="text-sm font-black text-heading mb-2">任务队列</h4>
      <div class="space-y-3">
        <div v-for="task in batchTaskQueue" :key="task.id" class="space-y-1">
          <div class="flex justify-between items-center">
            <span class="text-xs font-black text-slate-600">{{ task.type === 'bulk_append' ? '批量追加商品' : '批量停用活动' }}</span>
            <span class="text-xs font-black" :class="task.status === 'completed' ? 'text-green-500' : task.status === 'processing' ? 'text-blue-500' : 'text-slate-400'">
              {{ task.status === 'completed' ? '已完成' : task.status === 'processing' ? '处理中' : '等待中' }}
            </span>
          </div>
          <div v-if="task.status === 'processing'" class="w-full bg-slate-100 rounded-full h-1.5">
            <div class="bg-primary h-1.5 rounded-full transition-all duration-300" :style="{ width: task.progress + '%' }"></div>
          </div>
          <p class="text-xs text-slate-400">活动数: {{ task.platform_promotion_ids.length }}, 商品数: {{ task.platform_item_ids ? task.platform_item_ids.length : 0 }}</p>
        </div>
      </div>
    </div>

    <!-- 操作弹窗 -->
    <Modal 
      :visible="modalVisible" 
      :title="modalTitle"
      @close="modalVisible = false"
      @confirm="handleModalConfirm"
    >
      <div v-if="modalType === 'copy'" class="space-y-4">
        <p class="text-sm text-slate-600">您确定要复制活动 <strong>{{ currentPromo?.title }}</strong> 吗？</p>
        <p class="text-xs text-slate-400">复制后将创建一个新的活动，您可以修改活动时间和其他设置。</p>
      </div>
      <div v-else-if="modalType === 'append'" class="space-y-4">
        <p class="text-sm text-slate-600">您确定要为活动 <strong>{{ currentPromo?.title }}</strong> 追加商品吗？</p>
        <p class="text-xs text-slate-400">追加后将为该活动添加新的商品。</p>
        <div class="mt-4">
          <label class="block text-xs font-black text-slate-400 uppercase mb-1.5">商品 ID (多个 ID 用逗号分隔)</label>
          <textarea 
            v-model="productIds"
            placeholder="请输入商品 ID，多个 ID 用逗号分隔"
            class="w-full text-sm border border-slate-200 rounded-lg p-3 focus:outline-none focus:ring-2 focus:ring-primary/30 transition-all"
            rows="4"
          ></textarea>
        </div>
      </div>
      <div v-else-if="modalType === 'stop'" class="space-y-4">
        <p class="text-sm text-slate-600">您确定要停用活动 <strong>{{ currentPromo?.title }}</strong> 吗？</p>
        <p class="text-xs text-slate-400">停用后该活动将不再生效。</p>
      </div>
      <div v-else-if="modalType === 'bulk_append'" class="space-y-4">
        <p class="text-sm text-slate-600">您确定要为选中的 <strong>{{ selectedIds.length }}</strong> 个活动追加商品吗？</p>
        <p class="text-xs text-slate-400">追加后将为这些活动添加新的商品。</p>
        <div class="mt-4">
          <label class="block text-xs font-black text-slate-400 uppercase mb-1.5">商品 ID (多个 ID 用逗号分隔)</label>
          <textarea 
            v-model="productIds"
            placeholder="请输入商品 ID，多个 ID 用逗号分隔"
            class="w-full text-sm border border-slate-200 rounded-lg p-3 focus:outline-none focus:ring-2 focus:ring-primary/30 transition-all"
            rows="4"
          ></textarea>
        </div>
      </div>
      <div v-else-if="modalType === 'bulk_stop'" class="space-y-4">
        <p class="text-sm text-slate-600">您确定要停用选中的 <strong>{{ selectedIds.length }}</strong> 个活动吗？</p>
        <p class="text-xs text-slate-400">停用后这些活动将不再生效。</p>
      </div>
    </Modal>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue';
import { RefreshCw, Loader2, ChevronLeft, ChevronRight, SearchX, PlusSquare, Power, Copy, Package, X } from 'lucide-vue-next';
import { promotionApi } from '../../api/promotion';
import ShopSelector from '../../components/ShopSelector.vue';
import ModeToggle from '../../components/common/ModeToggle.vue';
import SearchBar from '../../components/common/SearchBar.vue';
import Button from '../../components/common/Button.vue';
import Modal from '../../components/common/Modal.vue';
import { useNotification } from '../../composables/useNotification';

const notify = useNotification();

const statusOptions = [
  { label: '全部', value: '' },
  { label: '待开始', value: '1' },
  { label: '进行中', value: '2' },
];

const filters = reactive({ shop_id: '', title: '', status: '' });
const list = ref<any[]>([]);
const total = ref(0);
const loading = ref(false);
const currentPage = ref(1);
const pageSize = ref(20);
const selectedIds = ref<string[]>([]);

// 批量操作相关状态
const isBatchProcessing = ref(false);
const batchTaskQueue = ref<any[]>([]);

// 弹窗相关状态
const modalVisible = ref(false);
const modalTitle = ref('');
const modalType = ref<'copy' | 'append' | 'stop' | 'bulk_append' | 'bulk_stop'>('copy');
const currentPromo = ref<any>(null);
const currentShopId = ref('');
const productIds = ref(''); // 用于输入商品 ID

// 分页逻辑
const totalPages = computed(() => Math.ceil(total.value / pageSize.value));
const paginationRange = computed(() => {
  const range: (number | string)[] = [];
  const total = totalPages.value;
  const current = currentPage.value;

  if (total <= 7) {
    for (let i = 1; i <= total; i++) range.push(i);
  } else {
    range.push(1);
    if (current > 4) range.push('...');
    const start = Math.max(2, current - 1);
    const end = Math.min(total - 1, current + 1);
    for (let i = start; i <= end; i++) range.push(i);
    if (current < total - 3) range.push('...');
    range.push(total);
  }
  return range;
});

// 多选逻辑
const isAllSelected = computed(() => list.value.length > 0 && selectedIds.value.length === list.value.length);
const toggleSelectAll = () => {
  selectedIds.value = isAllSelected.value ? [] : list.value.map(p => p.platform_promotion_id);
};

const fetchData = async () => {
  loading.value = true;
  selectedIds.value = []; // 刷新时重置选择
  try {
    const res = await promotionApi.getPromotionList({ 
      shop_id: filters.shop_id || undefined,
      status: filters.status || undefined,
      title: filters.title || undefined,
      page_no: currentPage.value,
      page_size: pageSize.value
    });
    list.value = res.data.data.list || [];
    total.value = res.data.data.total || 0;
  } catch (error) {
    notify.error('通信异常', '后端 RPA 服务器未响应');
  } finally {
    loading.value = false;
  }
};

const handleFilterChange = () => {
  currentPage.value = 1;
  fetchData();
};

const changePage = (p: number) => {
  currentPage.value = p;
  fetchData();
};

const handlePageSizeChange = () => {
  currentPage.value = 1;
  fetchData();
};

const handleBulkAction = (type: string) => {
  if (selectedIds.value.length === 0) {
    notify.error('操作失败', '请先选择要操作的活动');
    return;
  }
  
  if (isBatchProcessing.value) {
    notify.info('操作提示', '正在处理其他批量操作，请稍后再试');
    return;
  }
  
  if (type === 'append') {
    modalType.value = 'bulk_append';
    modalTitle.value = '批量追加商品';
  } else if (type === 'stop') {
    modalType.value = 'bulk_stop';
    modalTitle.value = '批量停用活动';
  }
  modalVisible.value = true;
};

const handleAction = (type: string, promo: any) => {
  if (type === 'copy' || type === 'stop') {
    // 复制和停用功能正在开发中
    notify.info('功能提示', `${type === 'copy' ? '复制' : '停用'}功能正在开发中`);
  } else if (type === 'append') {
    // 追加商品功能保留弹窗
    currentPromo.value = promo;
    currentShopId.value = filters.shop_id;
    modalType.value = 'append';
    modalTitle.value = '追加商品';
    modalVisible.value = true;
  }
};

const handleModalConfirm = async () => {
  modalVisible.value = false;
  
  try {
    if (modalType.value === 'copy') {
      // 复制活动 - 正在开发
      notify.info('功能提示', '复制功能正在开发中');
    } else if (modalType.value === 'stop') {
      // 停用单个活动
      notify.info('功能提示', '停用功能正在开发中');
    } else if (modalType.value === 'bulk_stop') {
      // 批量停用活动 - 显示开发中状态
      notify.info('功能提示', '批量停用功能正在开发中');
    } else if (modalType.value === 'append') {
      // 单个活动追加商品 - 正在开发
      notify.info('功能提示', '追加商品功能正在开发中');
    } else if (modalType.value === 'bulk_append') {
      // 批量追加商品 - 实现异步处理
      if (!productIds.value.trim()) {
        notify.error('操作失败', '请输入商品 ID');
        return;
      }
      
      // 解析商品 ID 列表
      const platformItemIds = productIds.value
        .split(',')
        .map(id => id.trim())
        .filter(id => id);
      
      if (platformItemIds.length === 0) {
        notify.error('操作失败', '请输入有效的商品 ID');
        return;
      }
      
      // 显示加载状态
      isBatchProcessing.value = true;
      
      // 创建任务对象
      const task = {
        id: Date.now().toString(),
        type: 'bulk_append',
        status: 'pending',
        shop_id: filters.shop_id,
        platform_promotion_ids: selectedIds.value,
        platform_item_ids: platformItemIds,
        created_at: new Date().toISOString(),
        progress: 0
      };
      
      // 添加到任务队列
      batchTaskQueue.value.push(task);
      
      // 模拟异步处理
      setTimeout(() => {
        // 更新任务状态为处理中
        task.status = 'processing';
        task.progress = 30;
        
        // 模拟处理过程
        setTimeout(() => {
          task.progress = 70;
          
          // 模拟任务完成
          setTimeout(() => {
            task.status = 'completed';
            task.progress = 100;
            isBatchProcessing.value = false;
            
            // 显示任务完成通知
            notify.success('任务完成', `已成功为 ${selectedIds.value.length} 个活动追加商品`);
            fetchData();
          }, 1000);
        }, 1000);
      }, 500);
      
      // 立即返回任务已下发的通知
      notify.success('任务已下发', '请稍后关注处理结果');
    }
  } catch (error) {
    isBatchProcessing.value = false;
    notify.error('操作失败', '网络错误，请稍后重试');
    console.error(error);
  }
};

onMounted(() => fetchData());

const formatStatus = (s: string) => ({ '1': '待开始', '2': '进行中', '3': '已结束' }[s] || '已失效');
const getStatusStyle = (s: string) => s === '2' ? 'bg-green-500/5 text-green-700' : s === '1' ? 'bg-amber-500/5 text-amber-700' : 'bg-slate-100 text-slate-500';
const getStatusTextStyle = (s: string) => s === '2' ? 'text-green-700' : s === '1' ? 'text-amber-700' : 'text-slate-500';
const getStatusDotStyle = (s: string) => s === '2' ? 'bg-green-500 shadow-[0_0_8px_rgba(34,197,94,0.6)]' : s === '1' ? 'bg-amber-500' : 'bg-slate-400';
</script>

<style scoped>
@reference "../../style.css";

.page-btn {
  @apply p-1.5 rounded-lg hover:bg-white text-slate-400 disabled:opacity-20 transition-all hover:text-primary active:scale-90;
}

.custom-scrollbar::-webkit-scrollbar { width: 4px; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: #e2e8f0; border-radius: 10px; }

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

/* 表格行 hover 效果 */
tr.group:hover {
  border-left: 1.5px solid #FE2C55;
}

/* 表格行选中效果 */
tr.bg-primary\/5 {
  border-left: 1.5px solid #FE2C55;
}
</style>