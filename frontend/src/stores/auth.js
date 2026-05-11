import { defineStore } from "pinia";
import { ref, computed } from "vue";
import http from "../api/http";

export const useAuthStore = defineStore("auth", () => {
  const token = ref(localStorage.getItem("admin_token") || "");
  const username = ref("");
  const role = ref("");

  const isLoggedIn = computed(() => !!token.value);

  async function login(form) {
    const { data } = await http.post("/api/auth/login", form);
    token.value = data.access_token;
    username.value = data.username;
    role.value = data.role;
    localStorage.setItem("admin_token", data.access_token);
  }

  async function fetchMe() {
    if (!token.value) return;
    try {
      const { data } = await http.get("/api/auth/me");
      username.value = data.username;
      role.value = data.role;
    } catch {
      logout();
    }
  }

  function logout() {
    token.value = "";
    username.value = "";
    role.value = "";
    localStorage.removeItem("admin_token");
  }

  return { token, username, role, isLoggedIn, login, fetchMe, logout };
});
