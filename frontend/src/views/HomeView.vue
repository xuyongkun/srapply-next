<script setup>
import { onMounted, onUnmounted, ref } from "vue";
import http from "../api/http";
import ChatWidget from "../components/ChatWidget.vue";

const info = ref(null);
const cases = ref([]);
const advisors = ref([]);
const navScrolled = ref(false);

const visitorId = localStorage.getItem("visitor_id") || `visitor-${Math.random().toString(36).slice(2, 10)}`;
localStorage.setItem("visitor_id", visitorId);

const handleScroll = () => {
  navScrolled.value = window.scrollY > 60;
};

const scrollTo = (id) => {
  document.getElementById(id)?.scrollIntoView({ behavior: "smooth" });
};

onMounted(async () => {
  window.addEventListener("scroll", handleScroll, { passive: true });

  try {
    const [siteInfo, caseResp, advisorResp] = await Promise.all([
      http.get("/api/public/site-info"),
      http.get("/api/cms/cases"),
      http.get("/api/cms/advisors")
    ]);
    info.value = siteInfo.data;
    cases.value = caseResp.data;
    advisors.value = advisorResp.data;
  } catch {
    // use fallbacks below
  }

  http.post("/api/analytics/track", {
    visitor_id: visitorId,
    event_type: "page_view",
    page_url: window.location.href
  }).catch(() => {});
});

onUnmounted(() => {
  window.removeEventListener("scroll", handleScroll);
});

// ── Fallback helpers ──
const highlights = () => info.value?.highlights || [
  { title: "定位准确",  icon: "target",   desc: "基于学生背景与职业规划，精准匹配最适合的院校与专业，拒绝模板化方案。" },
  { title: "服务周到",  icon: "heart",    desc: "从选校到行前，全流程一对一顾问跟进，7×24小时在线答疑，让家长更放心。" },
  { title: "经验丰富",  icon: "star",     desc: "核心顾问团队平均从业年限超过8年，累计服务学生2000+，名校录取率行业领先。" },
  { title: "与时俱进",  icon: "trending", desc: "持续跟踪各国签证政策与院校招生动态，确保申请策略始终走在最前沿。" },
];

const about = () => info.value?.about || {
  intro: "申荣留学是壹佰(香港)教育集团全资控股的高端留学咨询品牌，专注于为每一位学生提供个性化、透明化的留学规划服务。我们致力于打破传统留学中介的信息壁垒，让优质海外教育资源触手可及。",
  mission: "我们的使命是让留学服务更简单、更透明。从选校定位、背景提升、文书定制到签证指导、行前准备，申荣团队提供全流程一站式服务，用专业与真诚陪伴每一位学子的留学之路。",
};

const stats = () => info.value?.stats || [
  { value: "10+",  label: "年行业经验" },
  { value: "2000+", label: "服务学生" },
  { value: "98%",  label: "签证通过率" },
  { value: "100+", label: "合作院校" },
];

const contact = () => info.value?.contact || {
  email: "srapply@163.com",
  phone: "18516222635",
  wechat_hint: "提交咨询后实时通知微信客服",
};

const locations = () => info.value?.locations || [
  { city: "成都", district: "高新区",  address: "环球中心E2-5楼喵谷",             metro: "地铁1号线锦城广场站A口" },
  { city: "成都", district: "天府新区", address: "天府二街166号雄川金融中心1栋19楼", metro: "" },
  { city: "南昌", district: "",         address: "恒茂梦时代广场7号楼603室",        metro: "" },
  { city: "香港", district: "九龙",     address: "旺角亚皆老街98号富都大厦0222室",  metro: "" },
];

const getInitial = (name) => (name || "?")[0];

const avatarColors = ["#1a56db","#7c3aed","#db2777","#ea580c"];
const getAvatarColor = (i) => avatarColors[i % avatarColors.length];

const heroSlogan = () => info.value?.slogan || "让留学更简单 · To Be Easier And Better";
const brandName = () => info.value?.brand || "申荣留学";
</script>

<template>
  <div class="home-page">

    <!-- ══════ Nav ══════ -->
    <nav class="nav-bar" :class="{ scrolled: navScrolled }">
      <div class="nav-inner">
        <span class="nav-logo">{{ brandName() }}</span>
        <ul class="nav-links">
          <li><a href="#" @click.prevent="scrollTo('hero')">首页</a></li>
          <li><a href="#" @click.prevent="scrollTo('about')">关于申荣</a></li>
          <li><a href="#" @click.prevent="scrollTo('features')">服务优势</a></li>
          <li><a href="#" @click.prevent="scrollTo('cases')">成功案例</a></li>
          <li><a href="#" @click.prevent="scrollTo('team')">顾问团队</a></li>
          <li><a href="#" @click.prevent="scrollTo('contact')">联系我们</a></li>
        </ul>
      </div>
    </nav>

    <!-- ══════ Hero ══════ -->
    <section id="hero" class="hero-section">
      <div class="hero-bg-circle"></div>
      <div class="hero-bg-circle"></div>
      <div class="hero-bg-circle"></div>
      <div class="hero-content">
        <h1 class="hero-brand">{{ brandName() }}</h1>
        <p class="hero-slogan">{{ heroSlogan() }}</p>
        <div class="hero-actions">
          <a href="#" class="btn btn-primary" @click.prevent="scrollTo('contact')">立即咨询</a>
          <a href="#" class="btn btn-outline" @click.prevent="scrollTo('cases')">查看案例</a>
        </div>
      </div>
    </section>

    <!-- ══════ About ══════ -->
    <section id="about" class="section">
      <div class="section-inner">
        <div class="section-header">
          <h2>关于申荣</h2>
          <p>壹佰(香港)教育集团旗下高端留学品牌</p>
        </div>
        <div class="about-grid">
          <div class="about-text">
            <p>{{ about().intro }}</p>
            <p>{{ about().mission }}</p>
          </div>
          <div class="stats-grid">
            <div class="stat-card" v-for="s in stats()" :key="s.label">
              <p class="stat-value">{{ s.value }}</p>
              <p class="stat-label">{{ s.label }}</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ══════ Features ══════ -->
    <section id="features" class="section" style="background:#fff">
      <div class="section-inner">
        <div class="section-header">
          <h2>我们的优势</h2>
          <p>专业团队 · 透明服务 · 值得信赖</p>
        </div>
        <div class="features-grid">
          <div class="feature-card" v-for="h in highlights()" :key="h.title">
            <div class="feature-icon" :class="h.icon">
              <!-- target -->
              <svg v-if="h.icon==='target'" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#1a56db" stroke-width="2"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>
              <!-- heart -->
              <svg v-else-if="h.icon==='heart'" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#db2777" stroke-width="2"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>
              <!-- star -->
              <svg v-else-if="h.icon==='star'" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#d97706" stroke-width="2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
              <!-- trending -->
              <svg v-else width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#059669" stroke-width="2"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/></svg>
            </div>
            <h3>{{ h.title }}</h3>
            <p>{{ h.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- ══════ Cases ══════ -->
    <section id="cases" class="section">
      <div class="section-inner">
        <div class="section-header">
          <h2>成功案例</h2>
          <p>每一位学生的梦想，都是我们全力以赴的理由</p>
        </div>
        <div class="cases-grid" v-if="cases.length">
          <div class="case-card" v-for="(c, i) in cases" :key="c.id">
            <div class="case-card-top">
              <div class="case-avatar" :style="{ background: getAvatarColor(i) }">{{ getInitial(c.title) }}</div>
              <div>
                <h3>{{ c.title }}</h3>
                <span class="case-country">{{ c.country }} / {{ c.major }}</span>
              </div>
            </div>
            <div class="case-card-body">
              <p>{{ c.summary }}</p>
            </div>
          </div>
        </div>
        <p v-else style="text-align:center;color:var(--color-text-muted)">案例数据加载中，请联系顾问获取最新录取案例。</p>
      </div>
    </section>

    <!-- ══════ Team ══════ -->
    <section id="team" class="section" style="background:#fff">
      <div class="section-inner">
        <div class="section-header">
          <h2>顾问团队</h2>
          <p>术业有专攻 · 每一位顾问都有自己最擅长的领域</p>
        </div>
        <div class="team-grid" v-if="advisors.length">
          <div class="team-card" v-for="(a, i) in advisors" :key="a.id">
            <div class="team-avatar" :style="{ background: getAvatarColor(i) }">{{ getInitial(a.name) }}</div>
            <h3>{{ a.name }}</h3>
            <p class="team-title">{{ a.title }}</p>
            <p class="team-bio">{{ a.bio }}</p>
            <div class="team-tags">
              <span class="team-tag" v-for="t in (a.specialties || '').split(/, ?/).filter(Boolean)" :key="t">{{ t }}</span>
            </div>
          </div>
        </div>
        <p v-else style="text-align:center;color:var(--color-text-muted)">顾问数据加载中，请联系客服了解更多。</p>
      </div>
    </section>

    <!-- ══════ Contact ══════ -->
    <section id="contact" class="section">
      <div class="section-inner">
        <div class="section-header">
          <h2>联系我们</h2>
          <p>多个城市设有办公室，欢迎来访咨询</p>
        </div>
        <div class="contact-grid">
          <div class="contact-highlights">
            <div class="contact-item">
              <div class="contact-item-icon email">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#1a56db" stroke-width="2"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 4-10 8L2 4"/></svg>
              </div>
              <div>
                <div class="contact-item-label">邮箱</div>
                <div class="contact-item-value">{{ contact().email }}</div>
              </div>
            </div>
            <div class="contact-item">
              <div class="contact-item-icon phone">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#059669" stroke-width="2"><rect x="5" y="2" width="14" height="20" rx="2"/><line x1="12" y1="18" x2="12.01" y2="18"/></svg>
              </div>
              <div>
                <div class="contact-item-label">电话</div>
                <div class="contact-item-value">{{ contact().phone }}</div>
              </div>
            </div>
            <div class="contact-item">
              <div class="contact-item-icon wechat">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#d97706" stroke-width="2"><path d="M8 10.9c3.6 0 6.5-2.6 6.5-5.7 0-3.2-2.9-5.7-6.5-5.7S1.5 2 1.5 5.2c0 1.8 1 3.4 2.5 4.4L3 12l2.8-1.3c.7.2 1.5.2 2.2.2z"/><path d="M14.5 13.1c3.7 0 6.5-2.5 6.5-5.6 0-3-2.8-5.5-6.5-5.5"/><path d="M18.5 19.9c3.2 0 5.5-2 5.5-4.5 0-2.4-2.3-4.5-5.5-4.5S13 13 13 15.4c0 1.4.8 2.6 2 3.4l-.5 1.7 2.2-1c.5.2 1.2.2 1.8.2z"/></svg>
              </div>
              <div>
                <div class="contact-item-label">微信客服</div>
                <div class="contact-item-value">{{ contact().wechat_hint }}</div>
              </div>
            </div>
          </div>
          <div class="locations-grid">
            <div class="location-card" v-for="loc in locations()" :key="loc.address">
              <p class="location-city">{{ loc.city }}{{ loc.district ? ' · ' + loc.district : '' }}</p>
              <p class="location-addr">{{ loc.address }}<span v-if="loc.metro"> · {{ loc.metro }}</span></p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ══════ Footer ══════ -->
    <footer class="site-footer">
      <p class="footer-brand">申荣留学</p>
      <p class="footer-info">
        &copy; 2019 成都申荣壹佰教育咨询有限公司<br>
        <a href="https://beian.miit.gov.cn/" target="_blank" rel="noopener">蜀ICP备17035358号-1</a>
        &nbsp;·&nbsp;
        <router-link to="/admin">管理后台</router-link>
      </p>
    </footer>

    <!-- ══════ Chat Widget ══════ -->
    <ChatWidget />
  </div>
</template>

<style scoped>
.home-page {
  /* ensures the nav and everything stack properly */
}
</style>
