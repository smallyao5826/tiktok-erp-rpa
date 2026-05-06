<template>
  <div class="animate-fade-up">
    <header class="flex justify-between items-end px-4 mb-10">
      <div>
        <h2 class="text-3xl font-black text-heading tracking-tighter italic uppercase">Shop <span class="text-primary italic">Console</span></h2>
        <p class="text-slate-400 font-medium mt-1">当前账号共 {{ shops.length }} 个店铺</p>
      </div>
      <button @click="fetchShops" class="p-3 bg-surface rounded-xl shadow-main text-slate-400 hover:text-primary transition-all active:scale-95 group">
        <RefreshCw :size="20" :class="{ 'animate-spin': loading }" class="group-hover:rotate-180 transition-transform duration-500" />
      </button>
    </header>

    <div class="bg-surface rounded-[24px] shadow-main border border-white/50 overflow-hidden">
      <table class="w-full table-fixed border-collapse">
        <thead>
          <tr class="bg-slate-50/50 border-b border-slate-100 text-[11px] font-bold text-slate-400 tracking-widest uppercase">
            <th class="w-32 py-5 text-center">妙手 ID</th>
            <th class="w-[45%] py-5 text-left pl-10">店铺名称</th>
            <th class="w-40 py-5 text-center">所属站点</th>
            <th class="w-40 py-5 text-center">业务平台</th>
          </tr>
        </thead>
        <tbody v-if="shops.length > 0">
          <tr v-for="shop in shops" :key="shop.shop_id" class="group hover:bg-slate-50/40 transition-all border-b border-slate-50 last:border-0">
            <td class="text-center py-6 font-mono text-[11px] text-slate-400">{{ shop.shop_id }}</td>
            <td class="py-6 text-left pl-10">
              <div class="flex items-center gap-3">
                <span class="font-bold text-heading text-[15px] truncate">{{ shop.shop_nick }}</span>
              </div>
            </td>
            <td class="py-6 text-center">
              <div class="inline-flex items-center justify-center px-3 py-1 rounded-md min-w-[85px] border transition-colors"
                :style="{ backgroundColor: getSiteColor(shop.site) + '10', color: getSiteColor(shop.site), borderColor: getSiteColor(shop.site) + '20' }">
                <span class="text-xs font-bold">{{ getSiteName(shop.site) }}</span>
              </div>
            </td>
            <td class="py-6 text-center text-slate-500 font-bold text-[11px] uppercase tracking-widest">TikTok</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { ShoppingBag, RefreshCw } from 'lucide-vue-next';
import { shopApi } from '../api/shop';
import { getSiteName, getSiteColor } from '../utils/mapping';

const shops = ref<any[]>([]);
const loading = ref(false);
const fetchShops = async () => {
  loading.value = true;
  const res = await shopApi.getShops();
  shops.value = res.data.data;
  loading.value = false;
};
onMounted(fetchShops);
</script>