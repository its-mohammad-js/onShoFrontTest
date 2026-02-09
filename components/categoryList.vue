<template>
  <section class="py-3 py-md-4 bg-white">
    <div class="container">
      <div class="mb-4">
        <h2 class="fw-bold text-dark mb-2">
          موضوعات و دسته‌بندی‌های <span class="text-danger1">آموزشی منتخب</span>
        </h2>
        <div class="d-flex justify-content-end">
          <nuxt-link to="/courses" class="text-primary text-decoration-none">
            <i class="bi bi-chevron-left ms-1"></i>
            همه
          </nuxt-link>
        </div>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">در حال بارگذاری...</span>
        </div>
      </div>

      <!-- Error -->
      <div v-else-if="error" class="text-center py-5 text-danger">
        {{ error }}
      </div>

      <!-- Grid -->
      <div v-else>
        <div class="row g-3 g-md-4">
          <div
            v-for="cat in displayedCategories"
            :key="cat.id"
            class="col-4 col-sm-4 col-md-3 col-lg-2 col-xxl-15"
          >
            <div
              class="category-card p-3 p-md-4 text-center rounded d-flex flex-column align-items-center justify-content-center"
              @click="goToCourses(cat.id)"
            >
              <div class="icon-wrapper mb-3">
                <img :src="cat.logo" alt="" class="category-logo" />
              </div>
              <h6 class="fw-bold mt-2 category-title">{{ cat.title }}</h6>
            </div>
          </div>
        </div>

        <!-- Load More Button -->
        <div v-if="hasMoreCategories" class="text-center mt-4">
          <button @click="loadMore" class="btn btn-outline-primary px-5 py-2">
            بیشتر
          </button>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
const categories = ref([]);
const loading = ref(true);
const error = ref(null);
const itemsToShow = ref(15);
const { getMediaUrl } = useMediaUrl();

const updateItemsToShow = () => {
  if (window.innerWidth <= 767) {
    // on mobile screens
    itemsToShow.value = 9;
  } else {
    //  on larger screens
    itemsToShow.value = 16;
  }
};

const displayedCategories = computed(() => {
  return categories.value.slice(0, itemsToShow.value).map((cat) => ({
    ...cat,
    logo: getMediaUrl(cat.logo),
  }));
});

const hasMoreCategories = computed(() => {
  return categories.value.length > itemsToShow.value;
});

const loadMore = () => {
  itemsToShow.value += 8;
};

const goToCourses = (id) => {
  router.push({ path: "/courses", query: { category: id } });
};

const fetchCategories = async () => {
  try {
    loading.value = true;
    const { $api } = useNuxtApp();

    const res = await $api.post("/course/category/home-page", {});
    console.log("خام API:", res); // اینو تو کنسول ببین

    // پشتیبانی از همه حالت‌های ممکن
    let dataArray = [];

    if (res?.data?.data && Array.isArray(res.data.data)) {
      dataArray = res.data.data;
    } else if (res?.data && Array.isArray(res.data)) {
      dataArray = res.data;
    } else if (Array.isArray(res)) {
      dataArray = res;
    }

    if (dataArray.length > 0) {
      categories.value = dataArray
        .map((cat) => ({
          id: cat.id,
          title: cat.title || "بدون عنوان",
          logo: cat.logo || "/images/home/categories/2.svg",
          display_order:
            cat.display_order || cat.home_page_order || cat.priority || 9999, // Default to high number if not set
        }))
        .sort((a, b) => {
          // Sort by display_order (lower number = higher priority)
          return (a.display_order || 9999) - (b.display_order || 9999);
        });
      console.log("دسته‌بندی‌ها (مرتب شده):", categories.value);
    } else {
      console.log("هیچ دسته‌بندی در صفحه اصلی نیست");
      categories.value = [];
    }
  } catch (err) {
    console.error("خطای کامل:", err);
    error.value = "خطا در بارگذاری دسته‌بندی‌ها";
    categories.value = [];
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  updateItemsToShow();
  fetchCategories();

  window.addEventListener("resize", updateItemsToShow);
});

onBeforeUnmount(() => {
  window.removeEventListener("resize", updateItemsToShow);
});
</script>

<style scoped>
.category-card {
  background: white;
  cursor: pointer;
  transition: 0.3s;
  border: 2px solid transparent;
  aspect-ratio: 1;
  filter: grayscale(100%);
}
.category-card:hover {
  background: #ff8c14;
  color: white;
  border-color: #ff8c14;
  transform: translateY(-5px);
  filter: grayscale(0%);
}
.category-card:hover h6 {
  color: white;
}

.icon-wrapper {
  background: #f8d7da;
  border-radius: 50%;
  width: 80px;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 8px; /* کاهش padding برای بزرگتر شدن لوگو */
}
.category-logo {
  width: 50px;
  height: 50px;
  object-fit: contain; /* بزرگتر کردن لوگو از 45px به 64px */
}
.category-title {
  font-size: 0.85rem;
  line-height: 1.3;
}
@media (min-width: 1400px) {
  .col-xxl-15 {
    flex: 0 0 12.5%;
    max-width: 12.5%;
  }
}
</style>
