<script setup>
import { ref, watch } from "vue";
import http from "../../api/http";

const props = defineProps({ leadId: Number });
const emit = defineEmits(["close"]);

const messages = ref([]);

watch(
  () => props.leadId,
  async (id) => {
    if (!id) return;
    const { data } = await http.get(`/api/admin/leads/${id}/messages`);
    messages.value = data;
  },
  { immediate: true }
);
</script>

<template>
  <div class="card">
    <h3>线索 #{{ leadId }} 聊天记录 <button @click="emit('close')">关闭</button></h3>
    <ul>
      <li v-for="msg in messages" :key="msg.id">[{{ msg.role }}] {{ msg.message }}</li>
    </ul>
  </div>
</template>
