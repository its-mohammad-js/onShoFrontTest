<template>
  <div class="container my-5 text-center" v-if="data.loaded">
    <div class="d-flex justify-content-between align-items-center mb-4 flex-column flex-md-row text-center text-md-start">
      <h3 class="fw-bold mb-3 mb-md-0">تخفیف ویژه</h3>
      <span class="text-muted d-flex align-items-center flex-column flex-md-row">
        <span class="mb-2 mb-md-0 ms-md-2">زمان باقی‌مانده تا پایان تخفیفات :</span>
        <div class="d-flex align-items-center justify-content-center flex-wrap">
          <span class="badge bg-danger text-white px-2 py-2 mx-1">
            {{ timer.seconds }}
            <span class="small d-block">ثانیه</span>
          </span>
          <span class="badge bg-danger text-white px-2 py-2 mx-1">
            {{ timer.minutes }}
            <span class="small d-block">دقیقه</span>
          </span>
          <span class="badge bg-danger text-white px-2 py-2 mx-1">
            {{ timer.hours }}
            <span class="small d-block">ساعت</span>
          </span>
          <span class="badge bg-danger text-white px-2 py-2 mx-1">
            {{ timer.days }}
            <span class="small d-block">روز</span>
          </span>
        </div>
      </span>
    </div>

    <!-- Slider -->
    <div v-if="courses.data && courses.data.length > 0">
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
        class="mySwiper py-2 px-3"
      >
        <swiper-slide
          v-for="(course, index) in courses.data"
          :key="index"
          class="mb-5 h-100"
        >
          <course :course="course" size="small" class="shadow-sm" />
        </swiper-slide>
      </swiper>
    </div>

    <div v-else>
      <img src="/images/no.gif" alt="No Courses Found" class="" style="width: 300px; height: auto" />
      <p class="text-muted">دوره‌ای یافت نشد.</p>
    </div>
  </div>
  <div class="container my-5 text-center" v-else>
    <div class="row">
      <div class="col-sm-12">
        <div class="spinner-grow text-danger1" role="status">
          <span class="visually-hidden">Loading...</span>
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
import { ref, reactive, onMounted } from "vue";

// Mock data for discounted courses
const courses = ref({
  data: [
    {
      id: "201",
      slug: "python-advanced",
      title: "پایتون پیشرفته",
      organizer: { name: "موسسه فناوری برتر" },
      image: "/images/courses/1.png",
      category: { id: 1, title: "برنامه‌نویسی" },
      attributes: [
        { title: "مدت زمان دوره", value: "30 ساعت" },
        { title: "تعداد موقعیت شغلی", value: "15" },
        { slug: "language", value: "پایتون" },
      ],
      price: "2,000,000",
      discount: { percentage: 20, discountedPrice: "1,600,000" },
    },
    {
      id: "202",
      slug: "react-js",
      title: "آموزش ری‌اکت",
      organizer: { name: "آکادمی وب" },
      image: "/images/courses/1.png",
      category: { id: 2, title: "طراحی وب" },
      attributes: [
        { title: "مدت زمان دوره", value: "25 ساعت" },
        { title: "تعداد موقعیت شغلی", value: "10" },
        { slug: "language", value: "جاوااسکریپت" },
      ],
      price: "1,800,000",
      discount: { percentage: 15, discountedPrice: "1,530,000" },
    },
    {
      id: "203",
      slug: "machine-learning",
      title: "یادگیری ماشین",
      organizer: { name: "مرکز نوآوری داده" },
      image: "/images/courses/1.png",
      category: { id: 3, title: "هوش مصنوعی" },
      attributes: [
        { title: "مدت زمان دوره", value: "40 ساعت" },
        { title: "تعداد موقعیت شغلی", value: "8" },
        { slug: "language", value: "پایتون" },
      ],
      price: "2,500,000",
      discount: { percentage: 25, discountedPrice: "1,875,000" },
    },
    {
      id: "204",
      slug: "cybersecurity-basics",
      title: "مبانی امنیت سایبری",
      organizer: { name: "موسسه امنیت" },
      image: "/images/courses/1.png",
      category: { id: 4, title: "امنیت سایبری" },
      attributes: [
        { title: "مدت زمان دوره", value: "20 ساعت" },
        { title: "تعداد موقعیت شغلی", value: "12" },
        { slug: "language", value: "متفرقه" },
      ],
      price: "1,500,000",
      discount: { percentage: 10, discountedPrice: "1,350,000" },
    },
  ],
});

const data = reactive({
  loaded: false,
});

const timer = reactive({
  days: '۰',
  hours: '۰',
  minutes: '۰',
  seconds: '۰',
});

// تبدیل اعداد انگلیسی به فارسی
const toPersianNumber = (num) => {
  const persianDigits = ['۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹'];
  return String(num).replace(/\d/g, d => persianDigits[d]);
};

const startTimer = () => {
  const endDate = new Date().getTime() + 3 * 24 * 60 * 60 * 1000; // 3 روز از الان
  setInterval(() => {
    const now = new Date().getTime();
    const distance = endDate - now;

    timer.days = toPersianNumber(Math.floor(distance / (1000 * 60 * 60 * 24)));
    timer.hours = toPersianNumber(Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)));
    timer.minutes = toPersianNumber(Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60)));
    timer.seconds = toPersianNumber(Math.floor((distance % (1000 * 60)) / 1000));
  }, 1000);
};

onMounted(() => {
  setTimeout(() => {
    data.loaded = true;
  }, 500);
  startTimer();
});
</script>

<style scoped>
.font-size-12-px {
  font-size: 12px;
}
.bg-danger {
  background-color: #FF8C14 !important;
}
</style>
