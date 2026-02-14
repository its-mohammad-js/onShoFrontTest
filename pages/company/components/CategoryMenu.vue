<template>
  <div>
    <!-- Categories (Desktop) Section -->
    <div v-if="categories.length > 0" class="row mb-5 d-none d-md-block">
      <div class="col-12">
        <div class="text-center mb-4">
          <h3 class="fw-bold">دسته‌بندی‌ها</h3>
        </div>
        <div class="d-flex flex-wrap justify-content-center gap-4 mb-4">
          <div
            v-for="category in categories"
            :key="category.id"
            class="category-item"
            :class="{ active: selectedCategoryId === category.id }"
            @click="selectCategory(category.id)"
          >
            <div class="category-icon">
              <img
                v-if="category.logo"
                :src="getMediaUrl(category.logo)"
                :alt="category.title"
                class="category-image"
              />
              <i
                v-else
                class="icon icon-filled-folder category-placeholder-icon"
              ></i>
            </div>
            <span class="category-label">{{ category.title }}</span>
          </div>
        </div>
        <div v-if="selectedCategoryId" class="text-center mt-3">
          <button @click="clearCategoryFilter" class="btn btn-outline-primary">
            <i class="icon icon-filled-close me-2"></i>
            حذف فیلتر
          </button>
        </div>
      </div>
    </div>

    <!-- Categories (Mobile) Section -->
    <div
      v-if="categories.length > 0"
      class="custom-category-menu-container d-md-none"
    >
      <div
        class="custom-category-item"
        :class="selectedCategoryId === null ? 'custom-active' : ''"
        @click="clearCategoryFilter"
      >
        <p class="custom-category-text">همه</p>
      </div>

      <div
        v-for="category in categories"
        :key="category.id"
        class="custom-category-item"
        :class="selectedCategoryId === category.id ? 'custom-active' : ''"
        @click="selectCategory(category.id)"
      >
        <p class="custom-category-text">
          {{ category.title }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, defineProps, defineEmits } from "vue";

// Props from parent component
const { categories, selectedCategoryId, getMediaUrl } = defineProps({
  categories: Array,
  selectedCategoryId: Number,
  getMediaUrl: Function,
});

// Emit events to parent component
const emit = defineEmits(["selectCategory", "clearCategoryFilter"]);

// Methods for selecting and clearing category filter
const selectCategory = (categoryId) => {
  emit("selectCategory", categoryId);
};

const clearCategoryFilter = () => {
  emit("clearCategoryFilter");
};
</script>

<style scoped>
.header {
  padding-top: 150px !important;
}

.bg-dark-subtle {
  background-color: rgba(43, 45, 66, 1) !important;
}

.text-primary {
  color: #ff6b35 !important;
}

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

.card {
  transition: transform 0.2s ease-in-out;
}

.card:hover {
  transform: translateY(-2px);
}

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

/* mobile categories menu */
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

/* type tag (offline or online) */

.custom-badge {
  display: inline-flex; /* Ensures that the content is displayed inline */
  align-items: center; /* Centers the content vertically */
  padding: 0.25rem 0.5rem; /* Adjust padding */
  border-radius: 9999px; /* Make the badge rounded */
  width: fit-content; /* Set width to fit content */
  max-width: 100%; /* Ensure no overflow */
  white-space: nowrap; /* Prevent text from wrapping */
}

.custom-badge i {
  margin-right: 0.25rem; /* Adjust margin for icon */
}
</style>
