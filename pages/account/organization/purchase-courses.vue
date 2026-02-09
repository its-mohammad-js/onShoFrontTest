<template>
  <div class="container py-5">
    <!-- Header -->
    <div class="row mb-4">
      <div class="col-12">
        <h2 class="text-dark fw-bold mb-3">
          <i class="icon icon-filled-shopping-cart text-danger me-2"></i>
          خرید دوره برای سازمان
        </h2>
        <p class="text-muted">دوره‌های آموزشی را با تعداد دلخواه خریداری کنید و کد دریافت کنید</p>
      </div>
    </div>

    <!-- Organization Selection/Info -->
    <div class="card border-0 shadow-sm mb-4" v-if="!organization">
      <div class="card-body">
        <h5 class="mb-3">انتخاب یا ثبت سازمان</h5>
        <div class="mb-3">
          <label class="form-label">نام سازمان</label>
          <input 
            type="text" 
            class="form-control" 
            v-model="organizationName"
            placeholder="نام سازمان خود را وارد کنید"
          />
        </div>
        <button class="btn btn-primary" @click="registerOrganization">
          ثبت سازمان
        </button>
      </div>
    </div>

    <!-- Courses List -->
    <div v-if="organization">
      <!-- Search and Filters -->
      <div class="card border-0 shadow-sm mb-4">
        <div class="card-body">
          <div class="row">
            <div class="col-md-6 mb-3">
              <input 
                type="text" 
                class="form-control" 
                v-model="searchQuery"
                placeholder="جستجوی دوره..."
                @input="loadCourses"
              />
            </div>
            <div class="col-md-6">
              <select class="form-control" v-model="selectedCategory" @change="loadCourses">
                <option value="">همه دسته‌بندی‌ها</option>
                <option v-for="cat in categories" :key="cat.id" :value="cat.id">
                  {{ cat.title }}
                </option>
              </select>
            </div>
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">در حال بارگذاری...</span>
        </div>
      </div>

      <!-- Courses Grid -->
      <div v-else class="row">
        <div 
          v-for="course in courses" 
          :key="course.id"
          class="col-md-6 col-lg-4 mb-4"
        >
          <div class="card border-0 shadow-sm h-100">
            <img 
              :src="course.image || '/images/courses/1.png'" 
              class="card-img-top"
              style="height: 200px; object-fit: cover;"
              :alt="course.title"
            />
            <div class="card-body d-flex flex-column">
              <h5 class="card-title">{{ course.title }}</h5>
              <p class="card-text text-muted flex-grow-1">{{ course.description || 'بدون توضیحات' }}</p>
              <div class="mb-3">
                <span class="fw-bold text-danger fs-5">{{ formatPrice(course.price) }} تومان</span>
              </div>
              
              <!-- Quantity Selection -->
              <div class="mb-3">
                <label class="form-label small">تعداد</label>
                <div class="input-group">
                  <button 
                    class="btn btn-outline-secondary" 
                    @click="decreaseQuantity(course.id)"
                    :disabled="getQuantity(course.id) <= 1"
                  >
                    -
                  </button>
                  <input 
                    type="number" 
                    class="form-control text-center" 
                    v-model.number="quantities[course.id]"
                    min="1"
                    @input="updateQuantity(course.id, $event.target.value)"
                  />
                  <button 
                    class="btn btn-outline-secondary" 
                    @click="increaseQuantity(course.id)"
                  >
                    +
                  </button>
                </div>
              </div>

              <!-- Add to Cart Button -->
              <button 
                class="btn btn-danger w-100"
                @click="addToCart(course)"
                :disabled="getQuantity(course.id) < 1"
              >
                <i class="icon icon-filled-shopping-cart me-2"></i>
                افزودن به سبد خرید
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="!loading && courses.length === 0" class="text-center py-5">
        <i class="icon icon-filled-box text-muted" style="font-size: 4rem;"></i>
        <p class="text-muted mt-3">دوره‌ای یافت نشد</p>
      </div>

      <!-- Pagination -->
      <div v-if="totalPages > 1" class="d-flex justify-content-center mt-4">
        <nav>
          <ul class="pagination">
            <li class="page-item" :class="{ disabled: currentPage === 1 }">
              <button class="page-link" @click="goToPage(currentPage - 1)" :disabled="currentPage === 1">
                قبلی
              </button>
            </li>
            <li 
              v-for="page in getPageNumbers()" 
              :key="page"
              class="page-item"
              :class="{ active: page === currentPage }"
            >
              <button class="page-link" @click="goToPage(page)">{{ page }}</button>
            </li>
            <li class="page-item" :class="{ disabled: currentPage === totalPages }">
              <button class="page-link" @click="goToPage(currentPage + 1)" :disabled="currentPage === totalPages">
                بعدی
              </button>
            </li>
          </ul>
        </nav>
      </div>
    </div>

    <!-- Cart Summary (Fixed Bottom) -->
    <div 
      v-if="cartItems.length > 0"
      class="position-fixed bottom-0 start-0 end-0 bg-white border-top shadow-lg p-3"
      style="z-index: 1000;"
    >
      <div class="container">
        <div class="row align-items-center">
          <div class="col-md-6">
            <span class="fw-bold">تعداد آیتم‌ها: {{ cartItems.length }}</span>
            <span class="ms-3 fw-bold text-danger">
              مجموع: {{ formatPrice(totalPrice) }} تومان
            </span>
          </div>
          <div class="col-md-6 text-end">
            <button class="btn btn-danger me-2" @click="goToCheckout">
              <i class="icon icon-filled-shopping-cart me-2"></i>
              ادامه به پرداخت
            </button>
            <button class="btn btn-outline-secondary" @click="clearCart">
              پاک کردن سبد
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'

definePageMeta({
  layout: 'account',
  middleware: 'auth'
})

const router = useRouter()
const { $api, $sweetalert } = useNuxtApp()
const token = useCookie("token").value

// Data
const organization = ref(null)
const organizationName = ref('')
const courses = ref([])
const categories = ref([])
const loading = ref(false)
const searchQuery = ref('')
const selectedCategory = ref('')
const currentPage = ref(1)
const totalPages = ref(1)
const pageSize = ref(12)

// Cart for organization purchase
const cartItems = ref([])
const quantities = reactive({})

// Computed
const totalPrice = computed(() => {
  return cartItems.value.reduce((sum, item) => {
    return sum + (item.price * item.quantity)
  }, 0)
})

// Methods
const formatPrice = (value) => {
  return value ? value.toLocaleString('fa-IR') : '۰'
}

const getQuantity = (courseId) => {
  return quantities[courseId] || 1
}

const increaseQuantity = (courseId) => {
  if (!quantities[courseId]) {
    quantities[courseId] = 1
  }
  quantities[courseId]++
}

const decreaseQuantity = (courseId) => {
  if (quantities[courseId] > 1) {
    quantities[courseId]--
  }
}

const updateQuantity = (courseId, value) => {
  const numValue = parseInt(value) || 1
  quantities[courseId] = Math.max(1, numValue)
}

const addToCart = (course) => {
  const quantity = getQuantity(course.id)
  const existingIndex = cartItems.value.findIndex(item => item.id === course.id)
  
  if (existingIndex >= 0) {
    cartItems.value[existingIndex].quantity += quantity
  } else {
    cartItems.value.push({
      id: course.id,
      title: course.title,
      price: course.price,
      image: course.image,
      quantity: quantity
    })
  }
  
  $sweetalert.success(`دوره به سبد خرید اضافه شد (${quantity} عدد)`)
}

const clearCart = () => {
  cartItems.value = []
  $sweetalert.success('سبد خرید پاک شد')
}

const goToCheckout = () => {
  // Save cart to session storage for checkout page
  sessionStorage.setItem('orgCart', JSON.stringify(cartItems.value))
  router.push('/account/organization/checkout')
}

const registerOrganization = async () => {
  if (!organizationName.value.trim()) {
    $sweetalert.error('لطفاً نام سازمان را وارد کنید')
    return
  }

  try {
    loading.value = true
    const response = await $api.post('/course/organization/create', {
      name: organizationName.value
    }, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })

    if (response.data.status) {
      organization.value = response.data.data
      $sweetalert.success('سازمان با موفقیت ثبت شد')
      await loadOrganization()
    }
  } catch (error) {
    console.error('Error registering organization:', error)
    $sweetalert.error('خطا در ثبت سازمان')
  } finally {
    loading.value = false
  }
}

const loadOrganization = async () => {
  try {
    const response = await $api.post('/course/organization/detail', {}, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })

    if (response.data.status && response.data.data) {
      organization.value = response.data.data
    }
  } catch (error) {
    console.error('Error loading organization:', error)
  }
}

const loadCategories = async () => {
  try {
    const response = await $api.post('/course/category/list', {})
    if (response.data.status) {
      categories.value = response.data.data
    }
  } catch (error) {
    console.error('Error loading categories:', error)
  }
}

const loadCourses = async (page = 1) => {
  loading.value = true
  try {
    const requestData = {
      search: searchQuery.value || null,
      category_id: selectedCategory.value || null,
      page: page,
      page_size: pageSize.value
    }

    const response = await $api.post('/payment/courses', requestData, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    
    if (response.data.status) {
      // Handle different response structures
      const data = response.data.data
      courses.value = data.data || data.courses || data || []
      currentPage.value = page
      const totalCount = data.count || courses.value.length
      totalPages.value = Math.ceil(totalCount / pageSize.value)
    }
  } catch (error) {
    console.error('Error loading courses:', error)
    $sweetalert.error('خطا در بارگذاری دوره‌ها')
  } finally {
    loading.value = false
  }
}

const goToPage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    loadCourses(page)
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
}

const getPageNumbers = () => {
  const pages = []
  const maxVisible = 5
  let start = Math.max(1, currentPage.value - Math.floor(maxVisible / 2))
  let end = Math.min(totalPages.value, start + maxVisible - 1)
  
  if (end - start + 1 < maxVisible) {
    start = Math.max(1, end - maxVisible + 1)
  }
  
  for (let i = start; i <= end; i++) {
    pages.push(i)
  }
  
  return pages
}

onMounted(async () => {
  await Promise.all([
    loadOrganization(),
    loadCategories(),
    loadCourses()
  ])
})
</script>

<style scoped>
.page-link {
  color: #c1121f;
  border: 1px solid #dee2e6;
}

.page-item.active .page-link {
  background-color: #c1121f;
  border-color: #c1121f;
  color: #fff;
}

.page-link:hover {
  color: #fff;
  background-color: #c1121f;
  border-color: #c1121f;
}
</style>

