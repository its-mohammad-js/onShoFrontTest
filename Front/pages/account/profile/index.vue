<template>
    <div class="card my-4 bg-light py-4">
    <div class="container">
  
        <div class="row justify-content-center">
          <!-- Personal Information -->
          <div class="col-md-12">
            <h6 class="fw-bold text-end">اطلاعات شخصی</h6>
            <div class="row gap-5 justify-content-center">
              <!-- Name -->
              <div class="col-md-5 my-1 my-md-2 my-lg-3">
                <div class="d-flex align-items-center justify-content-between">
                  <label class="form-label text-end text-muted" for="fname"
                  >نام</label
                  >
                  <i :class="{'d-none': data.edit}" class="icon fw-light icon-regular-edit text-danger1 cursor-pointer"
                     @click="editUser"></i>
                </div>
  
                <input
                    id="fname"
                    v-model="data.form.first_name"
                    :disabled="!data.edit"
                    class="form-control bg-light border-2 py-3 shadow-none"
                    type="text"
                />
              </div>
  
              <div class="col-md-5 my-1 my-md-2 my-lg-3">
                <div class="d-flex align-items-center justify-content-between">
                  <label class="form-label text-end text-muted" for="lname"
                  >نام خانوادگی</label
                  >
                  <i :class="{'d-none': data.edit}" class="icon fw-light icon-regular-edit text-danger1 cursor-pointer"
                     @click="editUser"></i>
                </div>
  
                <input
                    id="lname"
                    v-model="data.form.last_name"
                    :disabled="!data.edit"
                    class="form-control bg-light border-2 py-3 shadow-none"
                    type="text"
                />
              </div>
  
              <!-- Phone Number -->
              <div class="col-md-5 my-1 my-md-2 my-lg-3">
                <div class="d-flex align-items-center justify-content-between">
                  <label class="form-label text-end text-muted" for="phone"
                  >شماره تماس</label
                  >
  
                </div>
  
                <input
                    id="phone"
                    v-model="data.form.phone"
                    class="form-control bg-light border-2 py-3 shadow-none"
                    disabled
                    type="text"
                />
              </div>
  
              <div class="col-md-5 my-1 my-md-2 my-lg-3">
                <div class="d-flex align-items-center justify-content-between">
                  <label class="form-label text-end text-muted" for="email"
                  >ایمیل</label
                  >
                  <i :class="{'d-none': data.edit}" class="icon fw-light icon-regular-edit text-danger1 cursor-pointer"
                     @click="editUser"></i>
                </div>
  
                <input
                    id="email"
                    v-model="data.form.email"
                    :disabled="!data.edit"
                    class="form-control bg-light border-2 py-3 shadow-none"
                    type="email"
                />
            </div>
            </div>
          </div>
        </div>
        <div class="row justify-content-center gap-5 my-5">
          <div class="col-md-5">
          </div>
          <div class="col-md-5">
            <button class="btn btn-danger d-block w-100 py-3" type="button" @click="editData">ذخیره</button>
          </div>
        </div>
        </div>
        </div>
  </template>
  
  <script setup>
  import {useAuthStore} from "~/stores/auth";
  
  const authStore = useAuthStore();
  const {$api, $sweetalert} = useNuxtApp();
  const data = reactive({
    edit: false,
    form: {
      first_name: '',
      last_name: '',
      phone: '',
      email: '',
    },
  })
  const editUser = () => {
    data.edit = !data.edit;
  }
  definePageMeta({
    layout: "account",
    middleware: ['auth']
  });
  
  
  
  onMounted(() => {
    setTimeout(() => {
      data.form.first_name = authStore.user.first_name;
      data.form.last_name = authStore.user.last_name;
      data.form.phone = authStore.user.phone_number;
      data.form.email = authStore.user.email;
    }, 750);
  });
  
 
  const editData = async () => {
    await $api.post('/auth/edit', data.form, {
      headers: {
        Authorization: 'Bearer ' + useCookie('token').value
      }
    }).then((value) => {
      (value.data)
      $sweetalert.success('تغییرات با موفقیت انجام شد .')
    })
  }
  
  </script>
  <style scoped>
  .bg-white {
    min-height: 45vh;
  }
  
  .border-dashed {
    border: 2px dashed #ddd !important;
    border-radius: 8px;
  }
  
  .form-control:disabled {
    background-color: #f8f9fa !important;
    cursor: not-allowed;
  }
  
  .text-end {
    direction: rtl;
    text-align: end;
  }
  
  .cursor-pointer {
    cursor: pointer;
  }
  .card {
    transform: scale(1) !important;
  }
  </style>
  