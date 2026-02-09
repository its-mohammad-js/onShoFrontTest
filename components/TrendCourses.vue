<!-- <template>
  <div class="container my-5 text-center" v-if="data.loaded">
    <div class="d-flex justify-content-between align-items-center mb-4 flex-column flex-md-row text-center text-md-start">
      <h3 class="fw-bold mb-3 mb-md-0">دوره‌های ترند</h3>
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
          0: { slidesPerView: 1, spaceBetween: 10 },
          768: { slidesPerView: 2, spaceBetween: 20 },
          1024: { slidesPerView: 3, spaceBetween: 30 },
          1200: { slidesPerView: 3, spaceBetween: 40 },
        }"
        class="mySwiper py-2 px-3"
      >
        <swiper-slide v-for="(course, index) in courses.data" :key="index" class="mb-5 h-100">
          <course :course="course" class="shadow-sm" />
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
</template> -->

<template>
  <div class="container my-5 text-center" v-if="data.loaded">
    <!-- Title -->
    <div class="d-flex justify-content-between align-items-center mb-4 flex-column flex-md-row text-center text-md-start">
      <h3 class="fw-bold mb-3 mb-md-0">دوره‌های ترند</h3>
    </div>

    <!-- Category Tabs - Level 1 -->
    <div class="category-tabs-wrapper mb-4">
      <div v-if="parentCategories.length === 0 && data.loaded" class="text-muted mb-2">
        دسته‌بندی‌ای یافت نشد
      </div>
      <ul v-if="parentCategories.length > 0" class="nav justify-content-center mb-2 tabs-list tabs-level-1">
        <li
          v-for="cat in parentCategories"
          :key="cat.id"
          class="nav-item mx-2 tab-item"
          :class="{ 
            activeTab: activeParentCategory?.id === cat.id,
            hasSubs: cat.children && cat.children.length > 0
          }"
          @click="selectParentCategory(cat)"
          @mouseenter="hoveredParentCategory = cat.id"
          @mouseleave="hoveredParentCategory = null"
        >
          {{ cat.title }}
          <i v-if="cat.children && cat.children.length > 0" class="bi bi-chevron-down ms-1"></i>
        </li>
      </ul>

      <!-- Category Tabs - Level 2 (Subcategories) -->
      <ul 
        v-if="activeParentCategory && activeParentCategory.children && activeParentCategory.children.length > 0"
        class="nav justify-content-center tabs-list tabs-level-2"
      >
        <li
          v-for="subCat in activeParentCategory.children"
          :key="subCat.id"
          class="nav-item mx-2 tab-item"
          :class="{ activeTab: activeSubCategory?.id === subCat.id }"
          @click="selectSubCategory(subCat)"
        >
          {{ subCat.title }}
        </li>
      </ul>
    </div>

    <!-- Slider -->
    <div v-if="filteredCourses.length > 0">
      <swiper
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
          v-for="(course, index) in filteredCourses"
          :key="index"
          class="mb-5 h-100"
        >
          <course :course="course" size="small" class="shadow-sm" />
        </swiper-slide>
      </swiper>
    </div>

    <div v-else>
      <img src="/images/no.gif" style="width: 300px" />
      <p class="text-muted">دوره‌ای یافت نشد.</p>
    </div>
  </div>

  <!-- Loading -->
  <div class="container my-5 text-center" v-else>
    <div class="spinner-grow text-danger1" role="status">
      <span class="visually-hidden">Loading...</span>
    </div>
  </div>
</template>

<script setup>
import { Swiper, SwiperSlide } from "swiper/vue";
import { Autoplay, Pagination } from "swiper/modules";
import "swiper/css";
import "swiper/css/pagination";
import { ref, reactive, onMounted, computed } from "vue";

const { $api } = useNuxtApp();

const parentCategories = ref([]);
const activeParentCategory = ref(null);
const activeSubCategory = ref(null);
const hoveredParentCategory = ref(null);

// No need for client-side filtering - API handles it
const filteredCourses = computed(() => {
  return courses.value.data || [];
});

const courses = ref({
  data: [],
});

const data = reactive({
  loaded: false,
});

// Load categories - Level 1 (Parent categories)
const loadCategories = async () => {
  try {
    const response = await $api.post('/course/category/list', {});
    console.log('📂 Category API Response:', response.data);
    
    // Handle different response structures
    let allCategories = [];
    if (response.data?.status && response.data?.data) {
      allCategories = response.data.data;
    } else if (response.data?.data && Array.isArray(response.data.data)) {
      allCategories = response.data.data;
    } else if (Array.isArray(response.data)) {
      allCategories = response.data;
    }
    
    console.log('📋 All Categories:', allCategories);
    
    // Get all parent categories (level 1) that have children
    // Filter categories where istrend is true OR show all parent categories with children
    parentCategories.value = allCategories.filter(cat => {
      // Show if it has children and (istrend is true OR we show all)
      return cat.children && cat.children.length > 0;
    }).map(cat => ({
      id: cat.id,
      title: cat.title || 'بدون عنوان',
      children: (cat.children || []).map(child => ({
        id: child.id,
        title: child.title || 'بدون عنوان'
      }))
    }));
    
    console.log('🎯 Parent Categories with children:', parentCategories.value);
    
    // If no categories with istrend found, show all parent categories with children
    if (parentCategories.value.length === 0) {
      console.log('⚠️ No categories with istrend found, showing all parent categories');
    }
  } catch (error) {
    console.error('❌ Error loading categories:', error);
    parentCategories.value = [];
  }
};

const allCourses = ref([]); // Store all courses

const selectParentCategory = async (cat) => {
  activeParentCategory.value = cat;
  activeSubCategory.value = null; // Reset subcategory when parent changes
  // Load trending courses for this parent category (includes all subcategories recursively)
  await loadCourses(cat.id);
};

const selectSubCategory = async (subCat) => {
  activeSubCategory.value = subCat;
  await filterCourses();
};

// Load trending courses from new API endpoint
const loadCourses = async (categoryId = null) => {
  data.loaded = false;
  try {
    const requestData = {
      page: 1,
      page_size: 50
    };
    
    if (categoryId) {
      requestData.category_id = categoryId;
    }
    
    console.log('🔥 Trending Courses API Request:', requestData);
    const response = await $api.post('/course/trending', requestData);
    console.log('🔥 Trending Courses API Response:', response.data);
    
    // Handle new API response format: { status: true, data: { results: [...] } }
    if (response.data?.status && response.data?.data?.results) {
      const coursesList = response.data.data.results;
      courses.value.data = coursesList;
      
      // Store all courses if no category filter
      if (!categoryId) {
        allCourses.value = coursesList;
      }
    } else if (response.data?.status && response.data?.data?.data) {
      // Fallback to old format
      const coursesList = response.data.data.data;
      courses.value.data = coursesList;
      if (!categoryId) {
        allCourses.value = coursesList;
      }
    } else {
      courses.value.data = [];
      if (!categoryId) {
        allCourses.value = [];
      }
    }
  } catch (error) {
    console.error('❌ Error loading trending courses:', error);
    courses.value.data = [];
    if (!categoryId) {
      allCourses.value = [];
    }
  } finally {
    data.loaded = true;
  }
};

const filterCourses = async () => {
  // Load courses with category filter
  await loadCourses(activeSubCategory.value?.id || null);
};

onMounted(async () => {
  await Promise.all([
    loadCategories(),
    loadCourses()
  ]);
});
</script>

<style scoped>
.font-size-12-px {
  font-size: 12px;
}
.bg-danger {
  background-color: #FF8C14 !important;
}

.tabs-list {
  border-bottom: 1px solid #eee;
  padding-bottom: 10px;
}

.tab-item {
  cursor: pointer;
  font-weight: 500;
  padding: 6px 15px;
  color: #444;
  position: relative;
}

.tab-item:hover {
  color: #FF8C14;
}

.activeTab {
  color: #FF8C14;
  font-weight: bold;
}

.activeTab::after {
  content: "";
  position: absolute;
  bottom: -10px;
  left: 0;
  width: 100%;
  height: 3px;
  background-color: #FF8C14;
  border-radius: 4px;
}

.category-tabs-wrapper {
  position: relative;
}

.tabs-level-1 {
  border-bottom: 2px solid #eee;
  padding-bottom: 10px;
  margin-bottom: 0;
}

.tabs-level-2 {
  border-bottom: 1px solid #eee;
  padding-bottom: 10px;
  margin-top: 10px;
  animation: slideDown 0.3s ease-out;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.tab-item.hasSubs {
  position: relative;
}

.tab-item.hasSubs:hover {
  background-color: rgba(255, 140, 20, 0.05);
  border-radius: 8px;
}

.tabs-level-2 .tab-item {
  font-size: 0.9rem;
  padding: 4px 12px;
}

.tabs-level-2 .tab-item:hover {
  background-color: rgba(255, 140, 20, 0.05);
  border-radius: 6px;
}

/* Mobile: 4 categories in one row */
@media (max-width: 767.98px) {
  .tabs-level-1 {
    display: grid !important;
    grid-template-columns: repeat(4, 1fr);
    gap: 8px;
    justify-items: center;
  }
  
  .tabs-level-1 .nav-item {
    margin: 0 !important;
    width: 100%;
    text-align: center;
  }
  
  .tabs-level-1 .tab-item {
    padding: 6px 8px;
    font-size: 0.75rem;
    width: 100%;
    text-align: center;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  
  .tabs-level-1 .tab-item i {
    display: none;
  }
}

</style>
