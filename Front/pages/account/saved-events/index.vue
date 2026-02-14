<template>
    <div class="container py-5">
      <h5 class="mb-4">رویدادهای مورد علاقه من</h5>
      <div class="row g-4">
        <div class="col-lg-6 col-md-6 h-100"
          v-for="(webinar, index) in webinars"
          :key="index"
          
        >
          <div class="card  mb-5 h-100 rounded-3 rounded-top-5">
            <div class="position-relative">
              <img
                :src="getMediaUrl(webinar.image)"
                class="card-img-top"
                :alt="webinar.title"
              />
              <div
                class="position-absolute top-0 start-0 m-3 bg-white rounded-circle shadow-sm d-flex justify-content-center align-items-center w-50-px h-50-px"
              >
                <i class="fas fa-bookmark text-danger1"></i>
              </div>
            </div>
            <div class="card-body">
              <h5 class="card-title fw-bold text-dark text-end">{{ webinar.title }}</h5>
              <p class="text-muted text-end mt-3">سخنران: {{ webinar.speaker }}</p>
  
              <div class="row mb-3">
                <div
                  class="col-6 d-flex align-items-center justify-content-center p-1"
                >
                  <div class="bg-light rounded-3 px-1 py-2">
                    <i class="fas fa-calendar-alt text-danger1 ms-2"></i>
                    <span>{{ webinar.date }}</span>
                  </div>
                </div>
                <div
                  class="col-6 d-flex align-items-center justify-content-center p-1"
                >
                  <div class="bg-light rounded-3 px-1 py-2">
                    <i class="fas fa-clock text-danger1 ms-2"></i>
                    <span>{{ webinar.time }}</span>
                  </div>
                </div>
              </div>
  
              <div class="d-flex justify-content-between align-items-center">
                <button class="btn btn-danger px-4 py-2">ثبت نام وبینار</button>
                <span class="text-muted">{{ webinar.price }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from "vue";
  
  const { getMediaUrl } = useMediaUrl();
  
  const webinars = [
    {
      image: "/images/webinars/1.png",
      title: "نقش امنیت در توسعه نرم‌افزار",
      speaker: "علی محمدی",
      time: "ساعت ۲۰ تا ۲۱:۳۰",
      date: "۱۷ دی ۱۴۰۳",
      price: "رایگان",
    },
    {
      image: "/images/webinars/2.png",
      title: "معرفی بازار آپشن",
      speaker: "علی محمدی",
      time: "ساعت ۲۰ تا ۲۱:۳۰",
      date: "۱۷ دی ۱۴۰۳",
      price: "رایگان",
    },
    {
      image: "/images/webinars/1.png",
      title: "نقش امنیت در توسعه نرم‌افزار",
      speaker: "علی محمدی",
      time: "ساعت ۲۰ تا ۲۱:۳۰",
      date: "۱۷ دی ۱۴۰۳",
      price: "رایگان",
    },
    {
      image: "/images/webinars/2.png",
      title: "معرفی بازار آپشن",
      speaker: "علی محمدی",
      time: "ساعت ۲۰ تا ۲۱:۳۰",
      date: "۱۷ دی ۱۴۰۳",
      price: "رایگان",
    },
  ];
  definePageMeta({
  layout: "account",
  middleware: ['auth']
});
  </script>
  
  <style scoped>
  .card {
    transition: transform 0.2s ease, box-shadow 0.2s ease;
  }
  .card:hover {
    transform: translateY(-5px);
    box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.2);
  }
  .btn-white {
    background-color: #ffffff;
    border: none;
  }
  .text-danger1 {
    color: #dc3545;
  }
  </style>
  