<template>
  <div class="border rounded p-4 bg-white mt-4">
    <div class="row">
      <div class="col-md-6">
        <!-- Title -->
        <h5 class="text-end fw-bold mb-4">تغییر رمز عبور</h5>

        <!-- Old Password Field -->
        <div class="mb-3">
          <div class="d-flex align-items-center justify-content-between">
            <label class="form-label text-end w-100" for="old-password">
              رمز عبور قبلی
            </label>
            <i
                :class="[{'icon-regular-eye-slash':data.oldPasswordVisible},{'icon-regular-eye':!data.oldPasswordVisible}]"
                class="icon fw-light text-danger1 cursor-pointer"
                @click="togglePasswordVisibility('oldPasswordVisible')"
            ></i>
          </div>

          <input
              id="old-password"
              v-model="data.form.oldPassword"
              :type="data.oldPasswordVisible ? 'text' : 'password'"
              class="form-control bg-light border-2 py-3"
              placeholder="رمز عبور قبلی"
          />
        </div>

        <!-- New Password Field -->
        <div class="mb-3">
          <div class="d-flex align-items-center justify-content-between">
            <label class="form-label text-end w-100" for="new-password">
              رمز عبور جدید
            </label>
            <i
                :class="[{'icon-regular-eye-slash':data.newPasswordVisible},{'icon-regular-eye':!data.newPasswordVisible}]"
                class="icon fw-light text-danger1 cursor-pointer"
                @click="togglePasswordVisibility('newPasswordVisible')"
            ></i>
          </div>

          <input
              id="new-password"
              v-model="data.form.newPassword"
              :type="data.newPasswordVisible ? 'text' : 'password'"
              class="form-control bg-light border-2 py-3"
              placeholder="رمز جدید"
              @keyup="validateField('newPassword')"
          />
          <div v-if="data.errors.newPassword" class="text-danger1">
            {{ data.errors.newPassword }}
          </div>
        </div>

        <!-- Confirm Password Field -->
        <div class="mb-3">
          <div class="d-flex align-items-center justify-content-between">
            <label class="form-label text-end w-100" for="confirm-password">
              تکرار رمز عبور جدید
            </label>
            <i
                :class="[{'icon-regular-eye-slash':data.confirmPasswordVisible},{'icon-regular-eye':!data.confirmPasswordVisible}]"
                class="icon fw-light text-danger1 cursor-pointer"
                @click="togglePasswordVisibility('confirmPasswordVisible')"
            ></i>
          </div>

          <input
              id="confirm-password"
              v-model="data.form.confirmPassword"
              :type="data.confirmPasswordVisible ? 'text' : 'password'"
              class="form-control bg-light border-2 py-3"
              placeholder="تکرار رمز جدید"
              @keyup="validateField('confirmPassword')"
          />
          <div v-if="data.errors.confirmPassword" class="text-danger1">
            {{ data.errors.confirmPassword }}
          </div>
        </div>

        <!-- Submit Button -->
        <button
            :disabled="!isFormValid"
            class="btn btn-primary px-4 py-2"
            @click="editData"
        >
          ثبت تغییرات
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import {computed, reactive} from "vue";
import {useAuthStore} from "~/stores/auth";

const authStore = useAuthStore();
const {$api, $sweetalert} = useNuxtApp();

// شیء reactive برای مدیریت فرم و وضعیت نمایش رمزها
const data = reactive({
  form: {
    oldPassword: "",
    newPassword: "",
    confirmPassword: "",
  },
  oldPasswordVisible: false,
  newPasswordVisible: false,
  confirmPasswordVisible: false,
  errors: {
    newPassword: "",
    confirmPassword: "",
  },
});

// تابع برای تغییر وضعیت نمایش رمز عبور
const togglePasswordVisibility = (field) => {
  data[field] = !data[field];
};

// اعتبارسنجی فیلدها
const validateField = (field) => {
  const value = data.form[field];
  if (field === "newPassword") {
    data.errors.newPassword =
        value.length < 6 ? "رمز عبور باید حداقل 8 کاراکتر باشد." : "";
  } else if (field === "confirmPassword") {
    data.errors.confirmPassword =
        value !== data.form.newPassword ? "رمز عبور و تکرار آن مطابقت ندارند." : "";
  }
};

// بررسی اعتبار کل فرم
const isFormValid = computed(() => {
  return (
      data.form.newPassword.length >= 6 &&
      data.form.newPassword === data.form.confirmPassword &&
      data.form.oldPassword !== ""
  );
});

// تابع ارسال داده‌های فرم
const editData = async () => {
  await $api
      .post("/auth/password", data.form, {
        headers: {
          Authorization: "Bearer " + useCookie("token").value,
        },
      })
      .then((value) => {
        $sweetalert.success("رمز عبور با موفقیت تغییر کرد.");
      })
      .catch(() => {
        $sweetalert.error("اطلاعات به درستی وارد نشده است");
      });
};

definePageMeta({
  layout: "account",
  middleware: ['auth']
});
</script>

<style scoped>
.bg-white {
  min-height: 45vh;
}

.cursor-pointer {
  cursor: pointer;
}

.icon {
  font-size: 1.2rem;
}

.input[disabled] {
  background-color: #f8f9fa !important;
  cursor: not-allowed;
}

.form-label {
  direction: rtl;
  text-align: right;
}

.btn {
  font-size: 1rem;
  font-weight: bold;
}
</style>
