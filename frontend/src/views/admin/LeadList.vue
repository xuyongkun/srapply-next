<script setup>
import { ref, onMounted } from "vue";
import http from "../../api/http";
import LeadMessages from "./LeadMessages.vue";

const leads = ref([]);
const users = ref([]);
const loading = ref(false);
const activeLeadId = ref(null);
const statusOptions = ["new", "contacted", "in_progress", "done"];

const fetchLeads = async () => {
  loading.value = true;
  try {
    const { data } = await http.get("/api/admin/leads");
    leads.value = data;
  } finally {
    loading.value = false;
  }
};

const fetchUsers = async () => {
  const { data } = await http.get("/api/admin/users");
  users.value = data;
};

const updateStatus = async (lead, status) => {
  await http.patch(`/api/admin/leads/${lead.id}/status`, { status });
  lead.status = status;
};

const assignLead = async (lead, assignee) => {
  await http.patch(`/api/admin/leads/${lead.id}/assign`, { assigned_to: assignee });
  lead.assigned_to = assignee;
};

onMounted(() => {
  fetchLeads();
  fetchUsers();
});
</script>

<template>
  <div class="admin-card-stack">
    <div class="admin-page-head">
      <h1 class="admin-page-title">线索管理</h1>
      <p class="admin-page-sub">查看与分配咨询线索，更新跟进状态</p>
    </div>

    <div class="admin-metrics">
      <div class="admin-stat-card">
        <p class="admin-stat-card__value">{{ leads.length }}</p>
        <p class="admin-stat-card__label">线索总数</p>
      </div>
      <div class="admin-stat-card">
        <p class="admin-stat-card__value">{{ users.length }}</p>
        <p class="admin-stat-card__label">可分配账号</p>
      </div>
    </div>

    <div class="admin-toolbar">
      <button type="button" :disabled="loading" @click="fetchLeads">
        {{ loading ? "刷新中…" : "刷新列表" }}
      </button>
      <span v-if="loading" class="admin-badge">加载中</span>
    </div>

    <div v-if="!loading" class="admin-table-wrap">
      <table class="admin-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>访客</th>
            <th>首条咨询</th>
            <th>最新消息</th>
            <th>来源页</th>
            <th>微信通知</th>
            <th>客服分配</th>
            <th>状态</th>
            <th>聊天明细</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="lead in leads" :key="lead.id">
            <td class="mono">{{ lead.id }}</td>
            <td class="mono">{{ lead.visitor_id }}</td>
            <td>{{ lead.first_message }}</td>
            <td>{{ lead.latest_message }}</td>
            <td class="mono">{{ lead.page_url }}</td>
            <td>
              <span class="admin-badge" :style="lead.notified_wechat ? {} : { opacity: 0.75 }">
                {{ lead.notified_wechat ? "已发送" : "未发送" }}
              </span>
            </td>
            <td>
              <select :value="lead.assigned_to || ''" @change="(e) => assignLead(lead, e.target.value)">
                <option value="">未分配</option>
                <option v-for="u in users" :key="u.id" :value="u.username">
                  {{ u.username }} ({{ u.role }})
                </option>
              </select>
            </td>
            <td>
              <select :value="lead.status" @change="(e) => updateStatus(lead, e.target.value)">
                <option v-for="s in statusOptions" :key="s" :value="s">{{ s }}</option>
              </select>
            </td>
            <td class="admin-table-actions">
              <button type="button" @click="activeLeadId = lead.id">查看</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <LeadMessages v-if="activeLeadId" :leadId="activeLeadId" @close="activeLeadId = null" />
  </div>
</template>
