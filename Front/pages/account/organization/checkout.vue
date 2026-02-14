<template>
  <div class="container py-5">
    <!-- Header -->
    <div class="row mb-4">
      <div class="col-12">
        <h2 class="text-dark fw-bold mb-3">
          <i class="icon icon-filled-ticket text-danger me-2"></i>
          ایجاد کدهای دسترسی
        </h2>
        <p class="text-muted">کدهای دسترسی برای دوره‌های انتخابی ایجاد کنید</p>
      </div>
    </div>

    <div class="row">
      <!-- Cart Items -->
      <div class="col-lg-8 mb-4">
        <div class="card border-0 shadow-sm">
          <div class="card-header bg-light">
            <h5 class="mb-0">سبد خرید سازمانی</h5>
          </div>
          <div class="card-body">
            <div v-if="cartItems.length === 0" class="text-center py-5">
              <i class="icon icon-filled-box text-muted" style="font-size: 4rem;"></i>
              <p class="text-muted mt-3">سبد خرید شما خالی است</p>
              <button class="btn btn-primary" @click="goToPurchase">
                بازگشت به خرید دوره‌ها
              </button>
            </div>

            <div v-else>
              <div 
                v-for="(item, index) in cartItems" 
                :key="index"
                class="border-bottom pb-3 mb-3"
              >
                <div class="d-flex align-items-center mb-3">
                  <img 
                    :src="item.image || '/images/courses/1.png'" 
                    class="rounded me-3"
                    style="width: 100px; height: 100px; object-fit: cover;"
                    :alt="item.title"
                  />
                  <div class="flex-grow-1">
                    <h6 class="mb-1">{{ item.title }}</h6>
                    <p class="text-muted small mb-0">تعداد کد: {{ item.quantity }}</p>
                    <p class="fw-bold text-danger mb-0 mt-2">
                      {{ formatPrice(item.price * item.quantity) }} تومان
                    </p>
                  </div>
                  <button 
                    class="btn btn-sm btn-outline-danger"
                    @click="removeItem(index)"
                  >
                    <i class="icon icon-filled-trash"></i>
                  </button>
                </div>
                <!-- Credits per code input -->
                <div class="row">
                  <div class="col-md-6">
                    <label class="form-label small">تعداد اعتبار برای هر کد</label>
                    <input 
                      type="number" 
                      class="form-control"
                      v-model.number="item.credits_per_code"
                      min="1"
                      placeholder="مثلاً 3"
                    />
                    <small class="text-muted">هر کد چند بار قابل استفاده است؟</small>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Payment Summary -->
      <div class="col-lg-4">
        <div class="card border-0 shadow-sm">
          <div class="card-header bg-danger text-white">
            <h5 class="mb-0">خلاصه سفارش</h5>
          </div>
          <div class="card-body">
            <div class="d-flex justify-content-between mb-3">
              <span>تعداد دوره‌ها:</span>
              <span class="fw-bold">{{ totalItems }}</span>
            </div>
            <div class="d-flex justify-content-between mb-3">
              <span>تعداد کل:</span>
              <span class="fw-bold">{{ totalQuantity }}</span>
            </div>
            <hr>
            <div class="d-flex justify-content-between mb-3">
              <span>مبلغ کل:</span>
              <span class="fw-bold text-danger fs-5">{{ formatPrice(totalPrice) }} تومان</span>
            </div>
            <button 
              class="btn btn-danger w-100"
              @click="processPayment"
              :disabled="cartItems.length === 0 || processing"
            >
              <span v-if="processing">
                <span class="spinner-border spinner-border-sm me-2"></span>
                در حال ایجاد کدها...
              </span>
              <span v-else>
                ایجاد کدها
              </span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

definePageMeta({
  layout: 'account',
  middleware: 'auth'
})

const router = useRouter()
const { $api, $sweetalert } = useNuxtApp()
const token = useCookie("token").value

// Data
const cartItems = ref([])
const processing = ref(false)

// Computed
const totalItems = computed(() => cartItems.value.length)

const totalQuantity = computed(() => {
  return cartItems.value.reduce((sum, item) => sum + item.quantity, 0)
})

const totalPrice = computed(() => {
  return cartItems.value.reduce((sum, item) => {
    return sum + (item.price * item.quantity)
  }, 0)
})

// Methods
const formatPrice = (value) => {
  return value ? value.toLocaleString('fa-IR') : '۰'
}

const loadCart = () => {
  const savedCart = sessionStorage.getItem('orgCart')
  if (savedCart) {
    try {
      cartItems.value = JSON.parse(savedCart)
    } catch (error) {
      console.error('Error loading cart:', error)
      cartItems.value = []
    }
  }
}

const removeItem = (index) => {
  cartItems.value.splice(index, 1)
  sessionStorage.setItem('orgCart', JSON.stringify(cartItems.value))
}

const goToPurchase = () => {
  router.push('/account/organization/purchase-courses')
}

const processPayment = async () => {
  if (cartItems.value.length === 0) {
    $sweetalert.error('سبد خرید شما خالی است')
    return
  }

  // Validate credits_per_code for all items
  for (const item of cartItems.value) {
    if (!item.credits_per_code || item.credits_per_code < 1) {
      $sweetalert.error(`لطفاً تعداد اعتبار برای دوره "${item.title}" را وارد کنید`)
      return
    }
  }

  processing.value = true

  try {
    // Generate codes for each course
    const codePromises = cartItems.value.map(async (item) => {
      const response = await $api.post('/payment/code/create', {
        course_id: item.id,
        quantity: item.quantity,
        credits_per_code: item.credits_per_code
      }, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      })
      return response
    })

    const responses = await Promise.all(codePromises)
    
    // Check if all requests were successful
    const allSuccess = responses.every(res => res.data.status)
    
    if (allSuccess) {
      // Collect all generated codes
      const allCodes = []
      responses.forEach((res, index) => {
        const item = cartItems.value[index]
        if (res.data.data && res.data.data.codes) {
          res.data.data.codes.forEach(code => {
            allCodes.push({
              code: code.code || code,
              course_title: item.title,
              credits: item.credits_per_code
            })
          })
        }
      })

      // Clear cart
      cartItems.value = []
      sessionStorage.removeItem('orgCart')
      
      // Show success with codes
      $sweetalert.fire({
        title: 'کدها با موفقیت ایجاد شدند!',
        html: `
          <p>تعداد ${allCodes.length} کد ایجاد شد.</p>
          <p>می‌توانید کدها را در صفحه مدیریت کدها مشاهده کنید.</p>
        `,
        icon: 'success',
        confirmButtonText: 'مشاهده کدها'
      }).then((result) => {
        if (result.isConfirmed) {
          router.push('/account/organization/codes')
        } else {
          router.push('/account/organization/purchase-courses')
        }
      })
    } else {
      // Find first error
      const errorResponse = responses.find(res => !res.data.status)
      $sweetalert.error(errorResponse?.data?.message || 'خطا در ایجاد کدها')
    }
  } catch (error) {
    console.error('Error creating codes:', error)
    const errorMessage = error.response?.data?.message || 'خطا در ایجاد کدها'
    $sweetalert.error(errorMessage)
  } finally {
    processing.value = false
  }
}

onMounted(() => {
  loadCart()
  if (cartItems.value.length === 0) {
    // If cart is empty, redirect to purchase page
    setTimeout(() => {
      router.push('/account/organization/purchase-courses')
    }, 2000)
  }
})
</script>

<style scoped>
.card-header.bg-danger {
  background-color: #c1121f !important;
}
</style>

