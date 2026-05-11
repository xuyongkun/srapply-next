<script setup>
import { ref, onMounted } from "vue";
import http from "../../api/http";

const cases = ref([]);
const advisors = ref([]);
const caseForm = ref({ title: "", summary: "", country: "", major: "" });
const advisorForm = ref({ name: "", title: "", bio: "", specialties: "" });

const fetchCms = async () => {
  const [caseResp, advisorResp] = await Promise.all([
    http.get("/api/cms/cases"),
    http.get("/api/cms/advisors"),
  ]);
  cases.value = caseResp.data;
  advisors.value = advisorResp.data;
};

const createCase = async () => {
  await http.post("/api/cms/cases", caseForm.value);
  caseForm.value = { title: "", summary: "", country: "", major: "" };
  await fetchCms();
};

const createAdvisor = async () => {
  await http.post("/api/cms/advisors", advisorForm.value);
  advisorForm.value = { name: "", title: "", bio: "", specialties: "" };
  await fetchCms();
};

onMounted(fetchCms);
</script>

<template>
  <div class="cms-grid">
    <div class="card">
      <h3>新增留学案例</h3>
      <input v-model="caseForm.title" placeholder="标题" />
      <input v-model="caseForm.country" placeholder="国家" />
      <input v-model="caseForm.major" placeholder="专业" />
      <textarea v-model="caseForm.summary" placeholder="摘要" />
      <button @click="createCase">新增案例</button>
      <ul>
        <li v-for="item in cases" :key="item.id">{{ item.title }} - {{ item.country }} / {{ item.major }}</li>
      </ul>
    </div>
    <div class="card">
      <h3>新增顾问</h3>
      <input v-model="advisorForm.name" placeholder="姓名" />
      <input v-model="advisorForm.title" placeholder="职称" />
      <input v-model="advisorForm.specialties" placeholder="擅长方向" />
      <textarea v-model="advisorForm.bio" placeholder="简介" />
      <button @click="createAdvisor">新增顾问</button>
      <ul>
        <li v-for="item in advisors" :key="item.id">{{ item.name }} - {{ item.title }}</li>
      </ul>
    </div>
  </div>
</template>
