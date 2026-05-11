<script setup>
import { ref, onMounted } from "vue";
import http from "../../api/http";
import { useAuthStore } from "../../stores/auth";
import LeadMessages from "./LeadMessages.vue";

const auth = useAuthStore();
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
  <div>
    <p>共 {{ leads.length }} 条线索</p>
    <button @click="fetchLeads">刷新</button>
    <p v-if="loading">加载中...</p>

    <table v-if="!loading" class="lead-table">
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
          <td>{{ lead.id }}</td>
          <td>{{ lead.visitor_id }}</td>
          <td>{{ lead.first_message }}</td>
          <td>{{ lead.latest_message }}</td>
          <td>{{ lead.page_url }}</td>
          <td>{{ lead.notified_wechat ? "已发送" : "未发送" }}</td>
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
          <td><button @click="activeLeadId = lead.id">查看</button></td>
        </tr>
      </tbody>
    </table>

    <LeadMessages v-if="activeLeadId" :leadId="activeLeadId" @close="activeLeadId = null" />
  </div>
</template>
