<template>
  <div>
    <section class="bg-white">
      <HomeBanner />
    </section>
    <section class="py-2 py-md-3 bg-white">
      <CategoryList />
    </section>
    <!-- <section class="py-2 py-md-3 bg-light">
    <courses-slider />
  </section> -->
    <section class="py-2 py-md-3 m-0">
      <TrendCourses />
    </section>
    <section class="py-2 py-md-3 m-0">
      <CourseSlider />
    </section>
    <section class="py-2 py-md-3 m-0">
      <discount />
    </section>
    <section class="m-0">
      <LearningPaths />
    </section>
    <!-- <section class="py-2 py-md-3 m-0">
    <CourseSlider />
  </section> -->
    <section class="m-0">
      <PartnerOrganizations />
    </section>
    <section class="m-0">
      <CourseHelpOptions />
    </section>

    <section class="py-2 py-md-3 m-0">
      <webinars-slider />
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from "vue";
import HomeBanner from "~/components/homeBanner.vue";

const { $api } = useNuxtApp();

const activeItem = ref(null);
const orgLoading = ref(true);
const organizations = ref([]);
const scrollContainer = ref(null);
const scrollPosition = ref(0);
const maxScroll = ref(0);

const toggleItem = (id) => {
  activeItem.value = activeItem.value === id ? null : id;
};

// Scroll functions
const scrollLeft = () => {
  if (scrollContainer.value) {
    const scrollAmount = 300;
    scrollContainer.value.scrollLeft -= scrollAmount;
    scrollPosition.value = scrollContainer.value.scrollLeft;
  }
};

const scrollRight = () => {
  if (scrollContainer.value) {
    const scrollAmount = 300;
    scrollContainer.value.scrollLeft += scrollAmount;
    scrollPosition.value = scrollContainer.value.scrollLeft;
  }
};

const updateScrollPosition = () => {
  if (scrollContainer.value) {
    scrollPosition.value = scrollContainer.value.scrollLeft;
    maxScroll.value =
      scrollContainer.value.scrollWidth - scrollContainer.value.clientWidth;
  }
};

// Fetch organizations
const fetchOrganizations = async () => {
  try {
    const response = await $api.post("/course/organization/list", {});

    if (response.data.status && response.data.data.data) {
      organizations.value = response.data.data.data;
    }
  } catch (error) {
    console.error("خطا در دریافت سازمان‌ها:", error);
  } finally {
    orgLoading.value = false;
  }
};

// Lifecycle
onMounted(() => {
  fetchOrganizations();

  // Initialize scroll position after organizations are loaded
  nextTick(() => {
    if (scrollContainer.value) {
      scrollContainer.value.addEventListener("scroll", updateScrollPosition);
      updateScrollPosition();
    }
  });
});
</script>

<style scoped>
.bg-dark-subtle {
  background-color: rgba(43, 45, 66, 1) !important;
}
.accordion-body {
  line-height: 1.8;
  transition: all 0.3s ease-in-out;
}

.accordion-button {
  box-shadow: none;
  border: none;
}

.accordion-button:focus {
  box-shadow: none;
}
.text-danger1 {
  color: #ff8c14;
}
.bg-danger-subtle {
  background-color: #fff5eb !important;
}
.search-box {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  display: flex;
}
.search-box input {
  flex: 1;
  font-size: 16px;
}
.search-btn {
  border: none;
  padding: 10px;
  font-size: 18px;
}
.bg-danger {
  background-color: #ff8c14 !important;
}

.text-primary {
  color: #ff8c14 !important;
}

.btn-primary {
  background-color: #ff8c14;
  border-color: #ff8c14;
}

.btn-primary:hover {
  background-color: #e67a0f;
  border-color: #d66a0a;
}

.btn-outline-primary {
  color: #ff8c14;
  border-color: #ff8c14;
}

.btn-outline-primary:hover {
  background-color: #ff8c14;
  border-color: #ff8c14;
}

.border-primary {
  border-color: #ff8c14 !important;
}

.organization-card {
  transition:
    transform 0.2s ease-in-out,
    box-shadow 0.2s ease-in-out;
}

.organization-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15) !important;
}

.icon {
  font-size: 1.1rem;
}

.badge {
  font-size: 0.875rem;
}

/* Organizations Scroll Styles */
.organizations-scroll-container {
  position: relative;
}

.organizations-scroll-wrapper {
  display: flex;
  overflow-x: auto;
  scroll-behavior: smooth;
  gap: 1.5rem;
  padding: 1rem 0;
  scrollbar-width: none; /* Firefox */
  -ms-overflow-style: none; /* IE and Edge */
}

.organizations-scroll-wrapper::-webkit-scrollbar {
  display: none; /* Chrome, Safari, Opera */
}

.organization-scroll-item {
  flex: 0 0 300px;
  min-width: 300px;
}

.scroll-navigation {
  display: flex;
  justify-content: center;
  align-items: center;
}

.scroll-btn {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.scroll-btn:hover:not(:disabled) {
  background-color: #ff8c14;
  border-color: #ff8c14;
  color: white;
}

.scroll-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Mobile tweaks */
@media (max-width: 576px) {
  .container {
    padding-left: 16px;
    padding-right: 16px;
  }
  h2.fw-bold {
    font-size: 1.25rem;
    line-height: 1.6;
  }
  .w-70-px,
  .h-70-px {
    width: 56px !important;
    height: 56px !important;
  }
  .organization-scroll-item {
    flex: 0 0 260px;
    min-width: 260px;
  }
  img.img-fluid {
    max-width: 100%;
    height: auto;
  }
  .row.gy-2 > [class*="col-"] {
    margin-bottom: 0.5rem;
  }
}
</style>
