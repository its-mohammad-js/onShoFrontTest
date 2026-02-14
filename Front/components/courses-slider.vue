<template>
  <div class="container my-3 text-center" v-if="data.loaded">
    <div class="d-flex justify-content-start flex-column rounded-3 py-3">
      <div class="nav-custom">
        <a href="javascript:;" :class="{ active: data.selectedcategory === '' }" @click="selectcategory('')">همه</a>
        <a
          href="javascript:;"
          v-for="(category, index) in categoriesWithMediaUrl"
          :key="index"
          :class="{ active: data.selectedcategory === category.id }"
          @click="selectcategory(category.id)"
        >
          <img :src="category.logo" alt="" class="w-20-px" />
          {{ category.title }}
        </a>
      </div>
    </div>

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
          768: { slidesPerView: 2, spaceBetween: 20 },
          1024: { slidesPerView: 3, spaceBetween: 30 },
          1200: { slidesPerView: 3, spaceBetween: 40 },
        }"
        class="mySwiper py-2 px-3"
      >
        <swiper-slide v-for="(course, index) in courses.data" :key="index" class="mb-5 h-100">
          <course :course="course" />
        </swiper-slide>
      </swiper>

      <div class="col-sm-12 text-center position-relative mt-5">
        <img
          src="/images/home/nav.png"
          alt="Illustration"
          class="mb-3 img-fluid position-absolute start-0 bottom-0-px d-none d-md-block"
        />
        <nuxt-link to="/courses" class="btn btn-danger px-4 py-2"> مشاهده تمام دوره‌ها </nuxt-link>
      </div>
    </div>

    <div v-else>
      <img src="/images/no.gif" alt="No Courses Found" class="" style="width: 300px; height: auto" />
      <p class="text-muted">دوره‌ای یافت نشد.</p>
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
import { ref, reactive, onMounted, computed } from "vue";

// Dynamic data from backend
const categories = ref([]);
const organizers = ref([]);
const languages = ref([
  { id: "lang1", name: "انگلیسی" },
  { id: "lang2", name: "ترکی" },
  { id: "lang3", name: "فارسی" },
  { id: "lang4", name: "آلمانی" },
]);

const allCourses = ref({
  data: [],
  count: 0,
  next: null,
  previous: null
});

const data = reactive({
  loaded: false,
  selectedcategory: "",
});

const courses = ref({ data: [] });
const { $api, $sweetalert } = useNuxtApp();
const { getMediaUrl } = useMediaUrl();

// تبدیل آدرس‌های logo به آدرس با /api
const categoriesWithMediaUrl = computed(() => {
  return categories.value.map(cat => ({
    ...cat,
    logo: getMediaUrl(cat.logo)
  }))
});

// Load categories from backend
const loadCategories = async () => {
  try {
    const response = await $api.post('/course/category/list', {});
    if (response.data.status) {
      categories.value = response.data.data;
    }
  } catch (error) {
    console.error('Error loading categories:', error);
  }
};

// Load courses from backend
const loadCourses = async () => {
  data.loaded = false;
  try {
    const requestData = {
      ordering: '-create_date'
    };

    const response = await $api.post('/course/list', requestData);
    if (response.data.status) {
      allCourses.value = response.data.data;
      courses.value.data = response.data.data.data;
    }
  } catch (error) {
    console.error('Error loading courses:', error);
    courses.value.data = [];
  } finally {
    data.loaded = true;
  }
};

const selectcategory = (id) => {
  data.selectedcategory = id;
  filterCourses();
};

const filterCourses = async () => {
  data.loaded = false;
  try {
    const requestData = {
      category_id: data.selectedcategory || null,
      ordering: '-create_date'
    };

    const response = await $api.post('/course/list', requestData);
    if (response.data.status) {
      allCourses.value = response.data.data;
      courses.value.data = response.data.data.data;
    }
  } catch (error) {
    console.error('Error filtering courses:', error);
    courses.value.data = [];
  } finally {
    data.loaded = true;
  }
};

onMounted(async () => {
  await Promise.all([
    loadCategories(),
    loadCourses()
  ]);
});
</script>

<style scoped>
/* تنظیمات اسلایدر */
.swiper-slide {
  cursor: grab;
}
.mySwiper .swiper-pagination-bullet-active {
  background-color: #3e64de;
}
</style>
