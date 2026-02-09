<template>
  <div class="container my-5">
    <nuxt-link class="mt-1 mb-3 cursor-pointer d-block text-danger1" to="/">
      <i class="icon icon-regular-angle-right"></i>بازگشت
    </nuxt-link>
    <div class="row d-flex align-items-center justify-content-between">
      <!-- Right Section -->
      <div class="col-md-5 form-container">
        <!-- User Type Selector -->
        <div class="mb-4">
          <label class="form-label text-muted fw-bold mb-3">نوع کاربری</label>
          <div class="d-flex gap-2 justify-content-center">
            <!-- کاربر -->
            <div
              :class="{ active: data.userType === 'user' }"
              class="user-type-icon-card"
              @click="changeUserType('user')"
            >
              <div class="icon-wrapper">
                <i class="icon icon-filled-user"></i>
              </div>
              <span class="icon-label">کاربر</span>
            </div>
            
            <!-- سازمان -->
            <div
              :class="{ active: data.userType === 'organization' }"
              class="user-type-icon-card"
              @click="changeUserType('organization')"
            >
              <div class="icon-wrapper">
                <i class="icon icon-filled-building"></i>
              </div>
              <span class="icon-label">سازمان</span>
            </div>
            
            <!-- آموزشگاه -->
            <div
              :class="{ active: data.userType === 'school' }"
              class="user-type-icon-card"
              @click="changeUserType('school')"
            >
              <div class="icon-wrapper">
                <i class="icon icon-filled-school"></i>
              </div>
              <span class="icon-label">آموزشگاه</span>
            </div>
          </div>
        </div>

        <!-- Tab Section (Step 1) -->
        <div v-if="data.step === 1">
          <ul class="nav nav-tabs custom-tabs mb-3" role="tablist">
            <li class="nav-item" role="presentation" @click="resetForm">
              <button
                :id="`${data.userType}-register-tab`"
                :class="{ active: data.actionType === 'register' }"
                class="nav-link custom-tab py-3"
                role="tab"
                type="button"
                @click="data.actionType = 'register'"
              >
                {{ data.userType === 'organization' ? 'ثبت نام سازمان' : data.userType === 'school' ? 'ثبت نام آموزشگاه' : 'ثبت نام' }}
              </button>
            </li>
            <li class="nav-item ms-2" role="presentation" @click="resetForm">
              <button
                :id="`${data.userType}-login-tab`"
                :class="{ active: data.actionType === 'login' }"
                class="nav-link custom-tab py-3"
                role="tab"
                type="button"
                @click="data.actionType = 'login'"
              >
                {{ data.userType === 'organization' ? 'ورود سازمان' : data.userType === 'school' ? 'ورود آموزشگاه' : 'ورود' }}
              </button>
            </li>
          </ul>

          <!-- Register Form -->
          <form v-if="data.actionType === 'register'" class="auth-form">
            <div class="row mb-3">
              <div class="col-6 mb-3">
                <label class="form-label text-muted fw-bold d-flex align-items-center justify-content-start" for="first_name">
                  نام
                </label>
                <input
                  id="first_name"
                  v-model="data.registerForm.first_name"
                  autocomplete="off"
                  class="form-control py-3 border-0 border-bottom border-3 shadow-none rounded-0"
                  placeholder="نام"
                  type="text"
                  @keyup="validateField('first_name', data.registerForm.first_name)"
                />
                <div v-if="data.errors.first_name" class="invalid-feedback d-block">
                  <i class="icon icon-regular-info-circle font-size-18"></i>
                  {{ data.errors.first_name }}
                </div>
              </div>
              <div class="col-6 mb-3">
                <label class="form-label text-muted fw-bold d-flex align-items-center justify-content-start" for="last_name">
                  نام خانوادگی
                </label>
                <input
                  id="last_name"
                  v-model="data.registerForm.last_name"
                  autocomplete="off"
                  class="form-control py-3 border-0 border-bottom border-3 shadow-none rounded-0"
                  placeholder="نام خانوادگی"
                  type="text"
                  @keyup="validateField('last_name', data.registerForm.last_name)"
                />
                <div v-if="data.errors.last_name" class="invalid-feedback d-block">
                  <i class="icon icon-regular-info-circle font-size-18"></i>
                  {{ data.errors.last_name }}
                </div>
              </div>
            </div>
            <div class="row mb-3">
              <div class="col-md-6 mb-3">
                <label class="form-label text-muted fw-bold d-flex align-items-center justify-content-start" for="email">
                  ایمیل
                </label>
                <input
                  id="email"
                  v-model="data.registerForm.email"
                  autocomplete="off"
                  class="form-control py-3 border-0 border-bottom border-3 shadow-none rounded-0"
                  placeholder="آدرس ایمیل خود را وارد کنید"
                  type="email"
                  @keyup="validateField('email', data.registerForm.email)"
                />
                <div v-if="data.errors.email" class="invalid-feedback d-block">
                  <i class="icon icon-regular-info-circle font-size-18"></i>
                  {{ data.errors.email }}
                </div>
              </div>
              <div class="col-md-6 mb-3">
                <label class="form-label text-muted fw-bold d-flex align-items-center justify-content-start" for="phone">
                  شماره تماس
                </label>
                <input
                  id="phone"
                  v-model="data.registerForm.phone"
                  autocomplete="off"
                  class="form-control py-3 border-0 border-bottom border-3 shadow-none rounded-0"
                  maxlength="11"
                  placeholder="شماره تماس خود را وارد کنید"
                  type="text"
                  @keyup="validateField('phone', data.registerForm.phone)"
                />
                <div v-if="data.errors.phone" class="invalid-feedback d-block">
                  <i class="icon icon-regular-info-circle font-size-18"></i>
                  {{ data.errors.phone }}
                </div>
              </div>
            </div>
            <div class="row mb-3">
              <div class="col-6 mb-3">
                <label class="form-label text-muted fw-bold d-flex align-items-center justify-content-start" for="password">
                  انتخاب رمز عبور
                </label>
                <input
                  id="password"
                  v-model="data.registerForm.password"
                  autocomplete="off"
                  class="form-control py-3 border-0 border-bottom border-3 shadow-none rounded-0"
                  placeholder="یک رمز عبور انتخاب کنید"
                  type="password"
                  @keyup="validateField('password', data.registerForm.password)"
                />
                <div v-if="data.errors.password" class="invalid-feedback d-block">
                  <i class="icon icon-regular-info-circle font-size-18"></i>
                  {{ data.errors.password }}
                </div>
              </div>
              <div class="col-6 mb-3">
                <label
                  class="form-label text-muted fw-bold d-flex align-items-center justify-content-start"
                  for="confirm_password"
                >
                  تکرار رمز عبور
                </label>
                <input
                  id="confirm_password"
                  v-model="data.registerForm.confirm_password"
                  autocomplete="off"
                  class="form-control py-3 border-0 border-bottom border-3 shadow-none rounded-0"
                  placeholder="تکرار رمز عبور"
                  type="password"
                  @keyup="validateField('confirm_password', data.registerForm.confirm_password)"
                />
                <div v-if="data.errors.confirm_password" class="invalid-feedback d-block">
                  <i class="icon icon-regular-info-circle font-size-18"></i>
                  {{ data.errors.confirm_password }}
                </div>
              </div>
            </div>

            <!-- File Upload Fields (Only for Organization and School) -->
            <div class="row mb-3 file-upload-section">
              <template v-if="data.userType === 'organization' || data.userType === 'school'">
                <div class="col-md-6 mb-3">
                  <label class="form-label text-muted fw-bold d-flex align-items-center justify-content-start" for="national_card">
                    کارت ملی <span class="text-danger">*</span>
                  </label>
                  <input
                    id="national_card"
                    ref="nationalCardInput"
                    type="file"
                    accept="image/*"
                    class="form-control py-3 border-0 border-bottom border-3 shadow-none rounded-0"
                    @change="handleFileSelect('national_card', $event)"
                  />
                  <div v-if="data.errors.national_card" class="invalid-feedback d-block">
                    <i class="icon icon-regular-info-circle font-size-18"></i>
                    {{ data.errors.national_card }}
                  </div>
                  <div v-if="data.registerForm.national_card" class="mt-2">
                    <small class="text-muted">
                      <i class="icon icon-regular-check text-success me-1"></i>
                      فایل انتخاب شده: {{ data.registerForm.national_card.name }}
                    </small>
                  </div>
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label text-muted fw-bold d-flex align-items-center justify-content-start" for="license">
                    مجوز <span class="text-danger">*</span>
                  </label>
                  <input
                    id="license"
                    ref="licenseInput"
                    type="file"
                    accept="image/*"
                    class="form-control py-3 border-0 border-bottom border-3 shadow-none rounded-0"
                    @change="handleFileSelect('license', $event)"
                  />
                  <div v-if="data.errors.license" class="invalid-feedback d-block">
                    <i class="icon icon-regular-info-circle font-size-18"></i>
                    {{ data.errors.license }}
                  </div>
                  <div v-if="data.registerForm.license" class="mt-2">
                    <small class="text-muted">
                      <i class="icon icon-regular-check text-success me-1"></i>
                      فایل انتخاب شده: {{ data.registerForm.license.name }}
                    </small>
                  </div>
                </div>
              </template>
              <!-- Placeholder space for user type to maintain consistent height -->
              <template v-else>
                <div class="col-md-6 mb-3">
                  <div class="file-upload-placeholder"></div>
                </div>
                <div class="col-md-6 mb-3">
                  <div class="file-upload-placeholder"></div>
                </div>
              </template>
            </div>

            <button
              class="btn btn-dark py-3 w-100 mt-3"
              type="button"
              @click="register"
              :disabled="submitting"
            >
              <span v-if="submitting" class="spinner-border spinner-border-sm me-2"></span>
              ثبت نام
            </button>
          </form>

          <!-- Login Form -->
          <form v-if="data.actionType === 'login'">
            <div class="mb-4">
              <label class="form-label text-muted fw-bold d-flex align-items-center justify-content-start" for="login-phone">
                شماره تماس
              </label>
              <input
                id="login-phone"
                v-model="data.loginForm.phone"
                autocomplete="off"
                class="form-control py-3 border-0 border-bottom border-3 shadow-none rounded-0"
                maxlength="11"
                placeholder="شماره تماس خود را وارد نمایید"
                type="text"
                @keyup="validateField('phone', data.loginForm.phone)"
              />
              <div v-if="data.errors.phone" class="invalid-feedback d-block">
                <i class="icon icon-regular-info-circle font-size-18"></i>
                {{ data.errors.phone }}
              </div>
            </div>
            <div id="collapseExample" class="collapse">
              <div class="mb-4">
                <label
                  class="form-label text-muted fw-bold d-flex align-items-center justify-content-start"
                  for="login-password"
                >
                  رمز عبور
                </label>
                <input
                  id="login-password"
                  v-model="data.loginForm.password"
                  autocomplete="off"
                  class="form-control py-3 border-0 border-bottom border-3 shadow-none rounded-0"
                  placeholder="رمز عبور خود را وارد کنید"
                  type="password"
                  @keyup="validateField('password', data.loginForm.password)"
                />
                <div v-if="data.errors.password" class="invalid-feedback d-block">
                  <i class="icon icon-regular-info-circle font-size-18"></i>
                  {{ data.errors.password }}
                </div>
              </div>
            </div>
            <a
              aria-controls="collapseExample"
              aria-expanded="false"
              class="text-danger1"
              data-bs-toggle="collapse"
              href="#collapseExample"
              role="button"
              @click="changeStatus"
            >
              ورود با
              {{
                data.loginForm.status === "code" ? "رمز عبور" : "کد یکبارمصرف"
              }}
            </a>
            <button
              class="btn btn-dark py-3 w-100 mt-2"
              type="button"
              @click="login"
            >
              ورود
            </button>
            
            <!-- Google Login Button -->
            <div class="mt-3 mb-3 text-center">
              <div class="position-relative">
                <hr class="my-3" />
                <span class="position-absolute top-50 start-50 translate-middle bg-white px-3 text-muted small">
                  یا
                </span>
              </div>
              <button
                class="btn btn-outline-danger py-3 w-100 mt-3 d-flex align-items-center justify-content-center gap-2 google-login-btn"
                type="button"
                @click="googleLogin"
              >
                <svg class="google-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
                  <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
                  <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/>
                  <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
                </svg>
                ورود با گوگل
              </button>
            </div>
          </form>
        </div>

        <!-- OTP Section (Step 2) -->
        <div v-if="data.step === 2 && data.actionType === 'login'">
          <div class="container my-5 d-flex flex-column align-items-center">
            <a
              class="d-flex align-items-center mb-3 cursor-pointer"
              @click="prevStep"
            >
              <i class="icon fw-light icon-regular-edit ms-1 text-danger1"></i>
              <span class="text-danger1 fw-bold">{{
                data.actionType === "register"
                  ? data.registerForm.phone
                  : data.loginForm.phone
              }}</span>
            </a>
            <p class="text-muted mb-3">کد ارسال شده را وارد کنید</p>
            <div class="d-flex justify-content-center gap-3 mb-4" style="direction: ltr !important;">
              <input
                v-for="(box, index) in 5"
                :id="'box-' + index"
                :key="index"
                v-model="data.otp[index]"
                autocomplete="off"
                class="form-control text-center border border-danger shadow-none"
                dir="ltr"
                maxlength="1"
                style="width: 50px; height: 50px; font-size: 1.5rem; direction: ltr !important;"
                type="text"
                @keyup="boxChange(index, $event)"
              />
            </div>
            <button
              :disabled="!isOtpComplete"
              class="btn btn-dark w-50 py-3 mb-2"
              @click="checkCode"
            >
              تایید کد فعالسازی
            </button>
            
            <p v-if="timer > 0" class="text-muted">
              تا ارسال مجدد کد
              <span class="fw-bold">{{ formattedTimer }}</span>
            </p>
            <button
              v-else
              class="btn btn-secondary w-50 py-2"
              @click="resendCode"
            >
              ارسال مجدد کد
            </button>
          </div>
        </div>

        <!-- Success Section (Step 2 for Register - Organization/School) -->
        <div v-if="data.step === 2 && data.actionType === 'register' && (data.userType === 'organization' || data.userType === 'school')">
          <div class="container my-5 d-flex flex-column align-items-center">
            <div class="text-center py-5">
              <div class="mb-4">
                <i class="icon icon-filled-check-circle text-success" style="font-size: 5rem;"></i>
              </div>
              <h3 class="fw-bold text-dark mb-4">ثبت نام با موفقیت انجام شد</h3>
              <p class="text-muted fs-5 mb-4">
                بعد از تایید شدن درخواست شما می‌توانید لاگین کنید.
              </p>
              <div class="d-flex gap-2 justify-content-center">
                <nuxt-link to="/" class="btn btn-outline-primary px-4">
                  <i class="icon icon-regular-home me-2"></i>
                  بازگشت به صفحه اصلی
                </nuxt-link>
                <button 
                  class="btn btn-primary px-4"
                  @click="goToLogin"
                >
                  <i class="icon icon-regular-login me-2"></i>
                  ورود به حساب کاربری
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Left Section -->
      <div class="col-md-6 d-flex align-items-center pt-5 w-50 bg-danger rounded-4 d-none d-md-block">
        <div class="text-center p-4">
          <img
            alt="Illustration"
            class="img-fluid"
            src="/images/auth/bg.png"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, reactive, ref, nextTick } from "vue";
import { useAuthStore } from "~/stores/auth";
import { useRoute, useRouter } from 'vue-router';
import { useOrganization } from "~/composables/useOrganization";

const { $sweetalert, $api } = useNuxtApp();
const route = useRoute();
const router = useRouter();

const authStore = useAuthStore();
const submitting = ref(false);
const data = reactive({
  userType: 'user', // 'user', 'organization', or 'school'
  step: 1,
  actionType: "login",
  registerForm: {
    first_name: "",
    last_name: "",
    email: "",
    phone: "",
    password: "",
    confirm_password: "",
    national_card: null,
    license: null,
  },
  loginForm: {
    phone: "",
    code: "",
    password: "",
    status: "code",
  },
  otp: Array(5).fill(""),
  errors: {
    first_name: "",
    last_name: "",
    phone: "",
    email: "",
    password: "",
    confirm_password: "",
    national_card: "",
    license: "",
  },
});

const changeUserType = (type) => {
  data.userType = type;
  resetForm();
  // Reset to login tab when changing user type
  data.actionType = 'login';
  data.step = 1;
};

const resetForm = () => {
  data.errors = {
    first_name: "",
    last_name: "",
    phone: "",
    email: "",
    password: "",
    confirm_password: "",
    national_card: "",
    license: "",
  };

  data.registerForm = {
    first_name: "",
    last_name: "",
    email: "",
    phone: "",
    password: "",
    confirm_password: "",
    national_card: null,
    license: null,
  };

  data.loginForm = {
    phone: "",
    code: "",
    password: "",
    status: "code",
  };
};

const handleFileSelect = (field, event) => {
  const file = event.target.files[0];
  if (file) {
    if (!file.type.startsWith('image/')) {
      data.errors[field] = 'لطفاً یک فایل تصویری انتخاب کنید';
      return;
    }
    if (file.size > 5 * 1024 * 1024) {
      data.errors[field] = 'حجم فایل نباید بیشتر از 5 مگابایت باشد';
      return;
    }
    data.registerForm[field] = file;
    data.errors[field] = '';
  }
};

const createError = () => {
  data.errors = {
    first_name: "",
    last_name: "",
    phone: "",
    email: "",
    password: "",
    confirm_password: "",
    national_card: "",
    license: "",
  };

  if (data.actionType === 'register') {
    validateField('first_name', data.registerForm.first_name);
    validateField('last_name', data.registerForm.last_name);
    validateField('email', data.registerForm.email);
    validateField('phone', data.registerForm.phone);
    validateField('password', data.registerForm.password);
    validateField('confirm_password', data.registerForm.confirm_password);
    
    if (data.userType === 'organization' || data.userType === 'school') {
      if (!data.registerForm.national_card) {
        data.errors.national_card = 'آپلود کارت ملی الزامی است';
      }
      if (!data.registerForm.license) {
        data.errors.license = 'آپلود مجوز الزامی است';
      }
    }
    
    if (data.userType === 'school') {
    }
  }

  if (data.actionType === 'login') {
    validateField('phone', data.loginForm.phone);
    if (data.loginForm.status === 'password') {
      validateField('password', data.loginForm.password);
    }
  }
};

const checkError = () => {
  let check = true;

  if (data.errors.first_name !== "") check = false;
  if (data.errors.last_name !== "") check = false;
  if (data.errors.phone !== "") check = false;
  if (data.errors.email !== "") check = false;
  if (data.errors.password !== "") check = false;
  if (data.errors.confirm_password !== "") check = false;
  if (data.errors.national_card !== "") check = false;
  if (data.errors.license !== "") check = false;

  return check;
};

const timer = ref(90);
let interval = null;

const isOtpComplete = computed(() => data.otp.every((digit) => digit !== ""));

const formattedTimer = computed(() => {
  const minutes = String(Math.floor(timer.value / 60)).padStart(2, "0");
  const seconds = String(timer.value % 60).padStart(2, "0");
  return `${minutes}:${seconds}`;
});

const changeStatus = () => {
  data.loginForm.status =
    data.loginForm.status === "password" ? "code" : "password";
};

const startTimer = () => {
  timer.value = 90;
  clearInterval(interval);
  interval = setInterval(() => {
    if (timer.value > 0) {
      timer.value--;
    } else {
      clearInterval(interval);
    }
  }, 1000);
};

const resendCode = () => {
  startTimer();
  loginCode();
};

const nextStep = () => {
  if (data.step < 2) {
    data.step++;
    if (data.step === 2) {
      startTimer();
    }
  }
};

const prevStep = () => {
  data.step--;
  if (data.step !== 2) {
    clearInterval(interval);
  }
};

const register = async () => {
  createError();
  if (checkError()) {
    submitting.value = true;
    try {
      if (data.userType === 'organization' || data.userType === 'school') {
        // Organization/School registration with file upload
        const formData = new FormData();
        formData.append('first_name', data.registerForm.first_name);
        formData.append('last_name', data.registerForm.last_name);
        formData.append('email', data.registerForm.email);
        formData.append('phone_number', data.registerForm.phone);
        formData.append('password', data.registerForm.password);
        formData.append('confirm_password', data.registerForm.confirm_password);
        formData.append('user_type', data.userType === 'school' ? 'school' : 'organization');
        formData.append('national_card', data.registerForm.national_card);
        formData.append('license', data.registerForm.license);

        const response = await $api.post("/auth/organization", formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });

        if (response.status >= 200 && response.status < 300) {
          if (response.data?.status === false) {
            const errors = response.data?.data?.errors;
            if (errors && errors.phone_number && errors.phone_number.length > 0) {
              $sweetalert.error("کاربری با این شماره تلفن از قبل وجود دارد");
            } else if (errors && errors.email && errors.email.length > 0) {
              $sweetalert.error("ایمیل از قبل وجود دارد");
            } else {
              $sweetalert.error('خطای غیرمنتظره رخ داده است.');
            }
          } else {
            // Success - show success page
            if (data.actionType === 'register') {
              data.step = 2;
              await nextTick();
            }
          }
        }
      } else {
        // Regular user registration
        const response = await $api.post("/auth/register", {
          first_name: data.registerForm.first_name,
          last_name: data.registerForm.last_name,
          email: data.registerForm.email,
          phone_number: data.registerForm.phone,
          password: data.registerForm.password,
          confirm_password: data.registerForm.confirm_password,
          user_type: data.registerForm.user_type || 'user',
        });

        data.loginForm.phone = data.registerForm.phone;
        loginCode();
      }
    } catch (error) {
      if (error.response) {
        const errors = error.response.data?.data?.errors;
        if (errors && errors.phone_number && errors.phone_number.length > 0) {
          $sweetalert.error("کاربری با این شماره تلفن از قبل وجود دارد");
        } else if (errors && errors.email && errors.email.length > 0) {
          $sweetalert.error("ایمیل از قبل وجود دارد");
        } else {
          $sweetalert.error('خطای غیرمنتظره رخ داده است.');
        }
      } else if (error.request) {
        $sweetalert.error('مشکل در ارسال درخواست به سرور');
      } else {
        $sweetalert.error('خطای غیرمنتظره رخ داده است.');
      }
    } finally {
      submitting.value = false;
    }
  }
};

const goToLogin = () => {
  data.actionType = 'login';
  data.step = 1;
  resetForm();
};

const checkCode = async () => {
  data.loginForm.code = data.otp.join("");
  const requestData = {
    phone_number: data.loginForm.phone,
    code: data.loginForm.code,
    login_type: data.userType === 'user' ? 'user' : 'organization',
  };
  
  $api
    .post("/auth/code/check", requestData)
    .then(async (value) => {
      if (value.data.status === false) {
        const errorMessage = value.data?.data?.error || 
                            value.data?.data?.message || 
                            "کد تأیید اشتباه است. لطفاً مجدداً تلاش کنید.";
        return $sweetalert.error(errorMessage);
      }
      authStore.setToken(value.data.data.token);
      await authStore.init();
      if (authStore.authenticated) {
        // Check school verification (backend already checks user type match)
        if (data.userType === 'school' && authStore.user) {
          await checkSchoolVerification();
        }
        
        if (authStore.user !== null && authStore.user.role === 'employee') {
          return router.push("/teacheraccount");
        } else {
          return router.push("/account");
        }
      }
    })
    .catch((error) => {
      if (error.response) {
        const errorMessage = error.response.data?.data?.error || 
                            error.response.data?.data?.message || 
                            error.response.data?.message || 
                            "کد تأیید اشتباه است. لطفاً مجدداً تلاش کنید.";
        $sweetalert.error(errorMessage);
      } else {
        $sweetalert.error("خطایی رخ داده است. لطفاً بعداً امتحان کنید.");
      }
    });
};

// Check school verification status
const checkSchoolVerification = async () => {
  try {
    const { fetchOrganization } = useOrganization();
    const organization = await fetchOrganization();
    
    if (organization && !organization.is_verified) {
      await $sweetalert.fire({
        title: 'حساب کاربری شما تایید نشده است',
        html: `
          <div class="text-right">
            <p>حساب کاربری آموزشگاه شما هنوز توسط مدیر سیستم تایید نشده است.</p>
            <p class="text-muted">دسترسی شما محدود است و برخی از امکانات در دسترس نیست.</p>
            <p class="text-muted">لطفاً منتظر تایید حساب کاربری خود باشید.</p>
          </div>
        `,
        icon: 'warning',
        confirmButtonText: 'متوجه شدم',
        confirmButtonColor: '#dc3545'
      });
    }
  } catch (error) {
    console.error('Error checking school verification:', error);
  }
};

const validate = (input, type) => {
  if (type === "first_name") {
    if (input.length === 0) {
      return "وارد کردن نام الزامی می باشد.";
    }
  }
  if (type === "last_name") {
    if (input.length === 0) {
      return "وارد کردن نام خانوادگی الزامی می باشد.";
    }
  }
  if (type === "phone") {
    if (input.length > 0) {
      const regex = /^09\d{9}$/;
      if (!regex.test(input)) return "شماره موبایل صحیح نیست.";
    } else {
      return "وارد کردن شماره موبایل الزامی می باشد.";
    }
  }
  if (type === "email") {
    if (input.length > 0) {
      const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!regex.test(input)) return "ایمیل صحیح نیست.";
    } else {
      return "وارد کردن ایمیل الزامی می باشد.";
    }
  }
  if (type === "password") {
    if (input.length > 0) {
      if (input.length < 6) return "رمز عبور باید حداقل ۶ کاراکتر باشد.";
    } else {
      return "وارد کردن رمز عبور الزامی می باشد.";
    }
  }
  if (type === "confirm_password") {
    if (input.length > 0) {
      if (input !== data.registerForm.password)
        return "رمز عبور و تکرار آن مطابقت ندارند.";
    } else {
      return "وارد کردن تکرار رمز عبور الزامی می باشد.";
    }
  }
  return "";
};

const validateField = (field, value) => {
  data.errors[field] = validate(value, field);
};

const boxChange = (index, event) => {
  const currentBox = document.getElementById(`box-${index}`);
  const nextBox = document.getElementById(`box-${index + 1}`);
  const prevBox = document.getElementById(`box-${index - 1}`);

  if (event.key === "Backspace" || event.key === "Delete") {
    if (currentBox.value === "" && prevBox) {
      prevBox.focus();
    }
    return;
  }

  if (currentBox.value !== "" && nextBox) {
    nextBox.focus();
  }

  if (index === 0 && event.key === "Backspace") {
    currentBox.value = "";
  }

  if (index === 4 && currentBox.value !== "" && event.key !== "Backspace" && event.key !== "Delete") {
    currentBox.blur();
  }
};

const loginPassword = async () => {
  createError();
  if (checkError()) {
    const requestData = {
      phone_number: data.loginForm.phone,
      password: data.loginForm.password,
      login_type: data.userType === 'user' ? 'user' : 'organization',
    };
    
    $api
      .post("/auth/login", requestData)
      .then(async (value) => {
        if (value.status === 200 && value.data.status === false) {
          const errorMessage = value.data?.data?.error || 
                              value.data?.data?.message || 
                              "شماره تماس یا رمزعبور اشتباه است";
          return $sweetalert.error(errorMessage);
        }
        authStore.setToken(value.data.data.token);
        await authStore.init();
        if (authStore.authenticated) {
          // Check school verification (backend already checks user type match)
          if (data.userType === 'school' && authStore.user) {
            await checkSchoolVerification();
          }
          
          return router.push("/account");
        }
      })
      .catch((error) => {
        if (error.response) {
          const errorMessage = error.response.data?.data?.error || 
                              error.response.data?.data?.message || 
                              error.response.data?.message || 
                              "شماره تماس یا رمزعبور اشتباه است.";
          $sweetalert.error(errorMessage);
        } else {
          $sweetalert.error("خطایی رخ داده است. لطفاً بعداً امتحان کنید.");
        }
      });
  }
};

const loginCode = () => {
  createError();
  if (checkError()) {
    const requestData = {
      phone_number: data.loginForm.phone,
      login_type: data.userType === 'user' ? 'user' : 'organization',
    };
    
    $api
      .post("/auth/code/send", requestData)
      .then((value) => {
        if (value.data.status) {
          // //in halat ro bardaram az test mode
          // if (value.data.data.development_mode && value.data.data.code) {
          //   $sweetalert.success(`کد تأیید: ${value.data.data.code}`, {
          //     title: "حالت توسعه - کد تأیید",
          //     timer: 10000,
          //     showConfirmButton: true
          //   });
          // }
          nextStep();
        } else {
          // Handle case when status is false
          const errorMessage = value.data?.data?.error || value.data?.message || 'خطایی رخ داده است.';
          $sweetalert.error(errorMessage);
        }
      })
      .catch((error) => {
        if (error.response) {
          const errorMessage = error.response.data?.data?.error || 
                              error.response.data?.data?.message || 
                              error.response.data?.message || 
                              'کاربری با این شماره تماس یافت نشد.';
          $sweetalert.error(errorMessage);
        } else {
          $sweetalert.error('خطایی رخ داده است. لطفاً بعداً امتحان کنید.');
        }
      });
  }
};

const login = async () => {
  if (data.loginForm.status === "code") {
    loginCode();
  } else {
    loginPassword();
  }
};

const googleLogin = () => {
  const config = useRuntimeConfig();
  const redirectUri = `${window.location.origin}/auth/google/callback`;
  const googleAuthUrl = `${config.public.apiBaseUrl}auth/google/login?redirect_uri=${encodeURIComponent(redirectUri)}`;
  
  // هدایت کاربر به backend که باید کاربر را به Google OAuth redirect کند
  window.location.href = googleAuthUrl;
};

onMounted(() => {
  if (data.step === 2) {
    startTimer();
  }
  const action = route.query.action;
  const type = route.query.type;
  
  if (type === 'organization') {
    data.userType = 'organization';
  }
  
  if (action === 'login') {
    data.actionType = 'login';
  } else if (action === 'register') {
    data.actionType = 'register';
  }
});

onBeforeUnmount(() => {
  clearInterval(interval);
});

definePageMeta({
  layout: "auth"
})
</script>

<style scoped>
.custom-tabs {
  display: flex;
  background-color: #fff;
  border: none;
  overflow: hidden;
  gap: 8px;
}

.nav-item {
  flex: 1;
  display: flex;
}

.nav-item.ms-2 {
  margin-right: 0;
}

.custom-tab {
  flex: 1;
  padding: 10px 0;
  text-align: center;
  font-size: 16px;
  font-weight: bold;
  background-color: transparent;
  border: none;
  transition: all 0.3s ease;
}

.bg-danger {
  background-color: #FF8C14 !important;
}

.border-danger {
  border-color: #FF8C14 !important;
}

.custom-tab:hover {
  background-color: #FF8C14 !important;
  color: #ffffff !important;
}

.custom-tab.active {
  background-color: #FF8C14 !important;
  color: #ffffff !important;
}

.user-type-icon-card {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 10px 6px;
  border: 2px solid #dee2e6;
  border-radius: 10px;
  background-color: #ffffff;
  cursor: pointer;
  transition: all 0.3s ease;
  min-width: 70px;
  max-width: 90px;
}

.user-type-icon-card:hover {
  border-color: #FF8C14;
  background-color: #fff5f5;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(255, 140, 20, 0.15);
}

.user-type-icon-card.active {
  border-color: #FF8C14;
  background-color: #FF8C14;
  box-shadow: 0 4px 12px rgba(255, 140, 20, 0.3);
}

.user-type-icon-card.active .icon-wrapper {
  background-color: #ffffff;
  color: #FF8C14;
}

.user-type-icon-card.active .icon-label {
  color: #ffffff !important;
}

.user-type-icon-card.active .icon-wrapper i {
  color: #FF8C14 !important;
}

.icon-wrapper {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f8f9fa;
  border-radius: 50%;
  margin-bottom: 6px;
  transition: all 0.3s ease;
}

.user-type-icon-card:hover .icon-wrapper {
  background-color: #FF8C14;
  color: #ffffff;
  transform: scale(1.1);
}

.icon-wrapper .icon,
.icon-wrapper i.icon {
  font-size: 16px !important;
  color: #495057 !important;
  transition: all 0.3s ease;
  line-height: 1 !important;
  vertical-align: middle !important;
}

.user-type-icon-card .icon-wrapper .icon:before {
  font-size: 16px !important;
}

.icon-wrapper i {
  font-size: 18px !important;
  color: #495057;
  transition: all 0.3s ease;
  line-height: 1;
}

.user-type-icon-card:hover .icon-wrapper i {
  color: #ffffff;
}

.icon-label {
  font-size: 11px;
  font-weight: 600;
  color: #495057;
  transition: all 0.3s ease;
  text-align: center;
  line-height: 1.2;
}

.user-type-icon-card:hover .icon-label {
  color: #FF8C14;
}

.text-success {
  color: #28a745 !important;
}

.btn-primary {
  background-color: #FF8C14;
  border-color: #FF8C14;
}

.btn-primary:hover {
  background-color: #E67A0F;
  border-color: #D66A0A;
}

.btn-outline-primary {
  color: #FF8C14;
  border-color: #FF8C14;
}

.btn-outline-primary:hover {
  background-color: #FF8C14;
  border-color: #FF8C14;
  color: #fff;
}

.btn-outline-danger {
  color: #FF8C14;
  border-color: #FF8C14;
}

.btn-outline-danger:hover {
  background-color: #FF8C14;
  border-color: #FF8C14;
  color: #fff;
}

/* Fix form height to prevent layout shift */
.form-container {
  min-height: 650px;
  display: flex;
  flex-direction: column;
}

.auth-form {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.file-upload-section {
  min-height: 140px;
}

.file-upload-placeholder {
  min-height: 120px;
  visibility: hidden;
  pointer-events: none;
}

/* Ensure consistent height for register forms */
form.auth-form {
  min-height: 580px;
}

/* Google Login Button Icon Styling */
.google-login-btn {
  position: relative;
}

.google-icon {
  width: 20px;
  height: 20px;
  display: inline-block;
  flex-shrink: 0;
  transition: transform 0.3s ease;
}

.google-login-btn:hover .google-icon {
  transform: scale(1.1);
}
</style>
