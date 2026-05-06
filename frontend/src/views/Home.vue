<template>
  <div class="animate-fade-up space-y-8">
    <header class="flex justify-between items-center">
      <div>
        <h2 class="text-3xl font-black text-heading tracking-tighter italic uppercase">
          RPA <span class="text-primary">Dashboard</span>
        </h2>
        <p class="text-slate-400 font-medium mt-1">欢迎使用妙手 TikTok RPA 自动化工具</p>
      </div>
      <button class="p-3 bg-surface rounded-xl shadow-subtle text-slate-400 hover:text-primary transition-colors"
        @click="refreshStatus">
        <RefreshCw :size="20" />
      </button>
    </header>

    <!-- 系统状态 -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="bg-surface rounded-xl p-6 shadow-main border border-white">
        <div class="flex items-center gap-3 mb-4">
          <div class="w-10 h-10 rounded-lg flex items-center justify-center"
            :class="cookieStatus.valid ? 'bg-green-100 text-green-600' : 'bg-red-100 text-red-600'">
            <ShieldCheck :size="20" />
          </div>
          <div>
            <h3 class="font-bold text-heading">Cookie 状态</h3>
            <p class="text-xs text-slate-400">{{ cookieStatus.valid ? '有效' : '无效' }}</p>
          </div>
        </div>
        <div v-if="!cookieStatus.valid" class="mt-4">
          <Button variant="primary" size="small" @click="$router.push('/login')">
            重新登录
          </Button>
        </div>
      </div>

      <div class="bg-surface rounded-xl p-6 shadow-main border border-white">
        <div class="flex items-center gap-3 mb-4">
          <div class="w-10 h-10 rounded-lg flex items-center justify-center"
            :class="webhookStatus.configured ? 'bg-green-100 text-green-600' : 'bg-yellow-100 text-yellow-600'">
            <Bell :size="20" />
          </div>
          <div>
            <h3 class="font-bold text-heading">Webhook 配置</h3>
            <p class="text-xs text-slate-400">{{ webhookStatus.configured ? '已设置' : '未设置' }}</p>
          </div>
        </div>
        <div v-if="!webhookStatus.configured" class="mt-4">
          <Button variant="primary" size="small" @click="$router.push('/settings')">
            前往设置
          </Button>
        </div>
      </div>

      <div class="bg-surface rounded-xl p-6 shadow-main border border-white">
        <div class="flex items-center gap-3 mb-4">
          <div class="w-10 h-10 rounded-lg flex items-center justify-center bg-blue-100 text-blue-600">
            <Server :size="20" />
          </div>
          <div>
            <h3 class="font-bold text-heading">系统状态</h3>
            <p class="text-xs text-slate-400">{{ systemStatus.running ? '运行中' : '已停止' }}</p>
          </div>
        </div>
        <div class="mt-4">
          <p class="text-xs text-slate-500">版本: {{ systemStatus.version }}</p>
        </div>
      </div>
    </div>

    <!-- 功能介绍 -->
    <div class="bg-surface rounded-xl p-6 shadow-main border border-white">
      <h3 class="font-bold text-heading mb-6 flex items-center gap-2 text-sm tracking-wider uppercase">
        <Zap :size="18" class="text-primary" /> 功能介绍
      </h3>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">

        <div
          class="p-4 bg-slate-50 rounded-xl hover:bg-secondary/5 cursor-pointer group transition-all border border-transparent hover:border-secondary/10">
          <div class="w-10 h-10 rounded-lg flex items-center justify-center bg-secondary/10 text-secondary mb-3">
            <Package :size="20" />
          </div>
          <h4 class="font-bold text-heading group-hover:text-secondary transition-colors">发货管理</h4>
          <p class="text-xs text-slate-400 mt-1">预上线仓库统计，订单管理</p>
          <Button variant="ghost" size="small" class="mt-3" @click="$router.push('/shipping/pre-launch')">
            查看详情
          </Button>
        </div>

        <div
          class="p-4 bg-slate-50 rounded-xl hover:bg-primary/5 cursor-pointer group transition-all border border-transparent hover:border-primary/10">
          <div class="w-10 h-10 rounded-lg flex items-center justify-center bg-primary/10 text-primary mb-3">
            <Zap :size="20" />
          </div>
          <h4 class="font-bold text-heading group-hover:text-primary transition-colors">闪购自动化</h4>
          <p class="text-xs text-slate-400 mt-1">一键创建闪购活动，自动分桶，智能定价</p>
          <Button variant="ghost" size="small" class="mt-3" @click="$router.push('/flash/add')">
            立即使用
          </Button>
        </div>



        <div
          class="p-4 bg-slate-50 rounded-xl hover:bg-blue/5 cursor-pointer group transition-all border border-transparent hover:border-blue/10">
          <div class="w-10 h-10 rounded-lg flex items-center justify-center bg-blue/10 text-blue mb-3">
            <Settings :size="20" />
          </div>
          <h4 class="font-bold text-heading group-hover:text-blue transition-colors">系统设置</h4>
          <p class="text-xs text-slate-400 mt-1">账户管理，Webhook 配置</p>
          <Button variant="ghost" size="small" class="mt-3" @click="$router.push('/settings')">
            前往设置
          </Button>
        </div>
      </div>
    </div>

    <!-- 实现原理 -->
    <div class="bg-surface rounded-xl p-6 shadow-main border border-white">
      <h3 class="font-bold text-heading mb-6 flex items-center gap-2 text-sm tracking-wider uppercase">
        <Cpu :size="18" class="text-primary" /> 实现原理
      </h3>
      <div class="space-y-4">
        <div class="flex gap-4">
          <div class="w-8 h-8 rounded-full bg-primary flex items-center justify-center text-white font-bold flex-shrink-0">1</div>
          <div>
            <h4 class="font-bold text-heading">用户认证</h4>
            <p class="text-xs text-slate-400 mt-1">通过妙手平台的登录接口获取访问权限，确保操作安全可靠</p>
          </div>
        </div>
        <div class="flex gap-4">
          <div class="w-8 h-8 rounded-full bg-primary flex items-center justify-center text-white font-bold flex-shrink-0">2</div>
          <div>
            <h4 class="font-bold text-heading">数据采集</h4>
            <p class="text-xs text-slate-400 mt-1">自动获取店铺信息、商品数据等业务数据，为后续操作做准备</p>
          </div>
        </div>
        <div class="flex gap-4">
          <div class="w-8 h-8 rounded-full bg-primary flex items-center justify-center text-white font-bold flex-shrink-0">3</div>
          <div>
            <h4 class="font-bold text-heading">智能处理</h4>
            <p class="text-xs text-slate-400 mt-1">系统自动编排执行路径，让重复琐碎的操作转化为流畅的自动化。</p>
          </div>
        </div>
        <div class="flex gap-4">
          <div class="w-8 h-8 rounded-full bg-primary flex items-center justify-center text-white font-bold flex-shrink-0">4</div>
          <div>
            <h4 class="font-bold text-heading">实时通知</h4>
            <p class="text-xs text-slate-400 mt-1">通过飞书 Webhook 推送任务状态，让您随时了解操作进展</p>
          </div>
        </div>
      </div>
    </div>


  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { RefreshCw, Zap, ShieldCheck, Bell, Server, Package, Settings, Cpu } from 'lucide-vue-next';
import Button from '../components/common/Button.vue';
import { useNotification } from '../composables/useNotification';
import { authApi } from '../api/auth';
import { systemApi } from '../api/system';

const notify = useNotification();

// 状态数据
const cookieStatus = ref({ valid: true });
const webhookStatus = ref({ configured: false });
const systemStatus = ref({ running: true, version: 'v0.1.0 测试版' });

// 刷新状态
const refreshStatus = async () => {
  try {
    // 检查系统状态
    try {
      const systemRes = await systemApi.checkSystemStatus();
      systemStatus.value.running = systemRes.data.status === 'online';
    } catch (error) {
      systemStatus.value.running = false;
    }

    // 检查 Cookie 状态
    try {
      const accountRes = await authApi.getAccountInfo();
      cookieStatus.value.valid = accountRes.data.code === 200;
    } catch (error) {
      cookieStatus.value.valid = false;
    }

    // 检查 Webhook 状态
    try {
      const webhookRes = await systemApi.getWebhookList();
      webhookStatus.value.configured = (webhookRes.data.data || []).length > 0;
    } catch (error) {
      webhookStatus.value.configured = false;
    }

  } catch (error) {
    notify.error('操作失败', '状态刷新失败');
  }
};

// 初始加载
onMounted(async () => {
  refreshStatus();
});
</script>