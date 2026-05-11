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
  <div class="card">
    <h3>咨询转化分析</h3>
    <p>访客数：{{ summary?.total_visitors || 0 }}</p>
    <p>发起咨询访客：{{ summary?.consultation_visitors || 0 }}</p>
    <p>咨询转化率：{{ summary?.conversion_rate || 0 }}%</p>
    <h4>页面热区（按访问量）</h4>
    <ul>
      <li v-for="item in summary?.top_pages || []" :key="item.page_url">{{ item.page_url }} - {{ item.hits }}</li>
    </ul>
  </div>
</template>
