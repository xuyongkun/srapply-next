import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import AdminLayout from "../views/admin/AdminLayout.vue";
import AdminLogin from "../views/admin/AdminLogin.vue";
import LeadList from "../views/admin/LeadList.vue";
import CmsPanel from "../views/admin/CmsPanel.vue";
import AnalyticsPanel from "../views/admin/AnalyticsPanel.vue";

const routes = [
  { path: "/", name: "home", component: HomeView },
  {
    path: "/admin",
    component: AdminLayout,
    children: [
      { path: "", name: "admin-leads", component: LeadList },
      { path: "cms", name: "admin-cms", component: CmsPanel },
      { path: "analytics", name: "admin-analytics", component: AnalyticsPanel },
    ],
  },
  { path: "/admin/login", name: "admin-login", component: AdminLogin },
];

export default createRouter({
  history: createWebHistory(),
  routes,
});
