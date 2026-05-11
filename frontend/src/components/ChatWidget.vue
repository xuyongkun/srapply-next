<script setup>
import { ref } from "vue";
import http from "../api/http";

const open = ref(false);
const input = ref("");
const loading = ref(false);
const messages = ref([{ role: "bot", text: "你好，我是申荣智能助手，请问你想申请哪个国家或专业？" }]);

const visitorId = localStorage.getItem("visitor_id") || `visitor-${Math.random().toString(36).slice(2, 10)}`;
localStorage.setItem("visitor_id", visitorId);

const sendMessage = async () => {
  if (!input.value.trim() || loading.value) return;
  const text = input.value.trim();
  messages.value.push({ role: "user", text });
  input.value = "";
  loading.value = true;

  try {
    const { data } = await http.post("/api/chat/visitor", {
      visitor_id: visitorId,
      message: text,
      page_url: window.location.href
    });
    messages.value.push({
      role: "bot",
      text: data.notified_wechat
        ? `${data.reply}\n(已通知微信客服，线索编号 #${data.lead_id})`
        : `${data.reply}\n(线索编号 #${data.lead_id})`
    });
  } catch (e) {
    messages.value.push({ role: "bot", text: "网络繁忙，请稍后再试。"});
  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <div class="chat-widget">
    <button class="chat-button" @click="open = !open">
      {{ open ? "关闭咨询" : "在线咨询" }}
    </button>
    <div v-if="open" class="chat-panel">
      <div class="chat-list">
        <div
          v-for="(item, idx) in messages"
          :key="idx"
          class="chat-item"
          :class="item.role"
        >
          {{ item.text }}
        </div>
      </div>
      <div class="chat-input">
        <input
          v-model="input"
          placeholder="输入你的问题..."
          @keyup.enter="sendMessage"
        />
        <button :disabled="loading" @click="sendMessage">
          {{ loading ? "发送中..." : "发送" }}
        </button>
      </div>
    </div>
  </div>
</template>
