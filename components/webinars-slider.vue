<template>
  <div class="container my-5 text-center" v-if="data.loaded">
    <div class="d-flex justify-content-center justify-content-md-start align-items-center">
      <i class="icon icon-filled-rocket text-danger1 fs-1"></i>
    </div>
    <div class="d-flex event-header justify-content-between align-items-center mb-4">
      <h3 class="fw-bold">از دانش تا درآمد، در <span class="text-danger1">وبینارهای تخصصی</span></h3>
      <nuxt-link to="/events" class="btn btn-danger px-4 py-2"> مشاهده همه </nuxt-link>
    </div>

    <!-- اسلایدر -->
    <div v-if="data.webinars && data.webinars.length > 0">
      <swiper
        :style="{
          '--swiper-navigation-color': '#FF8C14',
          '--swiper-pagination-color': '#FF8C14',
        }"
        :modules="[Autoplay, Pagination]"
        :autoplay="{ delay: 5000, disableOnInteraction: false }"
        :pagination="{ clickable: true }"
        :breakpoints="{
          0: { slidesPerView: 2.1, spaceBetween: 12 },
          576: { slidesPerView: 2, spaceBetween: 15 },
          768: { slidesPerView: 3, spaceBetween: 15 },
          992: { slidesPerView: 4, spaceBetween: 15 },
          1200: { slidesPerView: 5, spaceBetween: 20 },
        }"
        loop
        class="mySwiper py-2 px-3"
      >
        <swiper-slide
          v-for="(webinar, index) in data.webinars"
          :key="index"
          class="mb-5 h-100"
        >
          <webinar :webinar="webinar" size="small" />
        </swiper-slide>
      </swiper>
    </div>

    <div v-else>
      <img src="/images/no.gif" alt="No Webinars Found" class="" style="width: 300px; height: auto" />
      <p class="text-muted">وبیناری یافت نشد.</p>
    </div>
  </div>
  <div class="container my-5 text-center" v-else>
    <div class="row">
      <div class="col-sm-12">
        <div v-if="!data.loaded" class="spinner-overlay">
          <div class="spinner-grow text-danger1" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { Swiper, SwiperSlide } from "swiper/vue";
import { Autoplay, Pagination } from "swiper/modules";
import "swiper/css";
import "swiper/css/pagination";
import { reactive, onMounted } from "vue";

// Mock data for webinars
const data = reactive({
  webinars: [
    {
      id: "301",
      title: "مقدمه‌ای بر بلاکچین و ارزهای دیجیتال",
      speaker: "دکتر احمدی",
      date: "1404/05/15",
      start_time: "18:00",
      image: "/images/webinars/1.png",
      is_free: false,
      price: "150,000",
      category: { id: 1, title: "بلاکچین" },
    },
    {
      id: "302",
      title: "استراتژی‌های توسعه وب مدرن",
      speaker: "مهندس رضایی",
      date: "1404/05/20",
      start_time: "17:30",
      image: "/images/webinars/2.png",
      is_free: true,
      price: "0",
      category: { id: 2, title: "برنامه‌نویسی" },
    },
    {
      id: "303",
      title: "هوش مصنوعی در کسب‌وکار",
      speaker: "خانم محمدی",
      date: "1404/05/25",
      start_time: "19:00",
      image: "/images/webinars/1.png",
      is_free: false,
      price: "200,000",
      category: { id: 3, title: "هوش مصنوعی" },
    },
    {
      id: "304",
      title: "امنیت در برنامه‌نویسی موبایل",
      speaker: "مهندس حسینی",
      date: "1404/06/01",
      start_time: "16:00",
      image: "/images/webinars/2.png",
      is_free: false,
      price: "180,000",
      category: { id: 2, title: "برنامه‌نویسی" },
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
@media (max-width: 768px) {
  .event-header {
    flex-direction: column;
  }
  .event-header h3 {
    margin-bottom: 15px;
  }
}
</style>
