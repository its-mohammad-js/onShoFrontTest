<template>
  <div class="d-flex justify-content-start flex-column rounded-3 py-3">
    <!-- دکمه بازگشت اگر در صفحه children هستیم -->
    <a
      v-if="selectedCategory"
      class="mt-1 mb-3 cursor-pointer d-block text-danger1"
      @click="resetCategories"
    >
      <i class="icon icon-regular-angle-right"></i>
      {{ getParentCategoryTitle() }}
    </a>

    <!-- نمایش دسته‌بندی‌های فیلتر شده (اصلی یا children) -->
    <div v-if="filteredCategories.length > 0" class="nav-custom">
      <a
        v-if="!parentCategory"
        class="cursor-pointer"
        :class="{ active: selectedCategory === null }"
        @click="resetCategories"
      >
        همه
      </a>

      <a
        v-else
        class="cursor-pointer"
        :class="{ active: selectedCategory === null }"
        @click="resetToMainCategory"
      >
        همه
      </a>

      <a
        v-for="(category, index) in filteredCategories"
        :key="index"
        class="cursor-pointer"
        :class="{ active: selectedCategory === category.id }"
        @click="selectCategory(category)"
      >
        <img :src="category.logo" alt="" class="w-20-px" />
        {{ category.title }}
      </a>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";
import { useRoute, useRouter } from "vue-router";

// Props برای دریافت داده‌ها
const props = defineProps({
  categories: {
    type: Array,
    required: true,
  },
  selectedCategory: {
    type: [String, Number],
    required: false,
  },
  parentCategory: {
    type: Object,
    required: false,
  },
});

// Router و route
const route = useRoute();
const router = useRouter();

// محاسبه دسته‌بندی‌های فیلتر شده
const filteredCategories = computed(() => {
  if (props.parentCategory?.children?.length) {
    return props.parentCategory.children;
  }
  return props.selectedCategory ? [] : props.categories;
});

// عنوان دسته‌بندی والد
const getParentCategoryTitle = () => {
  const parentCategory = props.categories.find((category) =>
    category.children?.some((child) => child.id === props.selectedCategory),
  );
  return parentCategory ? `بازگشت به ${parentCategory.title}` : "بازگشت";
};

// انتخاب دسته‌بندی
const selectCategory = (category) => {
  router.push({ path: "/courses", query: { category: category.id } });
};

// ریست کردن دسته‌بندی‌ها
const resetCategories = () => {
  router.push("/courses");
};

// ریست کردن به دسته‌بندی اصلی
const resetToMainCategory = () => {
  router.push("/courses");
};
</script>

<style scoped>
.nav-custom a {
  display: flex;
  align-items: center;
  gap: 10px;
}

.nav-custom .active {
  font-weight: bold;
  color: #d9534f;
}

.w-20-px {
  width: 20px;
}
</style>
