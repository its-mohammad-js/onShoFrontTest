<template>
  <form @submit.prevent="saveStandard">
    <div class="row">
      <!-- Basic Information -->
      <div class="col-md-6">
        <h6 class="text-primary mb-3">اطلاعات پایه</h6>
        
        <div class="mb-3">
          <label class="form-label">شماره *</label>
          <input 
            type="number" 
            class="form-control" 
            v-model="form.number"
            :class="{ 'is-invalid': errors.number }"
          >
          <div v-if="errors.number" class="invalid-feedback">{{ errors.number }}</div>
        </div>

        <div class="mb-3">
          <label class="form-label">نام استاندارد *</label>
          <input 
            type="text" 
            class="form-control" 
            v-model="form.standard_name"
            :class="{ 'is-invalid': errors.standard_name }"
          >
          <div v-if="errors.standard_name" class="invalid-feedback">{{ errors.standard_name }}</div>
        </div>

        <div class="mb-3">
          <label class="form-label">نام استاندارد به لاتین</label>
          <input 
            type="text" 
            class="form-control" 
            v-model="form.standard_name_latin"
          >
        </div>

        <div class="mb-3">
          <label class="form-label">والد</label>
          <select class="form-control" v-model="form.parent">
            <option value="">بدون والد (ریشه)</option>
            <option v-for="standard in parentStandards" :key="standard.id" :value="standard.id">
              {{ standard.standard_name }} ({{ standard.number }})
            </option>
          </select>
        </div>
      </div>

      <!-- Classification -->
      <div class="col-md-6">
        <h6 class="text-primary mb-3">طبقه‌بندی</h6>
        
        <div class="mb-3">
          <label class="form-label">خوشه</label>
          <input 
            type="text" 
            class="form-control" 
            v-model="form.cluster"
          >
        </div>

        <div class="mb-3">
          <label class="form-label">نام گروه</label>
          <input 
            type="text" 
            class="form-control" 
            v-model="form.group_name"
          >
        </div>

        <div class="mb-3">
          <label class="form-label">نوع</label>
          <select class="form-control" v-model="form.type">
            <option value="شغل">شغل</option>
            <option value="مهارت">مهارت</option>
            <option value="صلاحیت">صلاحیت</option>
          </select>
        </div>
      </div>
    </div>

    <div class="row">
      <!-- Codes -->
      <div class="col-md-6">
        <h6 class="text-primary mb-3">کدها</h6>
        
        <div class="mb-3">
          <label class="form-label">کد استاندارد قدیم</label>
          <input 
            type="text" 
            class="form-control" 
            v-model="form.old_standard_code"
          >
        </div>

        <div class="mb-3">
          <label class="form-label">نسخه</label>
          <input 
            type="number" 
            class="form-control" 
            v-model="form.version"
            min="1"
          >
        </div>

        <div class="mb-3">
          <label class="form-label">کد شایستگی</label>
          <input 
            type="number" 
            class="form-control" 
            v-model="form.competency_code"
          >
        </div>

        <div class="mb-3">
          <label class="form-label">کد شغل ISCO</label>
          <input 
            type="number" 
            class="form-control" 
            v-model="form.isco_job_code"
          >
        </div>

        <div class="mb-3">
          <label class="form-label">کد گروه ISCO</label>
          <input 
            type="number" 
            class="form-control" 
            v-model="form.isco_group_code"
          >
        </div>
      </div>

      <!-- Education and Hours -->
      <div class="col-md-6">
        <h6 class="text-primary mb-3">تحصیلات و ساعات</h6>
        
        <div class="mb-3">
          <label class="form-label">سطح تحصیلات ورودی</label>
          <input 
            type="text" 
            class="form-control" 
            v-model="form.entry_education_level"
          >
        </div>

        <div class="mb-3">
          <label class="form-label">ساعت نظری</label>
          <input 
            type="number" 
            class="form-control" 
            v-model="form.theoretical_hours"
            min="0"
            @input="calculateTotalHours"
          >
        </div>

        <div class="mb-3">
          <label class="form-label">ساعت عملی</label>
          <input 
            type="number" 
            class="form-control" 
            v-model="form.practical_hours"
            min="0"
            @input="calculateTotalHours"
          >
        </div>

        <div class="mb-3">
          <label class="form-label">ساعت کارورزی</label>
          <input 
            type="number" 
            class="form-control" 
            v-model="form.internship_hours"
            min="0"
            @input="calculateTotalHours"
          >
        </div>

        <div class="mb-3">
          <label class="form-label">ساعت پروژه</label>
          <input 
            type="number" 
            class="form-control" 
            v-model="form.project_hours"
            min="0"
            @input="calculateTotalHours"
          >
        </div>

        <div class="mb-3">
          <label class="form-label">ساعت کل</label>
          <input 
            type="number" 
            class="form-control" 
            v-model="form.total_hours"
            min="0"
            readonly
            style="background-color: #f8f9fa;"
          >
        </div>
      </div>
    </div>

    <div class="row">
      <!-- Additional Information -->
      <div class="col-md-6">
        <h6 class="text-primary mb-3">اطلاعات تکمیلی</h6>
        
        <div class="mb-3">
          <label class="form-label">کارو دانش</label>
          <select class="form-control" v-model="form.work_and_knowledge">
            <option value="هیچ کدام">هیچ کدام</option>
            <option value="کار">کار</option>
            <option value="دانش">دانش</option>
            <option value="کار و دانش">کار و دانش</option>
          </select>
        </div>

        <div class="mb-3">
          <label class="form-label">تاریخ تدوین و به روز رسانی</label>
          <input 
            type="date" 
            class="form-control" 
            v-model="form.compilation_date"
          >
        </div>
      </div>
    </div>

    <!-- Form Actions -->
    <div class="row">
      <div class="col-12">
        <hr>
        <div class="d-flex justify-content-end">
          <button type="button" class="btn btn-secondary me-2" @click="$emit('cancelled')">
            انصراف
          </button>
          <button type="submit" class="btn btn-primary" :disabled="saving">
            <span v-if="saving" class="spinner-border spinner-border-sm me-2"></span>
            {{ isEdit ? 'به‌روزرسانی' : 'ذخیره' }}
          </button>
        </div>
      </div>
    </div>
  </form>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'

// Get runtime config for API base URL
const config = useRuntimeConfig()

// Props
const props = defineProps({
  standard: {
    type: Object,
    default: null
  },
  isEdit: {
    type: Boolean,
    default: false
  }
})

// Emits
const emit = defineEmits(['saved', 'cancelled'])

// Reactive data
const saving = ref(false)
const errors = ref({})
const parentStandards = ref([])

// Form data
const form = reactive({
  number: null,
  standard_name: '',
  standard_name_latin: '',
  cluster: '',
  group_name: '',
  type: 'شغل',
  old_standard_code: '',
  version: 1,
  competency_code: 0,
  isco_job_code: null,
  isco_group_code: null,
  entry_education_level: '',
  theoretical_hours: null,
  practical_hours: null,
  internship_hours: 0,
  project_hours: 0,
  total_hours: null,
  work_and_knowledge: 'هیچ کدام',
  compilation_date: '',
  parent: null
})

// Computed
const totalHours = computed(() => {
  const theoretical = parseInt(form.theoretical_hours) || 0
  const practical = parseInt(form.practical_hours) || 0
  const internship = parseInt(form.internship_hours) || 0
  const project = parseInt(form.project_hours) || 0
  return theoretical + practical + internship + project
})

// Methods
const loadParentStandards = async () => {
  try {
    const response = await $fetch(`${config.public.apiBaseUrl}course/standards/for-course`)
    if (response.status) {
      parentStandards.value = response.data
    }
  } catch (error) {
    console.error('Error loading parent standards:', error)
  }
}

const calculateTotalHours = () => {
  form.total_hours = totalHours.value
}

const validateForm = () => {
  errors.value = {}
  
  if (!form.number) {
    errors.value.number = 'شماره الزامی است'
  }
  
  if (!form.standard_name) {
    errors.value.standard_name = 'نام استاندارد الزامی است'
  }
  
  return Object.keys(errors.value).length === 0
}

const saveStandard = async () => {
  if (!validateForm()) {
    return
  }
  
  saving.value = true
  errors.value = {}
  
  try {
    const url = props.isEdit ? `${config.public.apiBaseUrl}course/standards/update` : `${config.public.apiBaseUrl}course/standards/create`
    const body = { ...form }
    
    if (props.isEdit) {
      body.standard_id = props.standard.id
    }
    
    const response = await $fetch(url, {
      method: 'POST',
      body
    })
    
    if (response.status) {
      emit('saved')
    } else {
      if (response.errors) {
        errors.value = response.errors
      } else {
        alert('خطا در ذخیره استاندارد: ' + response.message)
      }
    }
  } catch (error) {
    console.error('Error saving standard:', error)
    alert('خطا در ذخیره استاندارد')
  } finally {
    saving.value = false
  }
}

const initializeForm = () => {
  if (props.standard) {
    Object.keys(form).forEach(key => {
      if (props.standard[key] !== undefined) {
        form[key] = props.standard[key]
      }
    })
  }
}

// Watchers
watch(() => props.standard, () => {
  initializeForm()
}, { immediate: true })

// Lifecycle
onMounted(() => {
  loadParentStandards()
  initializeForm()
})
</script>

<style scoped>
.form-label {
  font-weight: 600;
  color: #495057;
}

.text-primary {
  color: #007bff !important;
}

hr {
  margin: 1.5rem 0;
}

.spinner-border-sm {
  width: 1rem;
  height: 1rem;
}
</style>
