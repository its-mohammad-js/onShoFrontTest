<template>
   <div class="container py-5">
  <!-- لودینگ -->
  <div v-if="data.loading" class="text-center py-5">
    <div class="spinner-border spinner-grow text-danger1" role="status">
      <span class="visually-hidden">در حال بارگذاری...</span>
    </div>
  </div>

  <!-- Courses Section -->
  <div v-else>
    <div v-if="data.courses.length === 0" class="card mb-4 bg-light">
      <div
        class="card-header border-bottom-0 shadow-none bg-light d-flex align-items-center justify-content-between py-3"
      >
        <h5 class="mb-0 text-dark">لیست دوره‌های شما</h5>
      </div>
      <div
        class="card-body min-vh-25 d-flex flex-column justify-content-between"
      >
        <table class="table table-striped">
          <thead class="bg-white rounded">
            <tr class="text-center">
              <th>نام دوره</th>
              <th>عملیات</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td
                colspan="2"
                class="text-center fw-bold shadow-none bg-light border-bottom-0 py-5"
              >
                <span class="d-dlex align-items-center fs-5">
                  <i
                    class="fa-solid fa-triangle-exclamation ms-2 text-warning fs-3"
                  ></i>
                  هنوز دوره‌ای ثبت نکرده‌اید.
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div v-else class="card mb-4 bg-light">
      <!-- Header Section -->
      <div
        class="card-header border-bottom-0 shadow-none bg-light d-flex align-items-center justify-content-between py-3"
      >
        <h5 class="mb-0 text-dark">لیست دوره‌های شما</h5>
      </div>

      <!-- Body Section -->
      <div
        class="card-body min-vh-25 d-flex flex-column justify-content-between"
      >
        <div class="table-responsive">
          <table class="table">
            <thead class="bg-white rounded">
              <tr class="text-center">
                <th class="text-end">نام دوره</th>
                <th>قیمت</th>
                <th>مدت زمان</th>
                <th>زبان</th>
                <th>عملیات</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="(course, index) in data.courses"
                :key="index"
                class="align-middle bg-light"
              >
                <td class="bg-light">
                  <div class="d-flex align-items-center py-3 flex-wrap">
                    <img
                      :src="getMediaUrl(course.image) || 'https://via.placeholder.com/60'"
                      alt="Course Image"
                      class="rounded w-100-px h-75-px object-fit-cover"
                    />
                    <div class="me-3 mt-2">
                      <div>
                        <span class="text-muted small">برگزار کننده :</span>
                        <span class="text-danger1 small">{{ course.organizer.name }}</span>
                      </div>
                      <h6 class="fw-bold mt-2">{{ course.title }}</h6>
                    </div>
                  </div>
                </td>
                <td class="text-center bg-light">{{ course.price }} تومان</td>
                <td class="text-center bg-light">{{ course.duration }} ساعت</td>
                <td class="text-center bg-light">{{ course.language }}</td>
                <td class="text-center bg-light">
                  <nuxt-link
                  :to="`/account/edit/${course.id}`"
                    class="btn btn-warning text-white btn-sm ms-0 mb-1 mb-lg-0 ms-md-2"
                  >
                    <i class="fa-solid fa-edit ms-1"></i>
                    <span class="d-none d-md-inline">ویرایش</span>
                  </nuxt-link>
                  <button
                    class="btn btn-danger btn-sm"
                    @click="removeCourse(index)"
                  >
                    <i class="fa-solid fa-trash-alt ms-1"></i>
                    <span class="d-none d-md-inline">حذف</span>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</div>
  </template>
  
  <script setup>
  import { reactive, onMounted } from "vue";
  import { useNuxtApp } from "#app";
  
  const { $api, $sweetalert } = useNuxtApp();
  const { getMediaUrl } = useMediaUrl();
  
  const data = reactive({
    loading: true,
    courses: [],
  });
  
  const getCourses = () => {
    data.loading = true;
    $api
      .post(
        "/course/modares/list",
        {},
        {
          headers: {
            Authorization: "Bearer " + useCookie("token").value,
          },
        }
      )
      .then((response) => {
        console.log("API Response:", response.data);
        data.courses = response.data.data.results || []; // مقداردهی لیست دوره‌ها
      })
      .catch((error) => {
        console.error("خطا در دریافت لیست دوره‌ها:", error);
        $sweetalert.error("خطایی در دریافت لیست دوره‌ها رخ داده است.");
      })
      .finally(() => {
        data.loading = false; // پایان لودینگ
      });
  };
  
  // اجرا در زمان لود شدن صفحه
  onMounted(() => {
    getCourses();
  });

  definePageMeta({
  layout: "account",
  middleware: ['auth']
});
  </script>
  
  <style scoped>
  .card {
    transform: scale(1) !important;
  }

  
  .table-responsive {
    overflow-x: auto;
  }
  
  @media (max-width: 768px) {
    .w-100-px {
      width: 50px !important;
    }
    .h-75-px {
      height: 50px !important;
    }
    td {
      font-size: 14px;
    }
    .btn {
      font-size: 12px;
      padding: 5px 10px;
    }
  }
  </style>
  