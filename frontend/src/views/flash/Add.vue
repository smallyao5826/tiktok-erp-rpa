<template>
  <div class="animate-fade-up">
    <header class="mb-10 px-1">
      <h2 class="text-3xl font-black text-heading tracking-tight italic uppercase">
        Flash <span class="text-primary italic">Creator</span>
      </h2>
      <p class="text-xs text-slate-400 font-bold mt-1 tracking-widest uppercase">
        添加闪购自动化任务 · 请确保已在价格策略中配置好对应的定价规则
      </p>
    </header>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8 items-stretch">
      <div class="lg:col-span-2">
        <div class="bg-surface p-10 rounded-xl shadow-main border border-white h-full space-y-8">
          
          <section class="space-y-4">
            <label class="block text-xs font-black text-slate-400 uppercase mb-1.5 ml-1">01. 目标执行店铺</label>
            <ShopSelector v-model="form.shop_id" mode="single" @change="handleShopChange" />
          </section>

          <section class="space-y-4">
            <label class="block text-xs font-black text-slate-400 uppercase mb-1.5 ml-1">02. 执行日期</label>
            <DatePicker v-model="selectedDate" />
          </section>

          <section class="space-y-4">
            <div class="flex justify-between items-end px-1">
              <div class="space-y-1">
                <label class="block text-xs font-black text-slate-400 uppercase mb-1.5 ml-1">03. 选择执行时段</label>
              </div>
              <button 
                @click="toggleAllSlots" 
                class="text-xs font-black uppercase px-4 py-2 rounded-md transition-all active:scale-95"
                :class="isAllSelected ? 'bg-primary text-white shadow-lg shadow-primary/20' : 'bg-slate-100 text-slate-500 hover:bg-slate-200'"
              >
                {{ isAllSelected ? '取消全选' : '全选所有' }}
              </button>
            </div>
            
            <div class="grid grid-cols-3 md:grid-cols-4 gap-3">
              <button 
                v-for="h in 24" :key="h"
                @click="toggleSlot(h - 1)"
                class="py-4 rounded-lg border text-sm font-mono font-bold transition-all active:scale-95"
                :class="isSlotSelected(h - 1) 
                  ? 'bg-primary text-white border-primary shadow-active' 
                  : 'bg-slate-50 text-slate-500 border-transparent hover:border-slate-200'"
              >
                {{ formatTimeRange(h - 1) }}
              </button>
            </div>
          </section>
        </div>
      </div>

      <div class="flex flex-col gap-6">
        <div class="bg-surface p-8 rounded-xl shadow-main border border-white flex flex-col flex-1 min-h-[600px]">
          <label class="text-xs font-black text-slate-400 uppercase tracking-[0.2em] block mb-6 px-1">04. 商品范围选择</label>

          <ModeToggle 
            v-model="productMode" 
            :options="[{label: '全部商品', value: 'all'}, {label: '部分商品', value: 'partial'}]" 
            class="mb-8"
          />

          <div class="flex-1 flex flex-col min-h-0 relative">
            
            <div v-if="productMode === 'all'" class="flex-1 flex flex-col items-center justify-center text-center space-y-6 animate-fade-in">
              <div class="relative">
                <div class="w-24 h-24 bg-primary/5 rounded-xl flex items-center justify-center text-primary shadow-inner">
                  <Package :size="40" :class="{ 'animate-pulse': isCountLoading }" />
                </div>
                <button 
                  v-if="form.shop_id"
                  @click="fetchOnsaleCount" 
                  class="absolute -bottom-1 -right-1 p-2 bg-white rounded-full shadow-subtle text-slate-400 hover:text-primary active:rotate-180 transition-all duration-500"
                >
                  <RefreshCw :size="14" :class="{ 'animate-spin': isCountLoading }" />
                </button>
              </div>

              <div v-if="form.shop_id" class="space-y-1">
                <p class="text-xs font-black text-slate-400 uppercase tracking-widest">当前店铺在售总量</p>
                <div class="flex items-baseline justify-center gap-1">
                  <p class="text-5xl font-black text-heading tracking-tighter">{{ onsaleCount }}</p>
                  <span class="text-sm font-bold text-slate-300 italic">件</span>
                </div>
              </div>
              <p v-else class="text-base text-slate-400 italic px-10 leading-relaxed font-medium text-slate-300">请先在左侧选择店铺</p>
            </div>

            <div v-else class="flex-1 flex flex-col animate-fade-in min-h-0">
              <SearchBar 
                v-model="searchId" 
                :loading="isSearching" 
                placeholder="输入商品ID（支持逗号分隔）" 
                @search="executeProductSearch"
                class="mb-8"
              />

              <div class="flex-1 overflow-y-auto custom-scrollbar space-y-4 pr-2">
                <transition-group name="list">
                  <div v-for="item in selectedProducts" :key="item.platform_item_id" 
                    class="p-3 bg-white border border-slate-100 rounded-lg flex items-center gap-4 shadow-subtle"
                  >
                    <div class="w-14 h-14 rounded-sm overflow-hidden bg-slate-50 flex-shrink-0 shadow-subtle border border-slate-50">
                      <img :src="item.pic_url" class="w-full h-full object-cover">
                    </div>
                    
                    <div class="flex flex-col justify-center min-w-0 flex-1">
                      <h4 class="text-sm font-black text-heading line-clamp-2 leading-tight uppercase italic mb-1">
                        {{ item.title }}
                      </h4>
                      <p class="text-xs font-mono font-bold text-slate-400 uppercase tracking-tighter">
                        ID: {{ item.platform_item_id }}
                      </p>
                    </div>
                  </div>
                </transition-group>
                
                <div v-if="selectedProducts.length === 0 && !isSearching" class="py-20 text-center opacity-20">
                  <PackageSearch :size="64" stroke-width="1" class="mx-auto mb-4" />
                  <p class="text-xs font-black uppercase tracking-widest">暂无数据</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <button 
          @click="handleSubmit" 
          :disabled="loading || !form.shop_id || (productMode === 'partial' && selectedProducts.length === 0) || form.time_slots.length === 0" 
          class="w-full py-6 bg-heading text-white rounded-xl font-black text-base uppercase tracking-[0.2em] hover:bg-primary transition-all active:scale-[0.98] disabled:opacity-20 shadow-main flex items-center justify-center gap-3"
        >
          <Zap v-if="!loading" :size="18" fill="currentColor" />
          {{ loading ? '正在启动任务...' : '启动闪购任务' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue';
import { Package, PackageSearch, RefreshCw, Zap } from 'lucide-vue-next';
import { promotionApi } from '../../api/promotion';
import { productApi } from '../../api/product';
import ShopSelector from '../../components/ShopSelector.vue';
import DatePicker from '../../components/DatePicker.vue';
import ModeToggle from '../../components/common/ModeToggle.vue';
import SearchBar from '../../components/common/SearchBar.vue';
import { useNotification } from '../../composables/useNotification';

const loading = ref(false);
const isSearching = ref(false);
const isCountLoading = ref(false);
const productMode = ref<'all' | 'partial'>('all');
const searchId = ref('');
const onsaleCount = ref(0);
const selectedDate = ref(new Date().toISOString().split('T')[0]);
const selectedProducts = ref<any[]>([]);

const notify = useNotification();

const form = reactive({ 
  shop_id: '', 
  time_slots: [] as { start: string, end: string }[],
});

const formatTimeRange = (h: number) => {
  const hour = String(h).padStart(2, '0');
  return `${hour}:00 - ${hour}:59`;
};

const isSlotSelected = (h: number) => 
  form.time_slots.some(s => s.start === `${String(h).padStart(2, '0')}:00:00`);

const toggleSlot = (h: number) => {
  const start = `${String(h).padStart(2, '0')}:00:00`;
  const end = `${String(h).padStart(2, '0')}:59:59`;
  const idx = form.time_slots.findIndex(s => s.start === start);
  idx > -1 ? form.time_slots.splice(idx, 1) : form.time_slots.push({ start, end });
};

const isAllSelected = computed(() => form.time_slots.length === 24);
const toggleAllSlots = () => {
  if (isAllSelected.value) { form.time_slots = []; }
  else {
    form.time_slots = Array.from({ length: 24 }, (_, i) => ({
      start: `${String(i).padStart(2, '0')}:00:00`,
      end: `${String(i).padStart(2, '0')}:59:59`
    }));
  }
};

const fetchOnsaleCount = async () => {
  if (!form.shop_id) return;
  isCountLoading.value = true;
  try {
    const res = await productApi.getOnsaleCount(form.shop_id);
    onsaleCount.value = res.data.data;
  } finally {
    setTimeout(() => { isCountLoading.value = false; }, 500);
  }
};

const handleShopChange = (val: string) => {
  if (val) fetchOnsaleCount();
  selectedProducts.value = [];
};

const executeProductSearch = async (id: string) => {
  if (!form.shop_id) return alert('请先选择目标店铺');
  
  isSearching.value = true;
  try {
    const res = await productApi.list({ 
      shop_ids: [form.shop_id], 
      status: 'onsale', 
      platform_item_id: id, 
      page_no: 1, 
      page_size: 100 // 🎯 支持批量搜索结果展示
    });

    if (res.data.data.list && res.data.data.list.length > 0) {
      // 🎯 替换为最新的搜索结果（支持多个结果）
      selectedProducts.value = res.data.data.list;
    } else {
      selectedProducts.value = [];
      alert('未找到商品，请确认 ID 是否正确');
    }
  } catch (e) {
    console.error(e);
  } finally {
    isSearching.value = false;
  }
};

const handleSubmit = async () => {
  loading.value = true;
  try {
    const finalSlots = form.time_slots.map(s => ({ 
      start: `${selectedDate.value} ${s.start}`, 
      end: `${selectedDate.value} ${s.end}` 
    }));
    
    const payload = { 
      shop_id: form.shop_id, 
      time_slots: finalSlots, 
      platform_item_ids: productMode.value === 'all' ? null : selectedProducts.value.map(p => p.platform_item_id) 
    };
    
    await promotionApi.createFlashSale(payload);
    notify.success('任务已成功下发', '请稍后关注TikTok后台或者妙手');
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.animate-fade-in { animation: fadeIn 0.4s cubic-bezier(0.16, 1, 0.3, 1); }
@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

.list-enter-active, .list-leave-active { transition: all 0.3s ease; }
.list-enter-from { opacity: 0; transform: scale(0.95); }

/* 已经使用 style.css 中的变量，这里仅保留必要的动画逻辑 */
</style>