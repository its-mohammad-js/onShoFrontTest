<template>
  <div class="container py-5">
    <div class="row justify-content-center">
      <div class="col-lg-6">
        <!-- Header -->
        <div class="text-center mb-4">
          <h2 class="text-dark fw-bold mb-3">
            <i class="icon icon-filled-ticket text-danger me-2"></i>
            استفاده از کد دسترسی
          </h2>
          <p class="text-muted">کد دسترسی خود را وارد کنید تا دوره مربوطه برای شما فعال شود</p>
        </div>

        <!-- Code Input Card -->
        <div class="card border-0 shadow-sm mb-4">
          <div class="card-body p-4">
            <div class="mb-4">
              <label class="form-label fw-bold">کد دسترسی</label>
              <div class="input-group input-group-lg">
                <input 
                  type="text" 
                  class="form-control text-center"
                  v-model="code"
                  placeholder="کد دسترسی را وارد کنید"
                  @keyup.enter="redeemCode"
                  :disabled="processing"
                />
                <button 
                  class="btn btn-danger"
                  @click="redeemCode"
                  :disabled="!code.trim() || processing"
                >
                  <span v-if="processing">
                    <span class="spinner-border spinner-border-sm me-2"></span>
                    در حال بررسی...
                  </span>
                  <span v-else>
                    فعال‌سازی
                  </span>
                </button>
              </div>
            </div>

            <!-- Info Box -->
            <div class="alert alert-info mb-0">
              <i class="icon icon-filled-info-circle me-2"></i>
              <small>
                پس از وارد کردن کد، دوره مربوطه به صورت خودکار برای شما فعال می‌شود و یک اعتبار از کد کسر می‌گردد.
                <br>
                <strong>نکته:</strong> دوره‌های فعال شده در صفحه <nuxt-link to="/account/courses" class="alert-link">دوره‌های من</nuxt-link> نمایش داده می‌شوند.
              </small>
            </div>
          </div>
        </div>


        <!-- Redeemed Courses History -->
        <div class="card border-0 shadow-sm">
          <div class="card-header bg-light">
            <h5 class="mb-0">دوره‌های فعال شده با کد</h5>
          </div>
          <div class="card-body">
            <div v-if="redeemedCoursesLoading" class="text-center py-3">
              <div class="spinner-border spinner-border-sm text-primary"></div>
            </div>
            <div v-else-if="redeemedCourses.length === 0" class="text-center py-3">
              <p class="text-muted mb-0">هنوز دوره‌ای با کد فعال نشده است</p>
            </div>
            <div v-else>
              <div 
                v-for="course in redeemedCourses" 
                :key="course.id"
                class="d-flex align-items-center border-bottom pb-3 mb-3"
              >
                <img 
                  :src="course.image || '/images/courses/1.png'" 
                  class="rounded me-3"
                  style="width: 80px; height: 80px; object-fit: cover;"
                  :alt="course.title"
                />
                <div class="flex-grow-1">
                  <h6 class="mb-1">{{ course.title }}</h6>
                  <p class="text-muted small mb-0">
                    فعال شده در: {{ formatDate(course.redeemed_at) }}
                  </p>
                </div>
                <button 
                  class="btn btn-sm btn-primary"
                  @click="goToCourse(course.slug)"
                >
                  مشاهده دوره
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

definePageMeta({
  layout: 'account',
  middleware: 'auth'
})

const router = useRouter()
const { $api, $sweetalert } = useNuxtApp()
const token = useCookie("token").value

// Data
const code = ref('')
const processing = ref(false)
const redeemedCourses = ref([])
const redeemedCoursesLoading = ref(false)

// Methods
const formatDate = (dateString) => {
  if (!dateString) return 'نامشخص'
  const date = new Date(dateString)
  return date.toLocaleDateString('fa-IR')
}

const redeemCode = async () => {
  if (!code.value.trim()) {
    $sweetalert.error('لطفاً کد دسترسی را وارد کنید')
    return
  }

  // Since there's no validate endpoint, proceed directly to redemption
  await confirmRedeem()
}

const confirmRedeem = async () => {
  if (!code.value.trim()) {
    $sweetalert.error('لطفاً کد دسترسی را وارد کنید')
    return
  }

  processing.value = true
  try {
    const response = await $api.post('/payment/code/redeem', {
      code: code.value.trim()
    }, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })

    if (response.data.status) {
      const data = response.data.data
      
      // Show success message with course details
      $sweetalert.fire({
        title: 'موفق!',
        html: `
          <p class="mb-2">${data.message || 'دوره با موفقیت برای شما فعال شد!'}</p>
          <p class="mb-2"><strong>دوره:</strong> ${data.course?.title || 'نامشخص'}</p>
          <p class="mb-2"><strong>کد:</strong> <code>${data.code}</code></p>
          <p class="mb-0"><strong>اعتبار باقیمانده:</strong> ${data.remaining_credits || 0}</p>
        `,
        icon: 'success',
        confirmButtonText: 'مشاهده دوره',
        cancelButtonText: 'بستن',
        showCancelButton: true
      }).then((result) => {
        // Reset form
        code.value = ''
        
        // Reload redeemed courses
        loadRedeemedCourses()
        
        // Note: The course should appear in your course list at /account/courses
        // If it doesn't appear immediately, please refresh the page
        
        // Redirect to course if user clicked confirm
        if (result.isConfirmed && data.course?.id) {
          // Try to get course slug, or use ID
          router.push(`/courses/${data.course.id}`)
        }
      })
    } else {
      // Handle specific error messages
      // Response structure: {"status":false,"data":{"error":"You are already enrolled in this course"}}
      const errorData = response.data.data || {}
      const errorMessage = errorData.error || response.data.message || 'خطا در فعال‌سازی دوره'
      
      console.log('Error response:', response.data)
      console.log('Error data:', errorData)
      console.log('Error message:', errorMessage)
      
      // Check if user is already enrolled - check the exact error message
      // The error message is: "You are already enrolled in this course"
      const isAlreadyEnrolled = errorMessage && (
          errorMessage.toLowerCase().includes('already enrolled') || 
          errorMessage.toLowerCase().includes('already enrolled in this course') ||
          errorMessage === 'You are already enrolled in this course'
      )
      
      console.log('Is already enrolled?', isAlreadyEnrolled, 'Error message:', errorMessage)
      
      if (isAlreadyEnrolled) {
        $sweetalert.fire({
          icon: 'warning',
          title: 'توجه',
          text: 'این کد قبلا برای شما فعال شده',
          confirmButtonText: 'باشه'
        })
      } else {
        $sweetalert.error(errorMessage)
      }
    }
  } catch (error) {
    console.error('Error redeeming code:', error)
    console.error('Error response:', error.response?.data)
    
    // Handle error response
    // Response structure: {"status":false,"data":{"error":"You are already enrolled in this course"}}
    const errorResponse = error.response?.data
    if (errorResponse) {
      const errorData = errorResponse.data || {}
      const errorMessage = errorData.error || errorResponse.message || 'خطا در فعال‌سازی دوره'
      
      console.log('Error response from catch:', errorResponse)
      console.log('Error data from catch:', errorData)
      console.log('Error message from catch:', errorMessage)
      
      // Check if user is already enrolled - check the exact error message
      // The error message is: "You are already enrolled in this course"
      const isAlreadyEnrolled = errorMessage && (
          errorMessage.toLowerCase().includes('already enrolled') || 
          errorMessage.toLowerCase().includes('already enrolled in this course') ||
          errorMessage === 'You are already enrolled in this course'
      )
      
      console.log('Is already enrolled (catch)?', isAlreadyEnrolled, 'Error message:', errorMessage)
      
      if (isAlreadyEnrolled) {
        $sweetalert.fire({
          icon: 'warning',
          title: 'توجه',
          text: 'این کد قبلا برای شما فعال شده',
          confirmButtonText: 'باشه'
        })
      } else {
        $sweetalert.error(errorMessage)
      }
    } else {
      $sweetalert.error('خطا در فعال‌سازی دوره')
    }
  } finally {
    processing.value = false
  }
}

const loadRedeemedCourses = async () => {
  redeemedCoursesLoading.value = true
  try {
    // Try to load redeemed courses (optional endpoint)
    const response = await $api.post('/payment/code/redeemed-courses', {}, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })

    if (response.data.status) {
      redeemedCourses.value = response.data.data || []
    }
  } catch (error) {
    // If endpoint doesn't exist, silently fail (optional feature)
    console.log('Redeemed courses endpoint not available')
    redeemedCourses.value = []
  } finally {
    redeemedCoursesLoading.value = false
  }
}

const goToCourse = (slug) => {
  if (slug) {
    router.push(`/courses/${slug}`)
  }
}

onMounted(() => {
  loadRedeemedCourses()
})
</script>

<style scoped>
.input-group-lg .form-control {
  font-size: 1.25rem;
}
</style>

