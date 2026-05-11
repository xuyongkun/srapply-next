<script setup>
import { onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useAuthStore } from "../../stores/auth";

const router = useRouter();
const route = useRoute();
const auth = useAuthStore();

onMounted(async () => {
  if (!auth.isLoggedIn) {
    router.replace("/admin/login");
    return;
  }
  await auth.fetchMe();
});

const tabs = [
  { path: "/admin", label: "线索管理" },
  { path: "/admin/cms", label: "案例/顾问 CMS" },
  { path: "/admin/analytics", label: "分析看板" },
];
</script>

<template>
  <div class="card admin-panel">
    <h1>管理后台</h1>
    <p>当前用户：{{ auth.username || "已登录" }}（{{ auth.role || "-" }}）</p>
    <div class="toolbar">
      <router-link
        v-for="tab in tabs"
        :key="tab.path"
        :to="tab.path"
        class="tab-link"
        :class="{ active: route.path === tab.path }"
      >
        {{ tab.label }}
      </router-link>
      <button @click="auth.logout(); router.push('/admin/login')">退出登录</button>
    </div>
    <router-view />
  </div>
</template>
