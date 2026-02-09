<template>
  <div class="coursera-menu">
    <!-- Main Container -->
    <div class="menu-wrapper shadow-lg">
      <!-- Level 1: Main Categories -->
      <div class="panel level-1">
        <ul class="list-unstyled mb-0">
          <li
            v-for="cat in displayedLevel1Items"
            :key="cat.id"
            class="menu-item"
            :class="{ active: selectedCategory?.id === cat.id }"
            @click="selectCategory(cat)"
          >
            <div class="d-flex align-items-center justify-content-between">
              <div class="d-flex align-items-center gap-3">
                <div class="icon-circle">
                  <img
                    v-if="cat.logo"
                    :src="cat.logo"
                    alt=""
                    class="icon-img"
                  />
                  <i v-else class="bi bi-bookmark"></i>
                </div>
                <span class="title">{{ cat.title }}</span>
              </div>
              <i class="bi bi-chevron-left arrow"></i>
            </div>
          </li>
        </ul>
        <button
          v-if="hasMoreLevel1"
          class="load-more-btn d-md-none"
          @click="loadMoreLevel1"
        >
          نمایش بیشتر
        </button>
      </div>

      <!-- Level 2: Subcategories -->
      <div v-if="selectedCategory" class="panel level-2">
        <div class="panel-header" @click="clearLevel(1)">
          <i class="bi bi-arrow-right"></i>
          <span>{{ selectedCategory.title }}</span>
        </div>
        <ul class="list-unstyled mb-0">
          <li
            v-for="sub in displayedLevel2Items"
            :key="sub.id"
            class="menu-item"
            :class="{ active: selectedSubCategory?.id === sub.id }"
            @click="selectSubCategory(sub)"
          >
            <span class="title">{{ sub.title }}</span>
            <i v-if="sub.children?.length" class="bi bi-chevron-left arrow"></i>
          </li>
        </ul>
        <button
          v-if="hasMoreLevel2"
          class="load-more-btn d-md-none"
          @click="loadMoreLevel2"
        >
          نمایش بیشتر
        </button>
      </div>

      <!-- Level 3: Deep Subcategories -->
      <div v-if="selectedSubCategory" class="panel level-3">
        <div class="panel-header" @click="clearLevel(2)">
          <i class="bi bi-arrow-right"></i>
          <span>{{ selectedSubCategory.title }}</span>
        </div>
        <ul class="list-unstyled mb-0">
          <li
            v-for="deep in displayedLevel3Items"
            :key="deep.id"
            class="menu-item leaf"
            @click="goToCategory(deep)"
          >
            <span class="title">{{ deep.title }}</span>
          </li>
        </ul>
        <button
          v-if="hasMoreLevel3"
          class="load-more-btn d-md-none"
          @click="loadMoreLevel3"
        >
          نمایش بیشتر
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
const emit = defineEmits(['navigate'])

const { $api } = useNuxtApp()
const router = useRouter()
const { getMediaUrl } = useMediaUrl()

const categories = ref([])
const selectedCategory = ref(null)
const selectedSubCategory = ref(null)
const loading = ref(true)

// Pagination states for mobile
const itemsPerPage = 5
const level1DisplayCount = ref(itemsPerPage)
const level2DisplayCount = ref(itemsPerPage)
const level3DisplayCount = ref(itemsPerPage)

// Check if mobile
const isMobile = computed(() => {
  if (typeof window === 'undefined') return false
  return window.innerWidth <= 576
})

// تبدیل آدرس‌های logo به آدرس با /api
const categoriesWithMediaUrl = computed(() => {
  return categories.value.map(cat => ({
    ...cat,
    logo: getMediaUrl(cat.logo),
    children: (cat.children || []).map(sub => ({
      ...sub,
      logo: getMediaUrl(sub.logo),
      children: (sub.children || []).map(deep => ({
        ...deep,
        logo: getMediaUrl(deep.logo)
      }))
    }))
  }))
})

// Displayed items for each level (with pagination on mobile)
const displayedLevel1Items = computed(() => {
  const items = categoriesWithMediaUrl.value
  if (isMobile.value) {
    return items.slice(0, level1DisplayCount.value)
  }
  return items
})

const displayedLevel2Items = computed(() => {
  if (!selectedCategory.value) return []
  const items = selectedCategory.value.children || []
  if (isMobile.value) {
    return items.slice(0, level2DisplayCount.value)
  }
  return items
})

const displayedLevel3Items = computed(() => {
  if (!selectedSubCategory.value) return []
  const items = selectedSubCategory.value.children || []
  if (isMobile.value) {
    return items.slice(0, level3DisplayCount.value)
  }
  return items
})

// Check if there are more items to load
const hasMoreLevel1 = computed(() => {
  if (!isMobile.value) return false
  return categoriesWithMediaUrl.value.length > level1DisplayCount.value
})

const hasMoreLevel2 = computed(() => {
  if (!isMobile.value || !selectedCategory.value) return false
  // Don't show "Load More" button for level 2 when level 3 is open
  if (selectedSubCategory.value) return false
  const total = (selectedCategory.value.children || []).length
  return total > level2DisplayCount.value
})

const hasMoreLevel3 = computed(() => {
  if (!isMobile.value || !selectedSubCategory.value) return false
  const total = (selectedSubCategory.value.children || []).length
  return total > level3DisplayCount.value
})

// Load more functions
const loadMoreLevel1 = () => {
  level1DisplayCount.value += itemsPerPage
}

const loadMoreLevel2 = () => {
  level2DisplayCount.value += itemsPerPage
}

const loadMoreLevel3 = () => {
  level3DisplayCount.value += itemsPerPage
}

function normalize(items) {
  return (items || []).map(item => ({
    ...item,
    children: Array.isArray(item.children)
      ? item.children.map(ch => ({
          ...ch,
          children: Array.isArray(ch.children) ? ch.children : []
        }))
      : []
  }))
}

onMounted(async () => {
  try {
    loading.value = true
    const res = await $api.post('/course/category/list', {})
    const data = res?.data?.data ?? res?.data ?? []
    categories.value = normalize(data)
  } catch (err) {
    console.error('خطا:', err)
  } finally {
    loading.value = false
  }
})

const selectCategory = (cat) => {
  selectedSubCategory.value = null
  // Reset level 2 pagination when selecting new category
  if (isMobile.value) {
    level2DisplayCount.value = itemsPerPage
  }
  // پیدا کردن category اصلی از categories (بدون media url)
  const originalCat = categories.value.find(c => c.id === cat.id) || cat
  if (originalCat.children?.length) {
    selectedCategory.value = originalCat
  } else {
    goToCategory(originalCat)
  }
}

const selectSubCategory = (cat) => {
  // Reset level 3 pagination when selecting new subcategory
  if (isMobile.value) {
    level3DisplayCount.value = itemsPerPage
  }
  // پیدا کردن subcategory اصلی
  const parent = categories.value.find(c => c.id === selectedCategory.value?.id)
  const originalSub = parent?.children?.find(c => c.id === cat.id) || cat
  if (originalSub.children?.length) {
    selectedSubCategory.value = originalSub
  } else {
    goToCategory(originalSub)
  }
}

const goToCategory = (cat) => {
  // اطلاع به والد (هدر) که روی یک دسته‌بندی کلیک شده تا منو را ببندد
  emit('navigate')
  router.push({ path: '/courses', query: { category: cat.id } })
}

const clearLevel = (level) => {
  if (level === 1) {
    selectedCategory.value = null
    selectedSubCategory.value = null
    // Reset pagination when going back
    if (isMobile.value) {
      level2DisplayCount.value = itemsPerPage
      level3DisplayCount.value = itemsPerPage
    }
  } else if (level === 2) {
    selectedSubCategory.value = null
    // Reset level 3 pagination when going back
    if (isMobile.value) {
      level3DisplayCount.value = itemsPerPage
    }
  }
}
</script>
<style scoped>
.coursera-menu {
  direction: rtl;
}

.menu-wrapper {
  display: flex;
  width: 720px;
  max-width: 100%;
  height: 460px;
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 20px 40px rgba(0,0,0,0.12);
}

.panel {
  width: 240px;
  border-left: 1px solid #e0e0e0;
  background: #fff;
  transition: all 0.3s ease;
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
}

.panel:first-child {
  border-left: none;
}

.level-2 { background: #f8f9fa; }
.level-3 { background: #f1f3f5; }

.panel-header {
  padding: 16px 20px;
  font-weight: 600;
  color: #28a745;
  cursor: pointer;
  border-bottom: 1px solid #e0e0e0;
  font-size: 15px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.panel-header:hover {
  background: rgba(40, 167, 69, 0.05);
}

.menu-item {
  padding: 12px 20px;
  cursor: pointer;
  transition: all 0.2s ease;
  border-bottom: 1px solid transparent;
}

.menu-item:hover {
  background: rgba(40, 167, 69, 0.05);
}

.menu-item.active {
  background: #28a745;
  color: white;
}

.menu-item.active .arrow {
  filter: brightness(0) invert(1);
}

.menu-item.leaf:hover {
  background: rgba(0,0,0,0.05);
}

.title {
  font-size: 14px;
  font-weight: 500;
  line-height: 1.4;
}

.icon-circle {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: rgba(40, 167, 69, 0.08);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  flex-shrink: 0;
}

.icon-img {
  width: 20px;
  height: 20px;
  object-fit: contain;
}

.arrow {
  font-size: 12px;
  color: #666;
  transition: transform 0.2s;
}

.menu-item:hover .arrow {
  transform: translateX(4px);
}

/* RTL Arrow Fix */
.bi-chevron-left {
  transform: rotate(180deg);
}
.bi-arrow-right {
  transform: rotate(180deg);
}

/* Responsive: Stack panels vertically on small screens */
@media (max-width: 576px) {
  .menu-wrapper {
    width: 100%;
    height: auto;
    max-height: 90vh;
    display: block;
    overflow: auto;
    -webkit-overflow-scrolling: touch;
  }
  .panel {
    width: 100%;
    border-left: none;
    border-bottom: 1px solid #e0e0e0;
    max-height: 70vh;
    overflow-y: auto;
  }
  .level-2, .level-3 {
    max-height: 70vh;
  }
  .panel-header {
    position: sticky;
    top: 0;
    background: inherit;
    z-index: 1;
    border-bottom: 1px solid #e0e0e0;
  }
  .menu-item {
    padding: 14px 16px;
  }
  .icon-circle {
    width: 32px;
    height: 32px;
  }
  .icon-img {
    width: 18px;
    height: 18px;
  }
  
  .load-more-btn {
    width: 100%;
    padding: 12px 16px;
    margin: 8px 0;
    background: #f8f9fa;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    color: #28a745;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
    text-align: center;
  }
  
  .load-more-btn:hover {
    background: rgba(40, 167, 69, 0.05);
    border-color: #28a745;
  }
  
  .load-more-btn:active {
    transform: scale(0.98);
  }
}

</style>