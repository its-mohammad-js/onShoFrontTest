<template>
  <div class="container py-5">
    <!-- Header -->
    <div class="row mb-4">
      <div class="col-12">
        <h2 class="text-dark fw-bold mb-3">
          <i class="icon icon-filled-ticket text-danger me-2"></i>
          کدهای دسترسی سازمان
        </h2>
        <p class="text-muted">کدهای خریداری شده و وضعیت استفاده از آن‌ها</p>
      </div>
    </div>

    <!-- Stats Cards -->
    <div class="row mb-4">
      <div class="col-md-4 mb-3">
        <div class="card border-0 shadow-sm bg-primary text-white">
          <div class="card-body">
            <h6 class="text-white-50 mb-2">کل کدها</h6>
            <h3 class="mb-0">{{ stats.totalCodes }}</h3>
          </div>
        </div>
      </div>
      <div class="col-md-4 mb-3">
        <div class="card border-0 shadow-sm bg-success text-white">
          <div class="card-body">
            <h6 class="text-white-50 mb-2">کدهای فعال</h6>
            <h3 class="mb-0">{{ stats.activeCodes }}</h3>
          </div>
        </div>
      </div>
      <div class="col-md-4 mb-3">
        <div class="card border-0 shadow-sm bg-warning text-white">
          <div class="card-body">
            <h6 class="text-white-50 mb-2">کدهای استفاده شده</h6>
            <h3 class="mb-0">{{ stats.usedCodes }}</h3>
          </div>
        </div>
      </div>
    </div>

    <!-- Filters -->
    <div class="card border-0 shadow-sm mb-4">
      <div class="card-body">
        <div class="row">
          <div class="col-md-4 mb-3">
            <input 
              type="text" 
              class="form-control" 
              v-model="searchQuery"
              placeholder="جستجوی کد..."
              @input="loadCodes"
            />
          </div>
          <div class="col-md-4 mb-3">
            <select class="form-control" v-model="statusFilter" @change="loadCodes">
              <option value="">همه وضعیت‌ها</option>
              <option value="active">فعال</option>
              <option value="used">استفاده شده</option>
              <option value="expired">منقضی شده</option>
            </select>
          </div>
          <div class="col-md-4 mb-3">
            <select class="form-control" v-model="courseFilter" @change="loadCodes">
              <option value="">همه دوره‌ها</option>
              <option v-for="course in courses" :key="course.id" :value="course.id">
                {{ course.title }}
              </option>
            </select>
          </div>
        </div>
      </div>
    </div>

    <!-- Codes List -->
    <div class="card border-0 shadow-sm">
      <div class="card-body">
        <div v-if="loading" class="text-center py-5">
          <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">در حال بارگذاری...</span>
          </div>
        </div>

        <div v-else-if="codes.length === 0" class="text-center py-5">
          <i class="icon icon-filled-ticket text-muted" style="font-size: 4rem;"></i>
          <p class="text-muted mt-3">کدی یافت نشد</p>
        </div>

        <div v-else>
          <div class="table-responsive">
            <table class="table">
              <thead>
                <tr>
                  <th>کد</th>
                  <th>دوره</th>
                  <th>تعداد اعتبار</th>
                  <th>اعتبار باقیمانده</th>
                  <th>وضعیت</th>
                  <th>تاریخ خرید</th>
                  <th>عملیات</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="code in codes" :key="code.id">
                  <td>
                    <code class="bg-light p-2 rounded">{{ code.code }}</code>
                    <button 
                      class="btn btn-sm btn-outline-secondary ms-2"
                      @click="copyCode(code.code)"
                      title="کپی کد"
                    >
                      <i class="icon icon-filled-copy"></i>
                    </button>
                  </td>
                  <td>{{ code.course?.title || 'نامشخص' }}</td>
                  <td>{{ code.total_credits }}</td>
                  <td>
                    <span :class="code.remaining_credits > 0 ? 'text-success' : 'text-danger'">
                      {{ code.remaining_credits }}
                    </span>
                  </td>
                  <td>
                    <span 
                      class="badge"
                      :class="{
                        'bg-success': code.status === 'active',
                        'bg-warning': code.status === 'used',
                        'bg-danger': code.status === 'expired'
                      }"
                    >
                      {{ getStatusText(code.status) }}
                    </span>
                  </td>
                  <td>{{ formatDate(code.created_at) }}</td>
                  <td>
                    <button 
                      class="btn btn-sm btn-outline-primary"
                      @click="viewCodeDetails(code)"
                    >
                      جزئیات
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- Code Details Modal -->
    <div 
      v-if="selectedCode"
      class="modal fade show d-block"
      style="background-color: rgba(0,0,0,0.5);"
      @click.self="selectedCode = null"
    >
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">جزئیات کد</h5>
            <button type="button" class="btn-close" @click="selectedCode = null"></button>
          </div>
          <div class="modal-body">
            <div class="row mb-3">
              <div class="col-md-6">
                <strong>کد:</strong>
                <code class="d-block bg-light p-2 rounded mt-1">{{ selectedCode.code }}</code>
              </div>
              <div class="col-md-6">
                <strong>دوره:</strong>
                <p class="mt-1">{{ selectedCode.course?.title || 'نامشخص' }}</p>
              </div>
            </div>
            <div class="row mb-3">
              <div class="col-md-6">
                <strong>تعداد کل اعتبار:</strong>
                <p class="mt-1">{{ selectedCode.total_credits }}</p>
              </div>
              <div class="col-md-6">
                <strong>اعتبار باقیمانده:</strong>
                <p class="mt-1" :class="selectedCode.remaining_credits > 0 ? 'text-success' : 'text-danger'">
                  {{ selectedCode.remaining_credits }}
                </p>
              </div>
            </div>
            <div class="row mb-3">
              <div class="col-md-6">
                <strong>تاریخ خرید:</strong>
                <p class="mt-1">{{ formatDate(selectedCode.created_at) }}</p>
              </div>
              <div class="col-md-6">
                <strong>وضعیت:</strong>
                <p class="mt-1">
                  <span 
                    class="badge"
                    :class="{
                      'bg-success': selectedCode.status === 'active',
                      'bg-warning': selectedCode.status === 'used',
                      'bg-danger': selectedCode.status === 'expired'
                    }"
                  >
                    {{ getStatusText(selectedCode.status) }}
                  </span>
                </p>
              </div>
            </div>
            <div v-if="selectedCode.usage_history && selectedCode.usage_history.length > 0">
              <strong>تاریخچه استفاده:</strong>
              <div class="table-responsive mt-2">
                <table class="table table-sm">
                  <thead>
                    <tr>
                      <th>تاریخ</th>
                      <th>کاربر</th>
                      <th>دوره</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(usage, index) in selectedCode.usage_history" :key="index">
                      <td>{{ formatDate(usage.used_at) }}</td>
                      <td>{{ usage.user?.email || 'نامشخص' }}</td>
                      <td>{{ usage.course?.title || 'نامشخص' }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'

definePageMeta({
  layout: 'account',
  middleware: 'auth'
})

const { $api, $sweetalert } = useNuxtApp()
const token = useCookie("token").value

// Data
const codes = ref([])
const courses = ref([])
const loading = ref(false)
const searchQuery = ref('')
const statusFilter = ref('')
const courseFilter = ref('')
const selectedCode = ref(null)

const stats = reactive({
  totalCodes: 0,
  activeCodes: 0,
  usedCodes: 0
})

// Methods
const formatDate = (dateString) => {
  if (!dateString) return 'نامشخص'
  const date = new Date(dateString)
  return date.toLocaleDateString('fa-IR')
}

const getStatusText = (status) => {
  const statusMap = {
    'active': 'فعال',
    'used': 'استفاده شده',
    'expired': 'منقضی شده'
  }
  return statusMap[status] || status
}

const copyCode = (code) => {
  navigator.clipboard.writeText(code).then(() => {
    $sweetalert.success('کد کپی شد')
  }).catch(() => {
    $sweetalert.error('خطا در کپی کردن کد')
  })
}

const viewCodeDetails = async (code) => {
  // If code object already has all details, use it directly
  // Otherwise, you might need to fetch from API if you have a detail endpoint
  selectedCode.value = code
}

const loadCodes = async () => {
  loading.value = true
  try {
    const response = await $api.post('/payment/code/list', {
      search: searchQuery.value || null,
      status: statusFilter.value || null,
      course_id: courseFilter.value || null
    }, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })

    if (response.data.status) {
      codes.value = response.data.data.codes || response.data.data || []
      
      // Calculate stats from codes
      stats.totalCodes = codes.value.length
      stats.activeCodes = codes.value.filter(c => c.status === 'active' || c.remaining_credits > 0).length
      stats.usedCodes = codes.value.filter(c => c.status === 'used' || c.remaining_credits === 0).length
    }
  } catch (error) {
    console.error('Error loading codes:', error)
    $sweetalert.error('خطا در بارگذاری کدها')
  } finally {
    loading.value = false
  }
}

const loadCourses = async () => {
  try {
    const response = await $api.post('/payment/courses', {
      page_size: 1000
    }, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    if (response.data.status) {
      courses.value = response.data.data.data || response.data.data || []
    }
  } catch (error) {
    console.error('Error loading courses:', error)
  }
}

onMounted(async () => {
  await Promise.all([
    loadCodes(),
    loadCourses()
  ])
})
</script>

<style scoped>
.modal.show {
  display: block;
}
</style>

