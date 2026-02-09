<template>
  <div class="container py-5">
    <!-- Header -->
    <div class="row mb-4">
      <div class="col-12">
        <h2 class="text-dark fw-bold mb-3">
          <i class="icon icon-filled-building text-danger me-2"></i>
          مدیریت سازمان
        </h2>
        <p class="text-muted">اطلاعات و تنظیمات سازمان خود را مدیریت کنید</p>
      </div>
    </div>

    <!-- Organization Info Card -->
    <div class="card border-0 shadow-sm mb-4">
      <div class="card-header bg-light border-0 py-3">
        <h5 class="mb-0 text-dark">
          <i class="icon icon-filled-info-circle text-primary me-2"></i>
          اطلاعات سازمان
        </h5>
      </div>
      <div class="card-body">
        <!-- Loading State -->
        <div v-if="loading" class="text-center py-5">
          <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">در حال بارگذاری...</span>
          </div>
          <p class="text-muted mt-3">در حال بارگذاری اطلاعات...</p>
        </div>

        <!-- No Organization State -->
        <div v-else-if="!organization" class="text-center py-5">
          <i class="icon icon-filled-building text-muted" style="font-size: 4rem;"></i>
          <h4 class="text-muted mt-3">سازمانی ایجاد نشده است</h4>
          <p class="text-muted">برای شروع، ابتدا سازمان خود را ایجاد کنید</p>
          <button @click="showCreateForm = true" class="btn btn-primary">
            <i class="icon icon-filled-plus me-2"></i>
            ایجاد سازمان
          </button>
        </div>

        <!-- Organization Display -->
        <div v-else class="row">
          <div class="col-lg-4 col-md-6 mb-4">
            <div class="text-center">
              <div class="position-relative d-inline-block">
                <img 
                  :src="organizationLogoUrl" 
                  :alt="organization.name"
                  class="rounded-circle border border-3 border-primary"
                  style="width: 150px; height: 150px; object-fit: cover;"
                />
                <button 
                  @click="triggerLogoUpload"
                  class="btn btn-sm btn-primary position-absolute bottom-0 end-0 rounded-circle"
                  style="width: 40px; height: 40px;"
                >
                  <i class="icon icon-filled-camera text-white"></i>
                </button>
              </div>
              <input 
                ref="logoInput"
                type="file" 
                accept="image/*" 
                @change="handleLogoUpload"
                class="d-none"
              />
            </div>
          </div>
          
          <div class="col-lg-8 col-md-6">
            <div class="mb-3">
              <label class="form-label fw-bold text-dark">نام سازمان</label>
              <div class="d-flex align-items-center">
                <span class="text-dark fs-5">{{ organization.name }}</span>
                <button @click="editField('name')" class="btn btn-sm btn-outline-primary ms-2">
                  <i class="icon icon-filled-pen"></i>
                </button>
              </div>
            </div>

            <div class="mb-3">
              <label class="form-label fw-bold text-dark">توضیحات</label>
              <div class="d-flex align-items-start">
                <p class="text-muted mb-0 flex-grow-1">{{ organization.description || 'توضیحاتی وارد نشده است' }}</p>
                <button @click="editField('description')" class="btn btn-sm btn-outline-primary ms-2">
                  <i class="icon icon-filled-pen"></i>
                </button>
              </div>
            </div>

            <div class="mb-3" v-if="organization.website_url">
              <label class="form-label fw-bold text-dark">وب‌سایت</label>
              <div class="d-flex align-items-center">
                <a :href="organization.website_url" target="_blank" class="text-primary text-decoration-none">
                  {{ organization.website_url }}
                </a>
                <button @click="editField('website_url')" class="btn btn-sm btn-outline-primary ms-2">
                  <i class="icon icon-filled-pen"></i>
                </button>
              </div>
            </div>

            <div class="mb-3" v-if="organization.subdomain">
              <label class="form-label fw-bold text-dark">زیردامنه</label>
              <div class="d-flex align-items-center">
                <span class="text-dark fs-6">
                  <i class="icon icon-regular-globe me-2"></i>
                  {{ organization.subdomain }}
                </span>
                <button @click="editField('subdomain')" class="btn btn-sm btn-outline-primary ms-2">
                  <i class="icon icon-filled-pen"></i>
                </button>
              </div>
            </div>

            <div class="mb-3">
              <label class="form-label fw-bold text-dark">وضعیت</label>
              <div class="d-flex align-items-center">
                <span 
                  class="badge p-2"
                  :class="organization.is_verified ? 'bg-success' : 'bg-warning'"
                >
                  <i :class="organization.is_verified ? 'icon icon-filled-check' : 'icon icon-filled-clock'" class="me-1"></i>
                  {{ organization.is_verified ? 'تأیید شده' : 'در انتظار تأیید' }}
                </span>
              </div>
            </div>

            <div class="mt-4">
              <button @click="showCreateForm = true" class="btn btn-primary me-2">
                <i class="icon icon-filled-pen me-2"></i>
                ویرایش اطلاعات
              </button>
              <button @click="viewOrganization" class="btn btn-outline-primary">
                <i class="icon icon-filled-eye me-2"></i>
                مشاهده صفحه سازمان
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Teachers Management Section -->
    <div v-if="organization" class="card border-0 shadow-sm mb-4">
      <div class="card-header bg-light border-0 py-3 d-flex justify-content-between align-items-center">
        <h5 class="mb-0 text-dark">
          <i class="icon icon-filled-users text-primary me-2"></i>
          مدیریت مدرسان
        </h5>
        <button @click="showAddTeacherModal = true" class="btn btn-primary btn-sm">
          <i class="icon icon-filled-plus me-2"></i>
          افزودن مدرس
        </button>
      </div>
      <div class="card-body">
        <!-- Loading State -->
        <div v-if="teachersLoading" class="text-center py-4">
          <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">در حال بارگذاری...</span>
          </div>
          <p class="text-muted mt-3">در حال بارگذاری لیست مدرسان...</p>
        </div>

        <!-- Teachers List -->
        <div v-else-if="teachers.length > 0" class="row g-3">
          <div 
            v-for="teacher in teachers" 
            :key="teacher.id"
            class="col-lg-6 col-md-12"
          >
            <div class="card border-0 shadow-sm h-100">
              <div class="card-body">
                <div class="d-flex align-items-center justify-content-between mb-3">
                  <div class="d-flex align-items-center">
                    <div class="avatar-circle me-3">
                      <i class="icon icon-filled-user text-white"></i>
                    </div>
                    <div>
                      <h6 class="mb-1 fw-bold">{{ teacher.first_name }} {{ teacher.last_name }}</h6>
                      <small class="text-muted">{{ teacher.phone_number }}</small>
                    </div>
                  </div>
                  <div class="d-flex flex-column align-items-end">
                    <span 
                      class="badge p-2 mb-1"
                      :class="teacher.is_active ? 'bg-success' : 'bg-secondary'"
                    >
                      <i :class="teacher.is_active ? 'icon icon-filled-check' : 'icon icon-filled-close'" class="me-1"></i>
                      {{ teacher.is_active ? 'فعال' : 'غیرفعال' }}
                    </span>
                    <span 
                      class="badge p-2"
                      :class="teacher.is_verified ? 'bg-primary' : 'bg-warning'"
                    >
                      <i :class="teacher.is_verified ? 'icon icon-filled-check' : 'icon icon-filled-clock'" class="me-1"></i>
                      {{ teacher.is_verified ? 'تأیید شده' : 'در انتظار تأیید' }}
                    </span>
                  </div>
                </div>
                
                <div class="d-flex justify-content-between align-items-center">
                  <small class="text-muted">
                    عضویت از: {{ formatDate(teacher.create_date) }}
                  </small>
                  <div class="d-flex gap-2">
                    <!-- Verify/Unverify Button -->
                    <button 
                      v-if="teacher.is_verified"
                      @click="verifyTeacher(teacher.id, 'unverify')"
                      class="btn btn-outline-warning btn-sm"
                      :disabled="teacher.id === currentUserTeacherId"
                    >
                      <i class="icon icon-filled-close me-1"></i>
                      لغو تأیید
                    </button>
                    <button 
                      v-else
                      @click="verifyTeacher(teacher.id, 'verify')"
                      class="btn btn-outline-primary btn-sm"
                    >
                      <i class="icon icon-filled-check me-1"></i>
                      تأیید
                    </button>
                    
                    <!-- Activate/Deactivate Button -->
                    <button 
                      v-if="teacher.is_active"
                      @click="toggleTeacher(teacher.id, 'deactivate')"
                      class="btn btn-outline-danger btn-sm"
                      :disabled="teacher.id === currentUserTeacherId"
                    >
                      <i class="icon icon-filled-close me-1"></i>
                      غیرفعال
                    </button>
                    <button 
                      v-else
                      @click="toggleTeacher(teacher.id, 'activate')"
                      class="btn btn-outline-success btn-sm"
                    >
                      <i class="icon icon-filled-check me-1"></i>
                      فعال
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- No Teachers State -->
        <div v-else class="text-center py-5">
          <i class="icon icon-filled-users text-muted" style="font-size: 3rem;"></i>
          <h5 class="text-muted mt-3">مدرسانی یافت نشد</h5>
          <p class="text-muted">هنوز مدرسی به این سازمان اضافه نشده است</p>
        </div>
      </div>
    </div>

    <!-- Create/Edit Organization Modal -->
    <div v-if="showCreateForm" class="modal show d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5);">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              <i class="icon icon-filled-building text-primary me-2"></i>
              {{ organization ? 'ویرایش سازمان' : 'ایجاد سازمان جدید' }}
            </h5>
            <button type="button" class="btn-close" @click="closeForm"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="submitForm">
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label for="name" class="form-label">نام سازمان <span class="text-danger">*</span></label>
                  <input 
                    type="text" 
                    class="form-control" 
                    id="name"
                    v-model="formData.name"
                    :class="{ 'is-invalid': errors.name }"
                    required
                  >
                  <div v-if="errors.name" class="invalid-feedback">{{ errors.name }}</div>
                </div>

                <div class="col-md-6 mb-3">
                  <label for="website_url" class="form-label">آدرس وب‌سایت</label>
                  <input 
                    type="url" 
                    class="form-control" 
                    id="website_url"
                    v-model="formData.website_url"
                    :class="{ 'is-invalid': errors.website_url }"
                    placeholder="https://example.com"
                  >
                  <div v-if="errors.website_url" class="invalid-feedback">{{ errors.website_url }}</div>
                </div>
              </div>

              <div class="row">
                <div class="col-md-6 mb-3">
                  <label for="subdomain" class="form-label">
                    زیردامنه
                    <i class="icon icon-regular-globe ms-1"></i>
                  </label>
                  <div class="input-group">
                    <input 
                      type="text" 
                      class="form-control" 
                      id="subdomain"
                      v-model="formData.subdomain"
                      :class="{ 'is-invalid': errors.subdomain }"
                      placeholder="subdomain"
                    />
                    <span class="input-group-text bg-light">
                      <i class="icon icon-regular-globe"></i>
                    </span>
                  </div>
                  <div v-if="errors.subdomain" class="invalid-feedback">{{ errors.subdomain }}</div>
                  <small class="text-muted d-block mt-1">
                    زیردامنه اختصاصی سازمان خود را وارد کنید
                  </small>
                </div>
              </div>

              <div class="mb-3">
                <label for="description" class="form-label">توضیحات <span class="text-danger">*</span></label>
                <textarea 
                  class="form-control" 
                  id="description"
                  v-model="formData.description"
                  :class="{ 'is-invalid': errors.description }"
                  rows="4"
                  required
                ></textarea>
                <div v-if="errors.description" class="invalid-feedback">{{ errors.description }}</div>
              </div>

              <div class="mb-3">
                <label for="logo" class="form-label">لوگو سازمان</label>
                <input 
                  type="file" 
                  class="form-control" 
                  id="logo"
                  accept="image/*"
                  @change="handleFileSelect"
                  :class="{ 'is-invalid': errors.logo }"
                >
                <div v-if="errors.logo" class="invalid-feedback">{{ errors.logo }}</div>
                <div v-if="selectedFile" class="mt-2">
                  <small class="text-muted">فایل انتخاب شده: {{ selectedFile.name }}</small>
                </div>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeForm">انصراف</button>
            <button 
              type="button" 
              class="btn btn-primary" 
              @click="submitForm"
              :disabled="submitting"
            >
              <span v-if="submitting" class="spinner-border spinner-border-sm me-2"></span>
              {{ organization ? 'به‌روزرسانی' : 'ایجاد' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Add Teacher Modal -->
    <div v-if="showAddTeacherModal" class="modal show d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5);">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              <i class="icon icon-filled-user-plus text-primary me-2"></i>
              افزودن مدرس جدید
            </h5>
            <button type="button" class="btn-close" @click="closeAddTeacherModal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="addTeacher">
              <div class="mb-3">
                <label for="phone_number" class="form-label">شماره تلفن مدرس <span class="text-danger">*</span></label>
                <input 
                  type="tel" 
                  class="form-control" 
                  id="phone_number"
                  v-model="addTeacherForm.phone_number"
                  :class="{ 'is-invalid': addTeacherErrors.phone_number }"
                  placeholder="09123456789"
                  required
                >
                <div v-if="addTeacherErrors.phone_number" class="invalid-feedback">{{ addTeacherErrors.phone_number }}</div>
                <div class="form-text">شماره تلفن مدرس را وارد کنید. مدرس باید قبلاً در سیستم ثبت نام کرده باشد.</div>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeAddTeacherModal">انصراف</button>
            <button type="button" class="btn btn-primary" @click="addTeacher" :disabled="addTeacherSubmitting">
              <span v-if="addTeacherSubmitting" class="spinner-border spinner-border-sm me-2" role="status"></span>
              <i v-else class="icon icon-filled-plus me-2"></i>
              افزودن مدرس
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive, computed } from 'vue'
import { useAuthStore } from '~/stores/auth'

const authStore = useAuthStore()
const { $api, $sweetalert } = useNuxtApp()

// Reactive data
const loading = ref(true)
const submitting = ref(false)
const organization = ref(null)
const { getMediaUrl } = useMediaUrl()

// تبدیل آدرس logo به آدرس با /api
const organizationLogoUrl = computed(() => {
  const defaultUrl = '/images/user.png'
  const url = organization.value?.logo || defaultUrl
  return getMediaUrl(url)
})
const showCreateForm = ref(false)
const selectedFile = ref(null)
const logoInput = ref(null)

// Teachers management
const teachers = ref([])
const teachersLoading = ref(false)
const currentUserTeacherId = ref(null)
const showAddTeacherModal = ref(false)
const addTeacherSubmitting = ref(false)

// Add teacher form
const addTeacherForm = reactive({
  phone_number: ''
})

const addTeacherErrors = reactive({
  phone_number: ''
})

// Form data
const formData = reactive({
  name: '',
  description: '',
  website_url: '',
  subdomain: '',
  logo: null
})

// Errors
const errors = reactive({
  name: '',
  description: '',
  website_url: '',
  subdomain: '',
  logo: ''
})

// Fetch organization data
const fetchOrganization = async () => {
  const token = useCookie("token").value
  if (!token) {
    loading.value = false
    return
  }

  try {
    console.log('Current user:', authStore.user)
    console.log('User ID:', authStore.user?.id)
    
    // First try to get current user's organization using the new endpoint
    const response = await $api.post('/course/organization/detail', {}, {
      headers: {
        Authorization: "Bearer " + token,
      },
    })

    console.log('Organization API Response:', response.data)

    if (response.data.status && response.data.data) {
      organization.value = response.data.data
      populateForm(response.data.data)
      console.log('Organization loaded:', organization.value)
    }
  } catch (error) {
    console.error('خطا در دریافت اطلاعات سازمان:', error)
    console.error('Error response:', error.response?.data)
    
    // Fallback: try to get from organization list
    try {
      console.log('Trying fallback method...')
      const fallbackResponse = await $api.post('/course/organization/list', {}, {
        headers: {
          Authorization: "Bearer " + token,
        },
      })

      if (fallbackResponse.data.status && fallbackResponse.data.data.data) {
        // Find current user's organization
        const userOrg = fallbackResponse.data.data.data.find(org => 
          org.user === authStore.user?.id || org.user_id === authStore.user?.id
        )
        if (userOrg) {
          organization.value = userOrg
          populateForm(userOrg)
          console.log('Organization loaded via fallback:', organization.value)
        }
      }
    } catch (fallbackError) {
      console.error('Fallback also failed:', fallbackError)
    }
  } finally {
    loading.value = false
  }
}

// Fetch teachers in organization
const fetchTeachers = async () => {
  const token = useCookie("token").value
  if (!token) return

  teachersLoading.value = true

  try {
    const response = await $api.post('/course/organization/teachers/list', {}, {
      headers: {
        Authorization: "Bearer " + token,
      },
    })

    if (response.data.status && response.data.data) {
      teachers.value = response.data.data
      
      // Find current user's teacher ID
      const currentTeacher = teachers.value.find(teacher => 
        teacher.user_id === authStore.user?.id
      )
      if (currentTeacher) {
        currentUserTeacherId.value = currentTeacher.id
      }
    }
  } catch (error) {
    console.error('خطا در دریافت لیست مدرسان:', error)
  } finally {
    teachersLoading.value = false
  }
}

// Toggle teacher active/inactive status
const toggleTeacher = async (teacherId, action) => {
  const token = useCookie("token").value
  if (!token) return

  try {
    const response = await $api.post('/course/organization/teachers/toggle', {
      teacher_id: teacherId,
      action: action
    }, {
      headers: {
        Authorization: "Bearer " + token,
      },
    })

    if (response.data.status) {
      // Update the teacher in the local list
      const teacherIndex = teachers.value.findIndex(t => t.id === teacherId)
      if (teacherIndex !== -1) {
        teachers.value[teacherIndex].is_active = response.data.data.is_active
      }
      
      // Show success message
      const actionText = action === 'activate' ? 'فعال' : 'غیرفعال'
      showSuccessMessage(`مدرس با موفقیت ${actionText} شد`)
    }
  } catch (error) {
    console.error('خطا در تغییر وضعیت مدرس:', error)
    showErrorMessage('خطا در تغییر وضعیت مدرس')
  }
}

// Verify/unverify teacher
const verifyTeacher = async (teacherId, action) => {
  const token = useCookie("token").value
  if (!token) return

  try {
    const response = await $api.post('/course/organization/teachers/verify', {
      teacher_id: teacherId,
      action: action
    }, {
      headers: {
        Authorization: "Bearer " + token,
      },
    })

    if (response.data.status) {
      // Update the teacher in the local list
      const teacherIndex = teachers.value.findIndex(t => t.id === teacherId)
      if (teacherIndex !== -1) {
        teachers.value[teacherIndex].is_verified = response.data.data.is_verified
      }
      
      // Show success message
      const actionText = action === 'verify' ? 'تأیید' : 'لغو تأیید'
      showSuccessMessage(`مدرس با موفقیت ${actionText} شد`)
    }
  } catch (error) {
    console.error('خطا در تغییر وضعیت تأیید مدرس:', error)
    showErrorMessage('خطا در تغییر وضعیت تأیید مدرس')
  }
}

// Add new teacher
const addTeacher = async () => {
  const token = useCookie("token").value
  if (!token) return

  addTeacherSubmitting.value = true
  clearAddTeacherErrors()

  try {
    const response = await $api.post('/course/organization/teachers/add', {
      phone_number: addTeacherForm.phone_number
    }, {
      headers: {
        Authorization: "Bearer " + token,
      },
    })

    if (response.data.status) {
      // Add the new teacher to the local list
      teachers.value.push(response.data.data)
      
      // Show success message
      showSuccessMessage('مدرس جدید با موفقیت اضافه شد')
      
      // Close modal and clear form
      closeAddTeacherModal()
    }
  } catch (error) {
    console.error('خطا در افزودن مدرس:', error)
    
    if (error.response?.data?.message) {
      const errorMessage = error.response.data.message
      
      // Show specific dialog for user not found
      if (errorMessage === 'User with this phone number not found') {
        showUserNotFoundDialog()
      } else {
        showErrorMessage(errorMessage)
      }
    } else {
      showErrorMessage('خطا در افزودن مدرس')
    }
  } finally {
    addTeacherSubmitting.value = false
  }
}

// Close add teacher modal
const closeAddTeacherModal = () => {
  showAddTeacherModal.value = false
  addTeacherForm.phone_number = ''
  clearAddTeacherErrors()
}

// Clear add teacher errors
const clearAddTeacherErrors = () => {
  addTeacherErrors.phone_number = ''
}

// Format date helper
const formatDate = (dateString) => {
  if (!dateString) return ''
  
  const date = new Date(dateString)
  return new Intl.DateTimeFormat('fa-IR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  }).format(date)
}

// Show success message
const showSuccessMessage = (message) => {
  $sweetalert.fire({
    title: 'موفقیت',
    text: message,
    icon: 'success',
    confirmButtonText: 'متوجه شدم'
  })
}

// Show error message
const showErrorMessage = (message) => {
  $sweetalert.fire({
    title: 'خطا',
    text: message,
    icon: 'error',
    confirmButtonText: 'متوجه شدم'
  })
}

// Show user not found dialog
const showUserNotFoundDialog = () => {
  $sweetalert.fire({
    title: 'کاربر یافت نشد',
    text: 'کاربری با این شماره تلفن در سیستم ثبت نام نکرده است. لطفاً شماره تلفن را بررسی کنید یا از کاربر بخواهید ابتدا در سیستم ثبت نام کند.',
    icon: 'warning',
    confirmButtonText: 'متوجه شدم'
  })
}

// Populate form with existing data
const populateForm = (org) => {
  formData.name = org.name || ''
  formData.description = org.description || ''
  formData.website_url = org.website_url || ''
  formData.subdomain = org.subdomain || ''
}

// Clear form
const clearForm = () => {
  formData.name = ''
  formData.description = ''
  formData.website_url = ''
  formData.subdomain = ''
  formData.logo = null
  selectedFile.value = null
  clearErrors()
}

// Clear errors
const clearErrors = () => {
  errors.name = ''
  errors.description = ''
  errors.website_url = ''
  errors.subdomain = ''
  errors.logo = ''
}

// Handle file selection
const handleFileSelect = (event) => {
  const file = event.target.files[0]
  if (file) {
    selectedFile.value = file
    formData.logo = file
  }
}

// Trigger logo upload
const triggerLogoUpload = () => {
  logoInput.value?.click()
}

// Handle logo upload
const handleLogoUpload = async (event) => {
  const file = event.target.files[0]
  if (!file) return

  const token = useCookie("token").value
  if (!token) return

  const formData = new FormData()
  formData.append('logo', file)

  try {
    submitting.value = true
    const response = await $api.post('/course/organization/edit', formData, {
      headers: {
        Authorization: "Bearer " + token,
        'Content-Type': 'multipart/form-data',
      },
    })

    if (response.data.status) {
      organization.value.logo = response.data.data.logo
      // Show success message
      alert('لوگو با موفقیت به‌روزرسانی شد')
    }
  } catch (error) {
    console.error('خطا در آپلود لوگو:', error)
    alert('خطا در آپلود لوگو')
  } finally {
    submitting.value = false
  }
}

// Edit specific field
const editField = (field) => {
  showCreateForm.value = true
  // Focus on the specific field
  setTimeout(() => {
    const element = document.getElementById(field)
    if (element) element.focus()
  }, 100)
}

// Submit form
const submitForm = async () => {
  clearErrors()
  submitting.value = true

  const token = useCookie("token").value
  if (!token) {
    alert('لطفاً وارد حساب کاربری خود شوید')
    return
  }

  const submitData = new FormData()
  submitData.append('name', formData.name)
  submitData.append('description', formData.description)
  if (formData.website_url) {
    submitData.append('website_url', formData.website_url)
  }
  submitData.append('subdomain', formData.subdomain || '')
  if (formData.logo) {
    submitData.append('logo', formData.logo)
  }

  try {
    const endpoint = organization.value ? '/course/organization/edit' : '/course/organization/create'
    const response = await $api.post(endpoint, submitData, {
      headers: {
        Authorization: "Bearer " + token,
        'Content-Type': 'multipart/form-data',
      },
    })

    if (response.data.status) {
      organization.value = response.data.data
      showCreateForm.value = false
      clearForm()
      alert(organization.value ? 'سازمان با موفقیت به‌روزرسانی شد' : 'سازمان با موفقیت ایجاد شد')
    }
  } catch (error) {
    console.error('خطا در ارسال فرم:', error)
    if (error.response?.data?.data) {
      const errorData = error.response.data.data
      Object.keys(errorData).forEach(key => {
        if (errors.hasOwnProperty(key)) {
          errors[key] = Array.isArray(errorData[key]) ? errorData[key][0] : errorData[key]
        }
      })
    } else {
      alert('خطا در ارسال فرم')
    }
  } finally {
    submitting.value = false
  }
}

// Close form
const closeForm = () => {
  showCreateForm.value = false
  if (organization.value) {
    populateForm(organization.value)
  } else {
    clearForm()
  }
}

// View organization page
const viewOrganization = () => {
  if (organization.value?.slug) {
    navigateTo(`/company/${organization.value.slug}`)
  } else {
    alert('آدرس سازمان در دسترس نیست')
  }
}

// Page meta
definePageMeta({
  layout: "account",
  middleware: ["auth"],
})

// Lifecycle
onMounted(async () => {
  await fetchOrganization()
  if (organization.value) {
    fetchTeachers()
  }
})
</script>

<style scoped>
.modal {
  z-index: 1055;
}

.modal-dialog {
  margin: 1.75rem auto;
}

.form-control:focus {
  border-color: #dc3545;
  box-shadow: 0 0 0 0.2rem rgba(220, 53, 69, 0.25);
}

.btn-primary {
  background-color: #dc3545;
  border-color: #dc3545;
}

.btn-primary:hover {
  background-color: #c82333;
  border-color: #bd2130;
}

.border-primary {
  border-color: #dc3545 !important;
}

.avatar-circle {
  width: 40px;
  height: 40px;
  background-color: #dc3545;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
}

.btn-group .btn {
  font-size: 0.875rem;
}

.badge {
  font-size: 0.75rem;
}

.text-primary {
  color: #dc3545 !important;
}

/* Custom SweetAlert styling */
:deep(.swal2-popup-custom) {
  border-radius: 15px;
  font-family: 'IRANSans', sans-serif;

}

:deep(.swal2-title) {
  font-family: 'IRANSans', sans-serif;
  font-weight: bold;
}

:deep(.swal2-html-container) {
  font-family: 'IRANSans', sans-serif;
}

:deep(.swal2-confirm) {
  font-family: 'IRANSans', sans-serif;
  border-radius: 8px;
}

.icon {
  font-size: 1.1rem;
}

.badge {
  font-size: 0.875rem;
}

@media (max-width: 768px) {
  .modal-dialog {
    margin: 0.5rem;
  }
  
  .modal-lg {
    max-width: calc(100% - 1rem);
  }
}
</style>
