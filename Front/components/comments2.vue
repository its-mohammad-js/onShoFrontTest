<template>
  <section class="py-5 testimonials-section">
    <div class="container">
      <!-- Header Section -->
      <div class="header d-flex align-items-center justify-content-between mb-5 position-relative">
        <div class="header-text">
          <div class="d-flex justify-content-start align-items-center mb-2">
            <i class="icon icon-filled-rocket text-danger1 fs-1"></i>
          </div>
          <h2 class="fw-bold">این پلتفرم زندگی من را تغییر داد!</h2>
        </div>
        <div class="header-img">
          <img src="/images/home/comments.png" class="img-fluid position-absolute start-0 bottom-50" />
        </div>
      </div>

      <!-- Swiper Slider -->
      <swiper
        :slides-per-view="'auto'"
        :centeredSlides="true"
        :space-between="30"
        :autoplay="{ delay: 3000, disableOnInteraction: false }"
        :loop="true"
        :modules="[Autoplay, Pagination]"
        class="mySwiper p-3"
      >
        <swiper-slide 
          v-for="(testimonial, index) in testimonials" 
          :key="index" 
          class="custom-slide"
        >
          <div class="card modern-card h-100">
            <div class="card-body text-center">
              <div class="text-end">
                <i class="fas fa-quote-right text-danger1 fs-1 mb-3"></i>
              </div>
              <h5 class="fw-bold mb-3">{{ testimonial.course }}</h5>
              <p class="text-muted lh-lg mb-4">{{ testimonial.description }}</p>
              <div class="testimonial-footer d-flex flex-column align-items-center justify-content-center gap-3">
                <div class="d-flex align-items-center gap-2">
                  <img
                    :src="testimonial.image"
                    alt="Student Avatar"
                    class="avatar rounded-circle shadow-sm"
                  />
                  <p class="mb-0 fw-bold">{{ testimonial.name }}</p>
                </div>
                <div class="status">
                  <p class="text-danger1 fw-bold mb-0">
                    <span class="text-muted me-2">وضعیت :</span> {{ testimonial.status }}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </swiper-slide>
      </swiper>
    </div>
  </section>
</template>

<script setup>
import { Swiper, SwiperSlide } from "swiper/vue";
import { Autoplay, Pagination } from "swiper/modules"; 
import "swiper/css";
import "swiper/css/pagination";
import { computed } from 'vue'

const { getMediaUrl } = useMediaUrl();

const testimonialsRaw = [
  {
    course: "دوره آموزشی Excel, Power BI, SQL",
    description:
      "لورم ایپسوم متن ساختگی با تولید سادگی نامفهوم از صنعت چاپ...",
    image: "/images/home/icons/student.png",
    name: "نام دانشجو",
    status: "استخدام شده",
  },
  {
    course: "دوره آموزشی Excel, Power BI, SQL",
    description:
      "لورم ایپسوم متن ساختگی با تولید سادگی نامفهوم از صنعت چاپ...",
    image: "/images/home/icons/student.png",
    name: "نام دانشجو",
    status: "استخدام شده",
  },
  {
    course: "دوره آموزشی Excel, Power BI, SQL",
    description:
      "لورم ایپسوم متن ساختگی با تولید سادگی نامفهوم از صنعت چاپ...",
    image: "/images/home/icons/student.png",
    name: "نام دانشجو",
    status: "استخدام شده",
  },
  {
    course: "دوره آموزشی Excel, Power BI, SQL",
    description:
      "لورم ایپسوم متن ساختگی با تولید سادگی نامفهوم از صنعت چاپ...",
    image: "/images/home/icons/student.png",
    name: "نام دانشجو",
    status: "استخدام شده",
  },
  {
    course: "دوره آموزشی Excel, Power BI, SQL",
    description:
      "لورم ایپسوم متن ساختگی با تولید سادگی نامفهوم از صنعت چاپ...",
    image: "/images/home/icons/student.png",
    name: "نام دانشجو",
    status: "استخدام شده",
  },
  {
    course: "دوره آموزشی Excel, Power BI, SQL",
    description:
      "لورم ایپسوم متن ساختگی با تولید سادگی نامفهوم از صنعت چاپ...",
    image: "/images/home/icons/student.png",
    name: "نام دانشجو",
    status: "استخدام شده",
  },
];

// تبدیل آدرس‌های تصویر به آدرس با /api
const testimonials = computed(() => {
  return testimonialsRaw.map(testimonial => ({
    ...testimonial,
    image: getMediaUrl(testimonial.image)
  }))
});
</script>

<style scoped>
:root {
  --primary-color: #FF8C14;
  --card-bg: #ffffff;
  --card-gradient: linear-gradient(135deg, #ffffff, #f2f2f2);
  --transition-ease: cubic-bezier(0.4, 0, 0.2, 1);
}

.testimonials-section {
  background: #f8f9fa;
  padding: 4rem 0;
}

.header h2 {
  font-size: 2.5rem;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
}

/* Swiper Settings */
.mySwiper {
  padding-bottom: 50px;
}

/* Slide Style */
.custom-slide {
  width: 320px;
  opacity: 0.6;
  transform: scale(0.90);
  filter: grayscale(75%);
  transition: opacity 0.5s var(--transition-ease), transform 0.5s var(--transition-ease);
}

/* Slide Active */
.mySwiper .swiper-slide-active {
  opacity: 1;
  transform: scale(1);
  filter: grayscale(0%);
}

/* Modern Card Style */
.modern-card {
  background: var(--card-gradient);
  border: none;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  transition: all ease-in-out 0.3s;
}

.modern-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
}

.card-body {
  padding: 2rem;
}

.avatar {
  width: 50px;
  height: 50px;
  object-fit: cover;
}

/* Pagination Bullets */
.mySwiper .swiper-pagination-bullet {
  background: #ddd;
  opacity: 1;
  transition: background 0.3s;
}

.mySwiper .swiper-pagination-bullet-active {
  background: var(--primary-color);
}

/* Responsive Adjustments */
@media (max-width: 768px) {
  .custom-slide {
    width: 260px;
  }
  .header h2 {
    font-size: 2rem;
  }
  .header-img img {
    width: 100px !important;
    margin-bottom: 25px;
  }
}
</style>
