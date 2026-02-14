<template>
  <div class="row">
    <div class="col-12">
      <div class="card border-0 shadow-sm">
        <div class="card-header bg-light border-0 py-3">
          <h5 class="mb-0 text-dark">
            <i class="icon icon-filled-book text-primary me-2"></i>
            دوره‌های {{ organization.name }}
          </h5>
        </div>
        <div class="card-body">
          <!-- Loading Courses -->
          <div v-if="coursesLoading" class="text-center py-4">
            <div class="spinner-border text-primary" role="status">
              <span class="visually-hidden">در حال بارگذاری...</span>
            </div>
          </div>

          <!-- No Courses -->
          <div v-else-if="courses.length === 0" class="text-center py-5">
            <i
              class="icon icon-filled-book text-muted"
              style="font-size: 3rem"
            ></i>
            <h5 class="text-muted mt-3">هنوز دوره‌ای منتشر نشده است</h5>
            <p class="text-muted">این آموزشگاه هنوز دوره‌ای منتشر نکرده است</p>
          </div>

          <!-- Courses Grid -->
          <div v-else class="row g-4">
            <div
              v-for="course in visibleCourses"
              :key="course.id"
              class="col-lg-4 col-md-6"
            >
              <div class="card border-0 shadow-sm h-100">
                <div class="position-relative">
                  <img
                    :src="
                      getMediaUrl(course.image) || '/images/courses/default.jpg'
                    "
                    :alt="course.title"
                    class="card-img-top"
                    style="height: 200px; object-fit: cover"
                  />
                  <div
                    class="position-absolute top-0 end-0 m-2 d-flex flex-column gap-1"
                  >
                    <span class="badge bg-primary">
                      {{ course.category?.title || "دسته‌بندی نشده" }}
                    </span>
                    <!-- type tag -->
                    <span
                      v-if="course.type"
                      class="badge custom-badge"
                      :class="getCourseTypeBadgeClass(course.type_value)"
                    >
                      <i
                        :class="getCourseTypeIcon(course.type_value)"
                        class="me-1"
                      ></i>
                      {{ course.type }}
                    </span>
                  </div>
                </div>
                <div class="card-body d-flex flex-column">
                  <h6 class="card-title fw-bold">{{ course.title }}</h6>
                  <p class="card-text text-muted small flex-grow-1">
                    {{ course.description?.substring(0, 100) }}
                    {{ course.description?.length > 100 ? "..." : "" }}
                  </p>
                  <div
                    class="d-flex justify-content-between align-items-center mt-auto"
                  >
                    <span class="text-primary fw-bold"
                      >{{ formatPrice(course.price) }} تومان</span
                    >
                    <nuxt-link
                      :to="`/courses/${course.slug}`"
                      class="btn btn-sm btn-outline-primary"
                    >
                      مشاهده
                    </nuxt-link>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Load More Button -->
          <div
            v-if="visibleCount < filteredCourses.length || hasMoreCourses"
            class="text-center mt-4"
          >
            <button
              @click="loadMoreCourses"
              class="btn btn-outline-primary"
              :disabled="coursesLoading"
            >
              <span
                v-if="coursesLoading"
                class="spinner-border spinner-border-sm me-2"
              ></span>
              مشاهده بیشتر
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";

// Props passed from parent
const props = defineProps({
  organization: Object,
  courses: Array,
  coursesLoading: Boolean,
  visibleCourses: Array,
  filteredCourses: Array,
  visibleCount: Number,
  hasMoreCourses: Boolean,
  getMediaUrl: Function,
  getCourseTypeBadgeClass: Function,
  getCourseTypeIcon: Function,
  formatPrice: Function,
  loadMoreCourses: Function,
});
</script>

<style scoped>
/* Header Section */
.header {
  padding-top: 150px !important;
}

.bg-dark-subtle {
  background-color: rgba(43, 45, 66, 1) !important;
}

.text-primary {
  color: #ff6b35 !important;
}

/* Button Styles */
.btn-primary {
  background-color: #ff6b35;
  border-color: #ff6b35;
}

.btn-primary:hover {
  background-color: #ff8c42;
  border-color: #ff7a2e;
}

.btn-outline-primary {
  color: #ff6b35;
  border-color: #ff6b35;
}

.btn-outline-primary:hover {
  background-color: #ff6b35;
  border-color: #ff6b35;
  color: #ffffff !important;
}

.border-primary {
  border-color: #ff6b35 !important;
}

.badge.bg-primary {
  background-color: #ff6b35 !important;
}

/* Card Styles */
.card {
  transition: transform 0.2s ease-in-out;
}

.card:hover {
  transform: translateY(-2px);
}

/* Icon Styles */
.icon {
  font-size: 1.1rem;
}

/* Category Styles */
.category-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  padding: 15px;
  border-radius: 15px;
  min-width: 120px;
  max-width: 150px;
}

.category-item:hover {
  transform: translateY(-5px);
  background-color: #f8f9fa;
}

.category-item.active {
  background-color: #fff5f0;
  border: 2px solid #ff6b35;
}

.category-icon {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background-color: #f8f9fa;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 10px;
  overflow: hidden;
  border: 3px solid #e9ecef;
  transition: all 0.3s ease;
}

.category-item:hover .category-icon {
  border-color: #ff6b35;
  transform: scale(1.05);
}

.category-item.active .category-icon {
  border-color: #ff6b35;
  background-color: #fff;
}

.category-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.category-placeholder-icon {
  font-size: 2.5rem;
  color: #6c757d;
}

.category-item.active .category-placeholder-icon {
  color: #ff6b35;
}

.category-label {
  font-size: 0.9rem;
  font-weight: 600;
  color: #495057;
  text-align: center;
  line-height: 1.3;
  margin-top: 5px;
}

.category-item.active .category-label {
  color: #ff6b35;
  font-weight: 700;
}

/* Media Queries for Mobile */
@media (max-width: 768px) {
  .header {
    padding-top: 100px !important;
  }

  .d-flex {
    flex-direction: column;
    text-align: center;
  }

  .d-flex img {
    margin-bottom: 1rem;
  }

  .category-item {
    min-width: 100px;
    max-width: 120px;
    padding: 10px;
  }

  .category-icon {
    width: 80px;
    height: 80px;
  }

  .category-label {
    font-size: 0.8rem;
  }
}

/* Mobile Categories Menu */
.custom-category-menu-container {
  display: flex;
  overflow-x: auto;
  padding: 0.5rem 0;
  gap: 1rem;
  margin-top: -8px;
  margin-bottom: 18px;
}

.custom-category-item {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 0.15rem 1.2rem;
  border-radius: 9999px;
  cursor: pointer;
  transition: all 0.3s ease;
  max-width: 150px;
  min-width: 120px;
}

.custom-category-item:hover {
  background-color: #f1f1f1;
}

.custom-active {
  background-color: #ff6b35;
  color: white;
}

.custom-category-item:not(.custom-active) {
  background-color: #f8f9fa;
  color: #495057;
}

.custom-category-text {
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  word-wrap: break-word;
  word-break: break-word;
  white-space: normal;
  max-height: 4rem;
}

/* Course Type Badge Styles */
.custom-badge {
  display: inline-flex;
  align-items: center;
  padding: 0.25rem 0.5rem;
  border-radius: 9999px;
  width: fit-content;
  max-width: 100%;
  white-space: nowrap;
}

.custom-badge i {
  margin-right: 0.25rem;
}
</style>
