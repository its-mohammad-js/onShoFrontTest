<template>
    <section class="py-5">
      <div class="container">
        <div class="d-flex align-items-center justify-content-between mb-5 position-relative">
            <div>
                <div class="d-flex justify-content-start align-items-center mb-2">
                  <i class="icon icon-filled-rocket text-danger1 fs-1"></i>
          </div>
          <h2 class="fw-bold">
            این پلتفرم زندگی من را تغییر داد!
          </h2>
            </div>
            <div>
                <img src="/images/home/comments.png" class="img-fluid position-absolute start-0 bottom-50"/>
            </div>
        </div>
        <swiper
        :slides-per-view="1"
        :space-between="30"
        :autoplay="{ delay: 5000, disableOnInteraction: false }"
        :loop="true"
        :modules="[Autoplay, Pagination]"
        :breakpoints="{
          768: { slidesPerView: 1 },
          1024: { slidesPerView: 2 }
        }"
        class="mySwiper p-3"
      >
        <swiper-slide v-for="(testimonial, index) in testimonials" :key="index">
  <div class="card shadow-sm border-0 h-100 rounded-4">
    <div class="card-body text-center p-4">
      <div class="d-flex align-items-center justify-content-between flex-column flex-md-row text-center text-md-start mb-3">
        <h5 class="fw-bold mb-2 mb-md-0">{{ testimonial.course }}</h5>
        <i class="fas fa-quote-right text-danger1 fs-3"></i>
      </div>

      <p class="text-muted lh-lg text-end text-md-start">{{ testimonial.description }}</p>

      <div class="d-flex align-items-center justify-content-between flex-column flex-md-row text-center text-md-start mt-4">
        <div class="d-flex gap-2 align-items-center flex-column flex-md-row">
          <img
            :src="testimonial.image"
            alt="Student Avatar"
            class="rounded-circle shadow-sm"
            style="width: 40px; height: 40px"
          />
          <p class="mb-1 fw-bold">{{ testimonial.name }}</p>
        </div>
        <div class="text-center text-md-end mt-2 mt-md-0">
          <p class="text-danger1 fw-bold mb-0"><span class="text-muted ms-2">وضعیت :</span> {{ testimonial.status }}</p>
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
import { Autoplay, Pagination } from "swiper/modules"; // 🚀 اضافه کردن ماژول‌های لازم
import "swiper/css";
import "swiper/css/pagination";
import { computed } from 'vue'

const { getMediaUrl } = useMediaUrl();
  
  const testimonialsRaw = [
    {
      course: "دوره آموزشی Excel, Power BI, SQL",
      description:
        "لورم ایپسوم متن ساختگی با تولید سادگی نامفهوم از صنعت چاپ، و با استفاده از طراحان گرافیک است، چاپگرها و متون بلکه روزنامه و مجله در ستون و سطرآنچنان که لازم است، و برای شرایط فعلی تکنولوژی مورد نیاز، و کاربردهای متنوع با هدف بهبود ابزارهای کاربردی می باشد، کتابهای زیادی در شصت و سه درصد گذشته حال و آینده، شناخت فراوان جامعه و متخصصان را می طلبد",
        image: "/images/home/icons/student.png",
      name: "نام دانشجو",
      status: "استخدام شده",
    },
    {
      course: "دوره آموزشی Excel, Power BI, SQL",
      description:
        "لورم ایپسوم متن ساختگی با تولید سادگی نامفهوم از صنعت چاپ، و با استفاده از طراحان گرافیک است، چاپگرها و متون بلکه روزنامه و مجله در ستون و سطرآنچنان که لازم است، و برای شرایط فعلی تکنولوژی مورد نیاز، و کاربردهای متنوع با هدف بهبود ابزارهای کاربردی می باشد، کتابهای زیادی در شصت و سه درصد گذشته حال و آینده، شناخت فراوان جامعه و متخصصان را می طلبد",
      image: "/images/home/icons/student.png",
      name: "نام دانشجو",
      status: "استخدام شده",
    },
    {
      course: "دوره آموزشی Excel, Power BI, SQL",
      description:
        "لورم ایپسوم متن ساختگی با تولید سادگی نامفهوم از صنعت چاپ، و با استفاده از طراحان گرافیک است، چاپگرها و متون بلکه روزنامه و مجله در ستون و سطرآنچنان که لازم است، و برای شرایط فعلی تکنولوژی مورد نیاز، و کاربردهای متنوع با هدف بهبود ابزارهای کاربردی می باشد، کتابهای زیادی در شصت و سه درصد گذشته حال و آینده، شناخت فراوان جامعه و متخصصان را می طلبد",
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
  .mySwiper .swiper-pagination-bullet-active {
    background-color: #FF8C14;
  }
  .card {
    transition: transform 0.3s ease;
  }
  .card:hover {
    transform: scale(1.05);
  }
  </style>
  