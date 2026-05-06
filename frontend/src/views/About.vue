<template>
  <div class="h-full flex flex-col items-center justify-center animate-fade-up pt-10">
    <div class="max-w-md w-full bg-surface rounded-2xl p-8 shadow-main border border-white text-center">
      <div class="mb-8">
        <div class="w-24 h-24 bg-primary rounded-2xl flex items-center justify-center text-white shadow-active mx-auto mb-6">
          <Zap :size="40" stroke-width="2" />
        </div>
        <h1 class="text-3xl font-black text-heading tracking-tighter uppercase mb-2">
          Automator
        </h1>
        <p class="text-slate-400">妙手 TikTok RPA 自动化工具</p>
      </div>

      <div class="space-y-4 mb-8">
        <div class="flex justify-between items-center py-2 border-b border-slate-100">
          <span class="text-slate-500 text-sm">版本号</span>
          <span class="font-bold text-heading">v0.1.0 测试版</span>
        </div>
        <div class="flex justify-between items-center py-2 border-b border-slate-100">
          <span class="text-slate-500 text-sm">作者</span>
          <span class="font-bold text-heading">Yao</span>
        </div>
        <div class="flex justify-between items-center py-2 border-b border-slate-100">
          <span class="text-slate-500 text-sm">更新日期</span>
          <span class="font-bold text-heading">2026-04-11</span>
        </div>
      </div>

      <div class="mb-8">
        <div class="bg-yellow-50 border border-yellow-100 rounded-lg p-4 text-left">
          <p class="text-yellow-700 text-sm font-medium mb-2">重要提示</p>
          <ul class="text-yellow-600 text-xs space-y-1">
            <li>• 这是内部应用，请勿传播</li>
            <li>• 仅用于测试和提效目的</li>
            <li>• 请遵守相关法律法规</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Zap } from 'lucide-vue-next';
import Button from '../components/common/Button.vue';
</script>
