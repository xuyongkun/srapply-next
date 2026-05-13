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
  <div class="admin-theme admin-modal-backdrop" @click.self="emit('close')">
    <div class="admin-modal" role="dialog" aria-modal="true" aria-labelledby="lead-msg-title">
      <div class="admin-modal__head">
        <h2 id="lead-msg-title" class="admin-card-title" style="margin: 0">
          线索 #{{ leadId }} 聊天记录
        </h2>
        <button type="button" @click="emit('close')">关闭</button>
      </div>
      <div class="admin-modal__body">
        <ul class="admin-modal__list">
          <li
            v-for="msg in messages"
            :key="msg.id"
            :style="{
              borderLeftColor:
                msg.role === 'user' ? 'var(--admin-accent)' : 'var(--admin-border-visible)',
            }"
          >
            <span class="admin-mono" style="color: var(--admin-text-muted)">[{{ msg.role }}]</span>
            {{ msg.message }}
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>
