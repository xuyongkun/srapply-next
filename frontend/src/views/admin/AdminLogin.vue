<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "../../stores/auth";

const router = useRouter();
const auth = useAuthStore();

const form = ref({ username: "", password: "" });
const error = ref("");

const doLogin = async () => {
  if (!form.value.username || !form.value.password) {
    error.value = "请输入账号和密码";
    return;
  }
  try {
    await auth.login(form.value);
    router.replace("/admin");
  } catch {
    error.value = "账号或密码错误";
  }
};
</script>

<template>
  <div class="admin-theme admin-login-page">
    <div class="admin-login-card">
      <span class="admin-card-label">管理员入口</span>
      <h1>管理后台</h1>
      <p>请输入账号密码进入咨询线索管理</p>
      <p v-if="error" class="admin-error">{{ error }}</p>
      <input v-model="form.username" placeholder="账号" autocomplete="username" @keyup.enter="doLogin" />
      <input
        v-model="form.password"
        type="password"
        placeholder="密码"
        autocomplete="current-password"
        @keyup.enter="doLogin"
      />
      <button type="button" class="admin-btn-primary" @click="doLogin">登录</button>
      <router-link to="/">返回官网</router-link>
      <p class="admin-login-hint">默认账号：admin / admin123</p>
    </div>
  </div>
</template>
