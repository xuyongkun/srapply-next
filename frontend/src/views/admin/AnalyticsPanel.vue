<script setup>
import { ref, onMounted } from "vue";
import http from "../../api/http";

const summary = ref(null);

onMounted(async () => {
  const { data } = await http.get("/api/analytics/summary");
  summary.value = data;
});
</script>

<template>
  <div class="admin-card-stack">
    <div class="admin-page-head">
      <h1 class="admin-page-title">分析看板</h1>
      <p class="admin-page-sub">访客、咨询转化与页面访问概况</p>
    </div>

    <div class="admin-metrics">
      <div class="admin-stat-card">
        <p class="admin-stat-card__value">{{ summary?.total_visitors ?? 0 }}</p>
        <p class="admin-stat-card__label">访客数</p>
      </div>
      <div class="admin-stat-card">
        <p class="admin-stat-card__value">{{ summary?.consultation_visitors ?? 0 }}</p>
        <p class="admin-stat-card__label">发起咨询访客</p>
      </div>
      <div class="admin-stat-card">
        <p class="admin-stat-card__value">{{ summary?.conversion_rate ?? 0 }}%</p>
        <p class="admin-stat-card__label">咨询转化率</p>
      </div>
    </div>

    <div class="admin-panel-card admin-panel-card--static">
      <span class="admin-card-label">流量</span>
      <h2 class="admin-card-title">页面热区（按访问量）</h2>
      <ul class="admin-feed">
        <li v-for="(item, idx) in summary?.top_pages || []" :key="item.page_url">
          <span
            class="admin-feed__indicator"
            :class="{ 'admin-feed__indicator--accent': idx === 0 }"
          />
          <div class="admin-feed__body">
            <div class="admin-mono" style="word-break: break-all">{{ item.page_url }}</div>
          </div>
          <span class="admin-feed__hits">{{ item.hits }}</span>
        </li>
      </ul>
      <p v-if="!(summary?.top_pages?.length)" class="admin-page-sub" style="margin: 12px 0 0">
        暂无访问数据
      </p>
    </div>
  </div>
</template>
