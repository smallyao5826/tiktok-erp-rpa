<template>
    <div class="h-screen w-screen flex bg-surface overflow-hidden">

        <div
            class="hidden lg:flex flex-1 relative bg-slate-50 flex-col items-center justify-center p-20 overflow-hidden">
            <div class="absolute top-[-10%] left-[-10%] w-[60%] h-[60%] bg-primary/5 rounded-full blur-[120px]"></div>
            <div class="absolute bottom-[-10%] right-[-10%] w-[50%] h-[50%] bg-secondary/5 rounded-full blur-[100px]">
            </div>

            <div class="relative z-10 text-center animate-fade-up">
                <div
                    class="inline-flex w-24 h-24 bg-white rounded-xl items-center justify-center shadow-main mb-12 animate-float">
                    <Zap :size="48" stroke-width="2.5" class="text-primary fill-primary/10" />
                </div>

                <h1 class="text-5xl font-black text-heading tracking-tighter uppercase mb-6">
                    妙手<span class="text-primary"> TikTok </span>助手
                </h1>

                <div class="h-px w-12 bg-slate-200 mx-auto mb-6"></div>

                <p class="text-base text-slate-400 font-medium tracking-[0.3em] uppercase opacity-80">
                    赋能全链路电商自动化方案
                </p>
            </div>

            <div class="absolute bottom-10 left-10 text-xs font-bold text-slate-300 uppercase tracking-widest">
                Version 0.1.0 · 测试版
            </div>
        </div>

        <div
            class="w-full lg:w-[540px] flex flex-col justify-center p-12 lg:p-24 bg-surface relative z-20 shadow-[-20px_0_80px_-20px_rgba(0,0,0,0.04)]">

            <div class="max-w-[360px] mx-auto w-full animate-fade-up" style="animation-delay: 0.1s">
                <header class="mb-12 text-left">
                    <h2 class="text-2xl font-black text-heading tracking-tight mb-2">欢迎回来</h2>
                    <p class="text-sm font-medium text-slate-400">请输入您的妙手官方账号进行身份验证</p>
                </header>

                <div class="space-y-8">
                    <div class="space-y-3">
                        <label class="block text-xs font-black text-slate-400 uppercase tracking-widest ml-1">账号 /
                            Account</label>
                        <input v-model="form.account" type="text"
                            class="w-full bg-slate-50 border-none px-5 py-4 text-sm font-bold text-heading rounded-md outline-none transition-all shadow-subtle focus:bg-white focus:ring-4 focus:ring-primary/5 placeholder:text-slate-300"
                            placeholder="手机号或邮箱地址" />
                    </div>

                    <div class="space-y-3">
                        <label class="block text-xs font-black text-slate-400 uppercase tracking-widest ml-1">密码 /
                            Password</label>
                        <input v-model="form.password" type="password"
                            class="w-full bg-slate-50 border-none px-5 py-4 text-sm font-bold text-heading rounded-md outline-none transition-all shadow-subtle focus:bg-white focus:ring-4 focus:ring-primary/5 placeholder:text-slate-300"
                            placeholder="请输入登录密码" />
                    </div>

                    <button @click="handleLogin" :disabled="loading"
                        class="w-full py-5 bg-heading text-white font-black rounded-md hover:bg-primary shadow-active active:scale-[0.98] transition-all disabled:opacity-50 disabled:scale-100 flex items-center justify-center gap-3 text-base uppercase tracking-[0.15em] mt-4">
                        <Loader2 v-if="loading" :size="20" class="animate-spin" />
                        {{ loading ? '登录中...' : '登录' }}
                    </button>
                </div>

                <footer class="mt-12 flex flex-col items-center space-y-1.5">
                    <p class="text-sm text-slate-300 font-medium tracking-wider uppercase">
                        登录即视为已同意本系统的自动化执行策略
                    </p>
                    <p class="text-sm text-slate-300 font-medium tracking-wider uppercase">
                        数据仅存储于本地运行环境，不经过云端服务器
                    </p>
                </footer>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { Zap, Loader2 } from 'lucide-vue-next';
import { authApi } from '../api/auth';
import { useNotification } from '../composables/useNotification';

const router = useRouter();
const notify = useNotification();
const loading = ref(false);
const form = ref({ account: '', password: '' });

const handleLogin = async () => {
    if (!form.value.account || !form.value.password) {
        return notify.warning('请完整填写', '账号或密码不能为空，请输入后重试');
    }

    loading.value = true;
    try {
        const res = await authApi.login(form.value);
        if (res.data.code === 200) {
            notify.success('验证成功', '欢迎回来');
            router.push('/');
        } else {
            notify.error('登录失败', res.data.msg || '账号或密码验证未通过');
        }
    } catch (error) {
        notify.error('网络错误', '无法连接至服务器，请确保后端服务已启动');
    } finally {
        loading.value = false;
    }
};
</script>

<style scoped>
/* 自定义浮动动画 */
@keyframes float {
    0% {
        transform: translateY(0px);
    }

    50% {
        transform: translateY(-10px);
    }

    100% {
        transform: translateY(0px);
    }
}

.animate-float {
    animation: float 4s ease-in-out infinite;
}

/* 覆盖 focus 时的阴影，让它更柔和 */
input:focus {
    box-shadow: var(--shadow-main);
}
</style>