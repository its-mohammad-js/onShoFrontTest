<template>
  <div class="container my-5 text-center" v-if="data.loaded">
    <swiper
      :modules="[Pagination]"
      :loop="true"
      :breakpoints="{
        0: { slidesPerView: 2, spaceBetween: 10 },
        768: { slidesPerView: 3, spaceBetween: 20 },
        1024: { slidesPerView: 4, spaceBetween: 30 },
        1200: { slidesPerView: 5, spaceBetween: 40 },
      }"
      class="mySwiper"
    >
      <swiper-slide v-for="(client, index) in clients" :key="index">
        <div class="d-flex flex-column align-items-center justify-content-center">
          <img :src="client.src" :alt="index" class="img-fluid w-50 h-50" />
        </div>
      </swiper-slide>
    </swiper>
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
import "swiper/css";
import "swiper/css/pagination";
import { Pagination } from "swiper/modules";
import { reactive, onMounted } from "vue";

const data = reactive({
  loaded: false,
});

const clients = [
  { src: "/images/home/clients/1.png" },
  { src: "/images/home/clients/2.png" },
  { src: "/images/home/clients/3.svg" },
  { src: "/images/home/clients/1.png" },
  { src: "/images/home/clients/2.png" },
  { src: "/images/home/clients/3.svg" },
  { src: "/images/home/clients/1.png" },
  { src: "/images/home/clients/2.png" },
  { src: "/images/home/clients/3.svg" },
  { src: "/images/home/clients/1.png" },
  { src: "/images/home/clients/2.png" },
];

onMounted(() => {
  setTimeout(() => {
    data.loaded = true;
  }, 500);
});
</script>

<style scoped>
.swiper-slide {
  cursor: grab;
}
</style>
