<script setup>
import { computed, onMounted } from "vue";
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
  { path: "/admin", name: "admin-leads", label: "线索管理" },
  { path: "/admin/cms", name: "admin-cms", label: "案例 / 顾问 CMS" },
  { path: "/admin/analytics", name: "admin-analytics", label: "分析看板" },
];

const crumb = computed(() => {
  const hit = tabs.find((t) => t.name === route.name);
  return hit?.label || "控制台";
});

const isActive = (name) => route.name === name;

const logout = () => {
  auth.logout();
  router.push("/admin/login");
};
</script>

<template>
  <div class="admin-theme admin-app">
    <aside class="admin-sidebar">
      <div class="admin-sidebar__brand">申荣 · 管理后台</div>

      <router-link
        v-for="tab in tabs"
        :key="tab.path"
        :to="tab.path"
        class="admin-nav-link"
        :class="{ 'admin-nav-link--active': isActive(tab.name) }"
      >
        <svg
          v-if="tab.name === 'admin-leads'"
          width="18"
          height="18"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          aria-hidden="true"
        >
          <path d="M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01" />
        </svg>
        <svg
          v-else-if="tab.name === 'admin-cms'"
          width="18"
          height="18"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          aria-hidden="true"
        >
          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
          <path d="M14 2v6h6M16 13H8M16 17H8M10 9H8" />
        </svg>
        <svg
          v-else
          width="18"
          height="18"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          aria-hidden="true"
        >
          <path d="M18 20V10M12 20V4M6 20v-6" />
        </svg>
        {{ tab.label }}
      </router-link>

      <div class="admin-sidebar__footer">
        <button type="button" class="admin-btn-primary" style="width: 100%" @click="logout">
          退出登录
        </button>
      </div>
    </aside>

    <header class="admin-topbar">
      <div class="admin-breadcrumb">
        控制台 <strong>/</strong> {{ crumb }}
      </div>
      <div class="admin-topbar__meta">
        {{ auth.username || "已登录" }} · {{ auth.role || "-" }}
      </div>
    </header>

    <main class="admin-main">
      <router-view />
    </main>
  </div>
</template>
