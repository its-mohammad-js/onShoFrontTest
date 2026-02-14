<template>
  <section class="container my-5">
    <h3 class="fw-bold mb-4">آخرین وبینارها</h3>

    <!-- لودر -->
    <div v-if="!data.loaded" class="text-center py-5">
      <div class="spinner-border spinner-grow text-danger1" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="text-muted mt-3">در حال بارگذاری...</p>
    </div>

    <!-- نمایش وبینارها -->
    <div v-else>
      <div v-if="data.webinars.length === 0" class="text-center">
        <img src="/images/no.gif" alt="No Courses Found" class="" style="width: 300px; height: auto" />
        <p>هیچ وبیناری برای نمایش وجود ندارد.</p>
      </div>
      <div class="row g-4" v-else>
        <div class="col-lg-4 col-md-6 h-100" v-for="(webinar, index) in data.webinars" :key="index">
          <webinar :webinar="webinar" />
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { reactive, onMounted } from "vue";
import webinar from "@/components/webinar.vue";

const data = reactive({
  webinars: [
    {
      id: "301",
      title: "مقدمه‌ای بر بلاکچین و ارزهای دیجیتال",
      speaker: "دکتر احمدی",
      date: "1404/05/15",
      start_time: "18:00",
      image: "/images/webinars/2.png",
      is_free: false,
      price: "150,000",
    },
    {
      id: "302",
      title: "استراتژی‌های توسعه وب مدرن",
      speaker: "مهندس رضایی",
      date: "1404/05/20",
      start_time: "17:30",
      image: "/images/webinars/1.png",
      is_free: true,
      price: "0",
    },
    {
      id: "303",
      title: "هوش مصنوعی در کسب‌وکار",
      speaker: "خانم محمدی",
      date: "1404/05/25",
      start_time: "19:00",
      image: "/images/webinars/2.png",
      is_free: false,
      price: "200,000",
    },
    {
      id: "304",
      title: "امنیت در برنامه‌نویسی موبایل",
      speaker: "مهندس حسینی",
      date: "1404/06/01",
      start_time: "16:00",
      image: "/images/webinars/1.png",
      is_free: false,
      price: "180,000",
    },
    {
      id: "305",
      title: "مدیریت پروژه با متدولوژی‌های چابک",
      speaker: "دکتر کریمی",
      date: "1404/06/05",
      start_time: "15:30",
      image: "/images/webinars/2.png",
      is_free: false,
      price: "170,000",
    },
    {
      id: "306",
      title: "تحلیل داده با پایتون",
      speaker: "مهندس رحیمی",
      date: "1404/06/10",
      start_time: "18:30",
      image: "/images/webinars/1.png",
      is_free: true,
      price: "0",
    },
    {
      id: "307",
      title: "طراحی تجربه کاربری (UX) پیشرفته",
      speaker: "خانم صادقی",
      date: "1404/06/15",
      start_time: "17:00",
      image: "/images/webinars/2.png",
      is_free: false,
      price: "190,000",
    },
  ],
  loaded: false,
});

onMounted(() => {
  setTimeout(() => {
    data.loaded = true;
  }, 500);
});
</script>

<style scoped>
/* تنظیمات استایل spinner */
.spinner-border {
  width: 3rem;
  height: 3rem;
  border-width: 0.3rem;
}
</style>
