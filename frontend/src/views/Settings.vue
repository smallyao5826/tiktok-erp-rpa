<template>
  <div class="h-full flex flex-col animate-fade-up gap-5 selection:bg-primary/10">
    
    <header class="flex justify-between items-end shrink-0 px-1">
      <div>
        <h2 class="text-3xl font-black text-heading tracking-tighter uppercase italic">
          Settings <span class="text-primary italic">Panel</span>
        </h2>
        <p class="text-xs text-slate-400 font-bold mt-1 tracking-widest uppercase">
          系统设置与账户管理
        </p>
      </div>
    </header>

    <div class="bg-surface rounded-xl p-6 shadow-main border border-white shrink-0 relative z-10">
      <h3 class="text-lg font-black text-heading mb-6">账户信息</h3>
      
      <div class="space-y-4">
        <div class="flex items-center justify-between p-4 bg-slate-50 rounded-lg border border-slate-100">
          <div>
            <p class="text-sm font-black text-heading mb-1">当前账户</p>
            <p class="text-xs text-slate-400">{{ accountInfo?.account || '未登录' }}</p>
          </div>
          <Button 
            variant="primary" 
            size="medium"
            @click="navigateToLogin"
            class="flex items-center gap-2"
          >
            切换账户
          </Button>
        </div>
      </div>
    </div>

    <div class="bg-surface rounded-xl p-6 shadow-main border border-white shrink-0 relative z-10">
      <div class="flex justify-between items-center mb-6">
        <h3 class="text-lg font-black text-heading">飞书 Webhook 配置</h3>
        <Button 
          variant="success" 
          size="medium"
          @click="openWebhookModal"
          class="flex items-center gap-2"
        >
          添加飞书 Webhook
        </Button>
      </div>
      
      <div class="mb-4 p-3 bg-blue-50 rounded-lg border border-blue-100">
        <p class="text-xs text-blue-700">
          <span class="font-bold">提示：</span> 目前仅支持飞书 Webhook，用于接收添加闪购活动的通知消息。
        </p>
      </div>
      
      <div class="space-y-4">
        <div v-if="webhooks.length === 0" class="py-10 text-center text-slate-400">
          <p class="text-sm font-black uppercase tracking-widest">暂无飞书 Webhook 配置</p>
        </div>
        
        <div v-for="webhook in webhooks" :key="webhook.id" class="flex items-center justify-between p-4 bg-slate-50 rounded-lg border border-slate-100">
          <div class="flex-1">
            <p class="text-sm font-black text-heading mb-1">飞书 Webhook URL</p>
            <p class="text-xs text-slate-400 truncate">{{ webhook.url }}</p>
          </div>
          <div class="flex items-center gap-2">
            <Button 
              variant="ghost" 
              size="small"
              @click="editWebhook(webhook)"
              class="h-8"
            >
              编辑
            </Button>
            <Button 
              variant="ghost" 
              size="small"
              @click="deleteWebhook(webhook.id)"
              class="h-8 text-red-500"
            >
              删除
            </Button>
          </div>
        </div>
      </div>
    </div>

    <!-- Webhook 编辑弹窗 -->
    <Modal 
      :visible="webhookModalVisible" 
      :title="webhookModalTitle"
      @close="webhookModalVisible = false"
      @confirm="saveWebhook"
    >
      <div class="space-y-4">
        <div>
          <label class="block text-xs font-black text-slate-400 uppercase mb-1.5">飞书 Webhook URL</label>
          <input 
            v-model="webhookForm.url" 
            type="text" 
            placeholder="输入飞书 Webhook URL"
            class="w-full text-sm border border-slate-200 rounded-lg p-3 focus:outline-none focus:ring-2 focus:ring-primary/30 transition-all"
          />
        </div>
        <div class="p-3 bg-blue-50 rounded-lg border border-blue-100">
          <p class="text-xs text-blue-700">
            <span class="font-bold">获取方法：</span> 飞书群 -> 群设置 -> 智能助手 -> 添加机器人 -> 自定义机器人 -> 复制 Webhook 地址
          </p>
        </div>
      </div>
    </Modal>

  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import Button from './../components/common/Button.vue';
import Modal from './../components/common/Modal.vue';
import { useNotification } from './../composables/useNotification';
import { authApi } from './../api/auth';
import { systemApi } from './../api/system';

const router = useRouter();
const notify = useNotification();
const accountInfo = ref<any>(null);
const webhooks = ref<any[]>([]);

// Webhook 弹窗相关状态
const webhookModalVisible = ref(false);
const webhookModalTitle = ref('添加 Webhook');
const webhookForm = ref({
  id: null,
  url: ''
});

const fetchAccountInfo = async () => {
  try {
    const res = await authApi.getAccountInfo();
    accountInfo.value = res.data.data;
  } catch (error) {
    notify.error('通信异常', '获取账户信息失败');
  }
};

const fetchWebhooks = async () => {
  try {
    const res = await systemApi.getWebhookList();
    webhooks.value = res.data.data || [];
  } catch (error) {
    notify.error('通信异常', '获取 Webhook 配置失败');
  }
};

const navigateToLogin = () => {
  if (confirm('确定要切换账户吗？切换后需要重新登录。')) {
    router.push('/login');
  }
};

const openWebhookModal = () => {
  webhookForm.value = {
    id: null,
    url: ''
  };
  webhookModalTitle.value = '添加飞书 Webhook';
  webhookModalVisible.value = true;
};

const editWebhook = (webhook: any) => {
  webhookForm.value = {
    id: webhook.id,
    url: webhook.url
  };
  webhookModalTitle.value = '编辑 Webhook';
  webhookModalVisible.value = true;
};

const saveWebhook = async () => {
  if (!webhookForm.value.url) {
    notify.error('操作失败', '请输入 Webhook URL');
    return;
  }
  
  try {
    if (webhookForm.value.id) {
      // 更新 Webhook
      await systemApi.updateWebhook(webhookForm.value.id, webhookForm.value.url);
      notify.success('操作成功', 'Webhook 更新成功');
    } else {
      // 添加 Webhook
      await systemApi.addWebhook(webhookForm.value.url);
      notify.success('操作成功', 'Webhook 添加成功');
    }
    webhookModalVisible.value = false;
    fetchWebhooks();
  } catch (error) {
    notify.error('操作失败', '保存 Webhook 失败');
  }
};

const deleteWebhook = async (webhookId: number) => {
  if (confirm('确定要删除这个 Webhook 吗？')) {
    try {
      await systemApi.deleteWebhook(webhookId);
      notify.success('操作成功', 'Webhook 删除成功');
      fetchWebhooks();
    } catch (error) {
      notify.error('操作失败', '删除 Webhook 失败');
    }
  }
};

onMounted(() => {
  fetchAccountInfo();
  fetchWebhooks();
});
</script>