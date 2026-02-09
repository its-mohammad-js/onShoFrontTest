<template>
  <div class="container my-5">
    <div class="row justify-content-center">
      <div class="col-lg-8 col-md-10">
        <div class="card shadow-sm border-0 rounded-4">
          <div class="card-header bg-white border-0 pt-4 pb-3">
            <div class="d-flex align-items-center justify-content-between mb-2">
              <h3 class="fw-bold mb-0">ثبت کاربر دستی</h3>
              <nuxt-link class="text-danger1" to="/">
                <i class="icon icon-regular-angle-right"></i>
                بازگشت
              </nuxt-link>
            </div>
            <p class="text-muted mb-0">لطفاً اطلاعات کاربر را وارد کنید</p>
          </div>

          <div class="card-body p-4">
            <form @submit.prevent="submitForm">
              <!-- Name -->
              <div class="mb-4">
                <label class="form-label text-muted fw-bold d-flex align-items-center justify-content-start">
                  نام <span class="text-danger ms-1">*</span>
                </label>
                <input
                  v-model="form.name"
                  type="text"
                  class="form-control py-3"
                  :class="{ 'is-invalid': errors.name }"
                  placeholder="نام"
                  maxlength="100"
                  @blur="validateField('name')"
                  @input="clearError('name')"
                />
                <div v-if="errors.name" class="invalid-feedback d-block mt-1">
                  <i class="icon icon-regular-info-circle me-1"></i>
                  {{ errors.name }}
                </div>
              </div>

              <!-- Lastname -->
              <div class="mb-4">
                <label class="form-label text-muted fw-bold d-flex align-items-center justify-content-start">
                  نام خانوادگی <span class="text-danger ms-1">*</span>
                </label>
                <input
                  v-model="form.lastname"
                  type="text"
                  class="form-control py-3"
                  :class="{ 'is-invalid': errors.lastname }"
                  placeholder="نام خانوادگی"
                  maxlength="100"
                  @blur="validateField('lastname')"
                  @input="clearError('lastname')"
                />
                <div v-if="errors.lastname" class="invalid-feedback d-block mt-1">
                  <i class="icon icon-regular-info-circle me-1"></i>
                  {{ errors.lastname }}
                </div>
              </div>

              <!-- National Code -->
              <div class="mb-4">
                <label class="form-label text-muted fw-bold d-flex align-items-center justify-content-start">
                  کد ملی <span class="text-danger ms-1">*</span>
                </label>
                <input
                  v-model="form.nationalcode"
                  type="text"
                  class="form-control py-3"
                  :class="{ 'is-invalid': errors.nationalcode }"
                  placeholder="کد ملی (10 رقم)"
                  maxlength="10"
                  pattern="[0-9]*"
                  @blur="validateField('nationalcode')"
                  @input="clearError('nationalcode'); formatNationalCode()"
                />
                <div v-if="errors.nationalcode" class="invalid-feedback d-block mt-1">
                  <i class="icon icon-regular-info-circle me-1"></i>
                  {{ errors.nationalcode }}
                </div>
              </div>

              <!-- Tel -->
              <div class="mb-4">
                <label class="form-label text-muted fw-bold d-flex align-items-center justify-content-start">
                  شماره تماس <span class="text-danger ms-1">*</span>
                </label>
                <input
                  v-model="form.tel"
                  type="text"
                  class="form-control py-3"
                  :class="{ 'is-invalid': errors.tel }"
                  placeholder="09123456789"
                  maxlength="11"
                  pattern="[0-9]*"
                  @blur="validateField('tel')"
                  @input="clearError('tel'); formatTel()"
                />
                <div v-if="errors.tel" class="invalid-feedback d-block mt-1">
                  <i class="icon icon-regular-info-circle me-1"></i>
                  {{ errors.tel }}
                </div>
              </div>

              <!-- Birthdate -->
              <div class="mb-4">
                <label class="form-label text-muted fw-bold d-flex align-items-center justify-content-start">
                  تاریخ تولد
                </label>
                <date-picker
                  v-model="form.birthdate"
                  format="jYYYY/jMM/jDD"
                  display-format="jYYYY/jMM/jDD"
                  :clearable="true"
                  :editable="true"
                  placeholder="تاریخ تولد را انتخاب کنید"
                  class="form-control py-3"
                  :class="{ 'is-invalid': errors.birthdate }"
                  @change="clearError('birthdate')"
                />
                <div v-if="errors.birthdate" class="invalid-feedback d-block mt-1">
                  <i class="icon icon-regular-info-circle me-1"></i>
                  {{ errors.birthdate }}
                </div>
              </div>

              <!-- Address -->
              <div class="mb-4">
                <label class="form-label text-muted fw-bold d-flex align-items-center justify-content-start">
                  آدرس
                </label>
                <textarea
                  v-model="form.address"
                  class="form-control py-3"
                  :class="{ 'is-invalid': errors.address }"
                  placeholder="آدرس"
                  rows="3"
                  @blur="validateField('address')"
                  @input="clearError('address')"
                ></textarea>
                <div v-if="errors.address" class="invalid-feedback d-block mt-1">
                  <i class="icon icon-regular-info-circle me-1"></i>
                  {{ errors.address }}
                </div>
              </div>

              <!-- Career -->
              <div class="mb-4">
                <label class="form-label text-muted fw-bold d-flex align-items-center justify-content-start">
                  شغل
                </label>
                <input
                  v-model="form.career"
                  type="text"
                  class="form-control py-3"
                  :class="{ 'is-invalid': errors.career }"
                  placeholder="شغل"
                  maxlength="200"
                  @blur="validateField('career')"
                  @input="clearError('career')"
                />
                <div v-if="errors.career" class="invalid-feedback d-block mt-1">
                  <i class="icon icon-regular-info-circle me-1"></i>
                  {{ errors.career }}
                </div>
              </div>

              <!-- Submit Button -->
              <div class="d-grid gap-2 mt-4">
                <button
                  type="submit"
                  class="btn btn-danger py-3"
                  :disabled="submitting"
                >
                  <span v-if="submitting" class="spinner-border spinner-border-sm me-2"></span>
                  <span v-else>
                    <i class="icon icon-regular-check me-2"></i>
                  </span>
                  {{ submitting ? 'در حال ثبت...' : 'ثبت کاربر' }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import moment from 'moment-jalaali';

definePageMeta({
  layout: 'default'
});

const { $api, $sweetalert } = useNuxtApp();

const submitting = ref(false);

const form = reactive({
  name: '',
  lastname: '',
  nationalcode: '',
  tel: '',
  birthdate: '',
  address: '',
  career: ''
});

const errors = reactive({
  name: '',
  lastname: '',
  nationalcode: '',
  tel: '',
  birthdate: '',
  address: '',
  career: ''
});

const clearError = (field) => {
  if (errors[field]) {
    errors[field] = '';
  }
};

const formatNationalCode = () => {
  // Only allow numbers
  form.nationalcode = form.nationalcode.replace(/[^0-9]/g, '');
};

const formatTel = () => {
  // Only allow numbers
  form.tel = form.tel.replace(/[^0-9]/g, '');
};

const validateField = (field) => {
  clearError(field);

  switch (field) {
    case 'name':
      if (!form.name || form.name.trim().length === 0) {
        errors.name = 'وارد کردن نام الزامی است';
      } else if (form.name.length > 100) {
        errors.name = 'نام نباید بیشتر از 100 کاراکتر باشد';
      }
      break;

    case 'lastname':
      if (!form.lastname || form.lastname.trim().length === 0) {
        errors.lastname = 'وارد کردن نام خانوادگی الزامی است';
      } else if (form.lastname.length > 100) {
        errors.lastname = 'نام خانوادگی نباید بیشتر از 100 کاراکتر باشد';
      }
      break;

    case 'nationalcode':
      if (!form.nationalcode || form.nationalcode.trim().length === 0) {
        errors.nationalcode = 'وارد کردن کد ملی الزامی است';
      } else if (!/^\d{10}$/.test(form.nationalcode)) {
        errors.nationalcode = 'کد ملی باید دقیقاً 10 رقم باشد';
      }
      break;

    case 'tel':
      if (!form.tel || form.tel.trim().length === 0) {
        errors.tel = 'وارد کردن شماره تماس الزامی است';
      } else if (!/^\d{11}$/.test(form.tel)) {
        errors.tel = 'شماره تماس باید دقیقاً 11 رقم باشد';
      }
      break;

    case 'birthdate':
      if (form.birthdate) {
        // Validate Persian date format (YYYY-MM-DD)
        const dateRegex = /^\d{4}\/\d{2}\/\d{2}$/;
        if (!dateRegex.test(form.birthdate)) {
          errors.birthdate = 'فرمت تاریخ صحیح نیست';
        } else {
          // Check if date is valid using moment-jalaali
          const jDate = moment(form.birthdate, 'jYYYY/jMM/jDD');
          if (!jDate.isValid()) {
            errors.birthdate = 'تاریخ معتبر نیست';
          }
        }
      }
      break;

    case 'career':
      if (form.career && form.career.length > 200) {
        errors.career = 'شغل نباید بیشتر از 200 کاراکتر باشد';
      }
      break;
  }
};

const validateForm = () => {
  // Validate all required fields
  validateField('name');
  validateField('lastname');
  validateField('nationalcode');
  validateField('tel');
  
  // Validate optional fields only if they have values
  if (form.birthdate) {
    validateField('birthdate');
  }
  if (form.career) {
    validateField('career');
  }

  // Check if there are any errors
  return !Object.values(errors).some(error => error !== '');
};

const resetForm = () => {
  form.name = '';
  form.lastname = '';
  form.nationalcode = '';
  form.tel = '';
  form.birthdate = '';
  form.address = '';
  form.career = '';
  
  Object.keys(errors).forEach(key => {
    errors[key] = '';
  });
};

const submitForm = async () => {
  if (!validateForm()) {
    $sweetalert.error('لطفاً خطاهای فرم را برطرف کنید');
    return;
  }

  submitting.value = true;

  try {
    // Convert Persian date to Gregorian (YYYY-MM-DD) for API
    let birthdateGregorian = null;
    if (form.birthdate) {
      const jDate = moment(form.birthdate, 'jYYYY/jMM/jDD');
      if (jDate.isValid()) {
        birthdateGregorian = jDate.format('YYYY-MM-DD');
      }
    }

    // Prepare request data
    const requestData = {
      name: form.name.trim(),
      lastname: form.lastname.trim(),
      nationalcode: form.nationalcode.trim(),
      tel: form.tel.trim(),
      ...(birthdateGregorian && { birthdate: birthdateGregorian }),
      ...(form.address && { address: form.address.trim() }),
      ...(form.career && { career: form.career.trim() })
    };

    console.log('📤 Sending request to API:', requestData);

    const response = await $api.post('/auth/manual-user/create', requestData);

    console.log('✅ API Response:', response.data);

    if (response.data?.status) {
      $sweetalert.success(response.data.message || 'کاربر دستی با موفقیت ایجاد شد');
      resetForm();
    } else {
      // Handle API validation errors
      if (response.data?.data && typeof response.data.data === 'object') {
        // API returned field-specific errors
        Object.keys(response.data.data).forEach(field => {
          const fieldErrors = response.data.data[field];
          if (Array.isArray(fieldErrors) && fieldErrors.length > 0) {
            errors[field] = fieldErrors[0]; // Show first error for each field
          }
        });
        $sweetalert.error(response.data.message || 'خطا در ایجاد کاربر دستی');
      } else {
        $sweetalert.error(response.data?.message || 'خطا در ایجاد کاربر دستی');
      }
    }
  } catch (error) {
    console.error('❌ Error creating manual user:', error);
    
    // Handle error response
    if (error.response?.data) {
      const errorData = error.response.data;
      
      if (errorData?.data && typeof errorData.data === 'object') {
        // API returned field-specific errors
        Object.keys(errorData.data).forEach(field => {
          const fieldErrors = errorData.data[field];
          if (Array.isArray(fieldErrors) && fieldErrors.length > 0) {
            errors[field] = fieldErrors[0];
          }
        });
      }
      
      $sweetalert.error(errorData?.message || 'خطا در ایجاد کاربر دستی');
    } else {
      $sweetalert.error('خطا در ارتباط با سرور. لطفاً دوباره تلاش کنید');
    }
  } finally {
    submitting.value = false;
  }
};
</script>

<style scoped>
.card {
  border-radius: 16px;
}

.form-control {
  border: 1px solid #dee2e6;
  border-radius: 8px;
  transition: all 0.3s;
}

.form-control:focus {
  border-color: rgba(193, 18, 31, 1);
  box-shadow: 0 0 0 0.2rem rgba(193, 18, 31, 0.25);
}

.form-control.is-invalid {
  border-color: #dc3545;
}

.invalid-feedback {
  display: block;
  font-size: 0.875rem;
  color: #dc3545;
}

.btn-danger {
  background-color: rgba(193, 18, 31, 1);
  border-color: rgba(193, 18, 31, 1);
  border-radius: 8px;
}

.btn-danger:hover {
  background-color: rgba(161, 15, 26, 1);
  border-color: rgba(161, 15, 26, 1);
}

.btn-danger:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.text-danger1 {
  color: rgba(193, 18, 31, 1) !important;
}
</style>

