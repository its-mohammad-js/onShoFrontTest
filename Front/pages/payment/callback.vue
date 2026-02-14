<template>
  <div class="container my-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card">
          <div class="card-body text-center">
            <div v-if="loading" class="py-5">
              <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">در حال پردازش...</span>
              </div>
              <p class="mt-3">در حال پردازش پرداخت...</p>
            </div>
            
            <div v-else-if="paymentResult.success" class="py-5">
              <div class="text-success mb-3">
                <i class="fas fa-check-circle fa-3x"></i>
              </div>
              <h4 class="text-success">پرداخت موفق!</h4>
              <p class="text-muted">پرداخت شما با موفقیت انجام شد.</p>
              <div class="alert alert-success">
                <strong>شماره پیگیری:</strong> {{ paymentResult.data.ref_id }}
              </div>
              
              <!-- Organization Codes (if applicable) -->
              <div v-if="paymentResult.data.codes && paymentResult.data.codes.length > 0" class="alert alert-info mt-3">
                <h6 class="mb-3">
                  <i class="icon icon-filled-ticket me-2"></i>
                  کدهای دسترسی شما:
                </h6>
                <div v-for="(codeInfo, index) in paymentResult.data.codes" :key="index" class="mb-3 p-3 bg-white rounded">
                  <div class="d-flex justify-content-between align-items-center mb-2">
                    <strong>دوره:</strong>
                    <span>{{ codeInfo.course_title }}</span>
                  </div>
                  <div class="d-flex justify-content-between align-items-center mb-2">
                    <strong>کد:</strong>
                    <code class="bg-light p-2 rounded">{{ codeInfo.code }}</code>
                    <button 
                      class="btn btn-sm btn-outline-secondary ms-2"
                      @click="copyCode(codeInfo.code)"
                    >
                      <i class="icon icon-filled-copy"></i> کپی
                    </button>
                  </div>
                  <div class="d-flex justify-content-between align-items-center">
                    <strong>تعداد اعتبار:</strong>
                    <span>{{ codeInfo.credits }}</span>
                  </div>
                </div>
                <button class="btn btn-primary w-100" @click="goToCodes">
                  <i class="icon icon-filled-ticket me-2"></i>
                  مدیریت کدها
                </button>
              </div>
              
              <button class="btn btn-primary" @click="goToAccount">
                {{ paymentResult.data.codes ? 'مشاهده دوره‌ها' : 'مشاهده دوره‌ها' }}
              </button>
            </div>
            
            <div v-else class="py-5">
              <div class="text-danger mb-3">
                <i class="fas fa-times-circle fa-3x"></i>
              </div>
              <h4 class="text-danger">پرداخت ناموفق</h4>
              <p class="text-muted">{{ paymentResult.error }}</p>
              <button class="btn btn-secondary" @click="goToCheckout">تلاش مجدد</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useNuxtApp } from '#app'

const route = useRoute()
const router = useRouter()
const { $api, $sweetalert } = useNuxtApp()

const loading = ref(true)
const paymentResult = ref({ success: false, data: {}, error: '' })

onMounted(async () => {
  try {
    // Get callback parameters
    const authority = route.query.Authority
    const status = route.query.Status
    
    console.log('Payment callback received:', { authority, status })
    
    if (!authority) {
      paymentResult.value = {
        success: false,
        error: 'پارامترهای پرداخت یافت نشد.'
      }
      loading.value = false
      return
    }
    
    // Call backend to verify payment
    const response = await $api.get('/payment/callback', {
      params: {
        Authority: authority,
        Status: status
      }
    })
    
    if (response.data.status) {
      paymentResult.value = {
        success: true,
        data: response.data.data
      }
    } else {
      paymentResult.value = {
        success: false,
        error: response.data.data.error || 'خطا در پردازش پرداخت'
      }
    }
    
  } catch (error) {
    console.error('Payment callback error:', error)
    paymentResult.value = {
      success: false,
      error: 'خطا در ارتباط با سرور'
    }
  } finally {
    loading.value = false
  }
})

const goToAccount = () => {
  router.push('/account')
}

const goToCheckout = () => {
  router.push('/checkout')
}

const goToCodes = () => {
  router.push('/account/organization/codes')
}

const copyCode = (code) => {
  navigator.clipboard.writeText(code).then(() => {
    $sweetalert.success('کد کپی شد')
  }).catch(() => {
    $sweetalert.error('خطا در کپی کردن کد')
  })
}
</script>

<style scoped>
.card {
  border: none;
  box-shadow: 0 0 20px rgba(0,0,0,0.1);
}

.spinner-border {
  width: 3rem;
  height: 3rem;
}
</style>
