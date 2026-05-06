<template>
  <div class="h-full flex flex-col animate-fade-up gap-5 selection:bg-primary/10">
    
    <header class="flex justify-between items-end shrink-0 px-1">
      <div>
        <h2 class="text-3xl font-black text-heading tracking-tighter uppercase italic">
          Pricing <span class="text-primary italic">Strategy</span>
        </h2>
        <p class="text-xs text-slate-400 font-bold mt-1 tracking-widest uppercase">
          目前仅支持通过关键词统一折扣或统一价格，不支持特殊价格
        </p>
      </div>
    </header>

    <div class="bg-surface rounded-xl p-4 shadow-main border border-white shrink-0 flex items-end gap-3 relative z-10">
      <div class="flex-1 max-w-[200px]">
        <label class="block text-xs font-black text-slate-400 uppercase mb-1.5 ml-1">01. 店铺</label>
        <ShopSelector v-model="currentShop" mode="single" class="h-[48px]" @change="fetchStrategies" />
      </div>
      <div class="flex-1 min-w-[200px]">
        <label class="block text-xs font-black text-slate-400 uppercase mb-1.5 ml-1">02. 搜索</label>
        <SearchBar 
          v-model="searchKeyword" 
          placeholder="搜索关键词..."
          class="h-[48px]"
          @search="fetchStrategies"
        />
      </div>
      <Button 
        variant="success" 
        size="medium" 
        @click="openAddStrategy"
        class="flex items-center gap-2 h-[48px]"
      >
        新建策略
      </Button>
      <Button 
        variant="ghost" 
        size="medium"
        @click="fetchStrategies"
        class="flex items-center justify-center h-[48px]"
      >
        <RefreshCw :size="16" />
      </Button>
    </div>

    <div class="bg-surface rounded-xl shadow-main border border-white flex-1 flex flex-col min-h-0 relative overflow-hidden">
      <div class="bg-slate-50/80 border-b border-slate-100 overflow-hidden">
        <table class="w-full table-fixed">
          <thead>
            <tr class="text-[11px] font-black text-slate-500 tracking-widest uppercase text-center">
              <th class="py-4 pl-6 w-[80px]">优先级</th>
              <th class="py-4 text-left pl-2 w-[40%]">关键词</th>
              <th class="py-4 w-[30%]">规则类型</th>
              <th class="py-4 pr-6 w-[20%]">操作</th>
            </tr>
          </thead>
        </table>
      </div>

      <div class="flex-1 overflow-y-auto custom-scrollbar">
        <table class="w-full table-fixed">
          <tbody v-if="strategies.length > 0">
            <tr v-for="rule in strategies" :key="rule.id" class="group hover:bg-slate-50/40 border-b border-slate-50 last:border-none transition-all relative">
              <td class="py-3.5 pl-6 w-[80px] text-center">
                <span class="text-lg font-black italic text-slate-200">{{ rule.priority }}</span>
              </td>
              <td class="py-3.5 text-left pl-2 w-[40%]">
                <div class="flex flex-col pr-4">
                  <span class="font-bold text-sm text-heading truncate mb-0.5 tracking-tight">{{ rule.keyword || '全部商品都适用' }}</span>
                </div>
              </td>
              <td class="py-3.5 w-[30%] text-center">
                <div class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-md border border-transparent bg-slate-50">
                  <span class="text-xs font-black tracking-wider">{{ rule.rule_type === 'discount_rate' ? '折扣' : '固定价格' }}</span>
                  <span class="text-xs font-black text-secondary">{{ rule.rule_type === 'discount_rate' ? (rule.rule_value * 10).toFixed(0) + '折' : rule.rule_value.toFixed(2) }}</span>
                </div>
              </td>
              <td class="py-3.5 pr-6 w-[20%] text-center">
                <div class="flex items-center justify-center gap-4 font-mono text-xs font-black uppercase tracking-widest">
                  <button @click="editStrategy(rule)" class="text-secondary hover:brightness-110 active:scale-90 transition-all">编辑</button>
                  <button @click="deleteStrategy(rule.id)" class="text-red-500 hover:brightness-110 active:scale-90 transition-all">删除</button>
                </div>
              </td>
            </tr>
          </tbody>
          <tbody v-else>
            <tr>
              <td colspan="4" class="py-20 text-center text-slate-300">
                <p class="text-xs font-black tracking-widest uppercase">未检索到策略</p>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- 策略编辑弹窗 -->
    <Modal 
      :visible="showStrategyModal" 
      :title="strategyModalTitle"
      @close="showStrategyModal = false"
      @confirm="saveStrategy"
      width="800px"
      class="animate-fade-in"
    >
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="col-span-1 space-y-5">
          <div>
            <label class="block text-xs font-black text-slate-400 uppercase mb-1.5">01. 优先级</label>
            <input 
              v-model.number="newStrategy.priority" 
              type="number" 
              min="0"
              placeholder="数字越大，优先级越高"
              class="w-full text-sm border border-slate-200 rounded-lg p-3 focus:outline-none focus:ring-2 focus:ring-primary/30 transition-all"
            />
          </div>
          <div>
            <label class="block text-xs font-black text-slate-400 uppercase mb-1.5">02. 规则类型</label>
            <Select 
              v-model="newStrategy.rule_type" 
              :options="ruleTypeOptions"
            />
          </div>
          <div>
            <label class="block text-xs font-black text-slate-400 uppercase mb-1.5">03. 规则值</label>
            <input 
              v-model.number="newStrategy.rule_value" 
              type="number" 
              step="0.01"
              min="0.01"
              placeholder="折扣率输入 0.1-1.0，固定价格输入具体金额"
              class="w-full text-sm border border-slate-200 rounded-lg p-3 focus:outline-none focus:ring-2 focus:ring-primary/30 transition-all"
            />
          </div>
          <div>
            <label class="block text-xs font-black text-slate-400 uppercase mb-1.5">04. 关键词</label>
            <input 
              v-model="newStrategy.keyword" 
              type="text" 
              placeholder="输入关键词"
              class="w-full text-sm border border-slate-200 rounded-lg p-3 focus:outline-none focus:ring-2 focus:ring-primary/30 transition-all"
            />

          </div>
        </div>
        <div class="col-span-2 bg-slate-50 rounded-lg p-4 border border-slate-100">
          <h4 class="text-sm font-black text-heading mb-3">填写说明</h4>
          <div class="space-y-3 text-xs text-slate-600">
            <div>
              <p class="font-bold mb-1">优先级</p>
              <p>数字越大，优先级越高，策略执行顺序越靠前</p>
            </div>
            <div>
              <p class="font-bold mb-1">规则类型</p>
              <p>选择折扣率或固定价格</p>
            </div>
            <div>
              <p class="font-bold mb-1">规则值</p>
              <p>折扣率：输入 0.1-1.0，例如 0.5 表示五折</p>
              <p>固定价格：输入具体金额，例如 9.99</p>
            </div>
            <div>
              <p class="font-bold mb-1">关键词</p>
              <p>留空表示全部商品适用</p>
              <p>多个关键词用逗号分隔（OR 逻辑）</p>
              <p>使用 + 连接关键词（AND 逻辑）</p>
              <p>例子：black,white+s 表示 SKU 包含 black 或者 (white 且 s 码) 才适用</p>
            </div>
          </div>
        </div>
      </div>
    </Modal>

    <!-- 删除确认弹窗 -->
    <Modal 
      :visible="showDeleteModal" 
      title="删除策略确认" 
      @close="showDeleteModal = false"
      @confirm="confirmDelete"
      width="400px"
    >
      <div class="p-4">
        <p class="text-sm text-slate-600">确定要删除这个价格策略吗？此操作不可撤销。</p>
      </div>
    </Modal>

  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import { Edit3, Trash2, Plus, RefreshCw } from 'lucide-vue-next';
import { promotionApi } from '../../api/promotion';
import { shopApi } from '../../api/shop';
import ShopSelector from '../../components/ShopSelector.vue';
import SearchBar from '../../components/common/SearchBar.vue';
import Button from '../../components/common/Button.vue';
import Modal from '../../components/common/Modal.vue';
import Select from '../../components/common/Select.vue';
import { useNotification } from '../../composables/useNotification';

const notify = useNotification();

const shopOptions = ref<any[]>([]);
const currentShop = ref('');
const strategies = ref<any[]>([]);
const searchKeyword = ref('');

// 策略弹窗相关状态
const showStrategyModal = ref(false);
const strategyModalTitle = ref('新建价格策略');
const showDeleteModal = ref(false);
const strategyToDelete = ref<number | null>(null);
const newStrategy = ref({
  id: undefined,
  keyword: '',
  rule_type: 'discount_rate',
  rule_value: 0.9,
  priority: 0
});

// 规则类型选项
const ruleTypeOptions = [
  { value: 'discount_rate', label: '统一折扣' },
  { value: 'fixed_price', label: '统一价格' }
];

const fetchStrategies = async () => {
  if (!currentShop.value) return;
  try {
    const res = await promotionApi.getStrategies(currentShop.value, searchKeyword.value);
    strategies.value = res.data.data || [];
  } catch (error) {
    notify.error('通信异常', '获取策略失败');
  }
};

const deleteStrategy = async (id: number) => {
  strategyToDelete.value = id;
  showDeleteModal.value = true;
};

const confirmDelete = async () => {
  if (strategyToDelete.value) {
    try {
      await promotionApi.deleteStrategy(strategyToDelete.value);
      fetchStrategies();
      notify.success('操作成功', '策略已删除');
    } catch (error) {
      notify.error('操作失败', '删除策略失败');
    } finally {
      showDeleteModal.value = false;
      strategyToDelete.value = null;
    }
  }
};

const openAddStrategy = () => {
  // 重置表单
  newStrategy.value = {
    id: undefined,
    keyword: '',
    rule_type: 'discount_rate',
    rule_value: 0.9,
    priority: 0
  };
  strategyModalTitle.value = '新建价格策略';
  showStrategyModal.value = true;
};

const editStrategy = (rule: any) => {
  // 填充现有策略数据
  newStrategy.value = {
    id: rule.id,
    keyword: rule.keyword || '',
    rule_type: rule.rule_type || 'discount_rate',
    rule_value: rule.rule_value || 0.9,
    priority: rule.priority || 0
  };
  strategyModalTitle.value = '编辑价格策略';
  showStrategyModal.value = true;
};

const saveStrategy = async () => {
  if (!currentShop.value) {
    notify.error('操作失败', '请先选择店铺');
    return;
  }
  
  try {
    await promotionApi.saveStrategy({
      id: newStrategy.value.id,
      shop_id: currentShop.value,
      keyword: newStrategy.value.keyword,
      rule_type: newStrategy.value.rule_type,
      rule_value: newStrategy.value.rule_value,
      priority: newStrategy.value.priority
    });
    notify.success('操作成功', newStrategy.value.id ? '策略更新成功' : '策略保存成功');
    showStrategyModal.value = false;
    fetchStrategies();
  } catch (error) {
    notify.error('操作失败', '保存策略失败');
  }
};

watch(currentShop, fetchStrategies);

onMounted(async () => {
  try {
    const res = await shopApi.getShops();
    if (res.data.code === 200) {
      shopOptions.value = res.data.data;
      if (shopOptions.value.length) currentShop.value = shopOptions.value[0].shop_id;
    }
  } catch (error) {
    notify.error('通信异常', '获取店铺列表失败');
  }
});
</script>

<style scoped>
@reference "../../style.css";

/* 动画效果 */
.animate-fade-in {
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 下拉框样式 */
select {
  border-radius: 0.5rem !important;
  border: 1px solid #e2e8f0 !important;
  padding: 0.75rem !important;
  transition: all 0.2s ease !important;
}

select:hover {
  border-color: rgba(254, 44, 85, 0.5) !important;
  cursor: pointer !important;
}

select:focus {
  outline: none !important;
  box-shadow: 0 0 0 2px rgba(254, 44, 85, 0.3) !important;
  border-color: #FE2C55 !important;
}
</style>