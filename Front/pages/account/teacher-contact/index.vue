<template>
    <div class="container py-5">
      <div v-if="courses.length === 0" class="card mb-4 bg-light">
        <div
          class="card-header border-bottom-0 shadow-none bg-light d-flex align-items-center justify-content-between py-3"
        >
        <h5 class="mb-0 text-dark">
            <i class="icon icon-filled-comment-dots fs-3 text-dark"></i> ارتباط با مدرس دوره‌ها
          </h5>
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
                  <span class="d-dlex align-items-center fs-5"><i class="fa-solid fa-triangle-exclamation ms-2 text-warning fs-3"></i> هنوز دوره‌ای برای ارتباط با مدرس ثبت نشده است.</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
  
      <div v-else class="card mb-4 bg-light">
        <div
          class="card-header border-bottom-0 shadow-none bg-light d-flex align-items-center justify-content-between py-3"
        >
          <h5 class="mb-0 text-dark">
            <i class="icon icon-filled-comment-dots fs-3 text-dark"></i> ارتباط با مدرس دوره‌ها
          </h5>
        </div>
  
        <div class="card-body min-vh-25 d-flex flex-column justify-content-between">
          <table class="table">
            <thead class="bg-white rounded">
              <tr class="text-center">
                <th class="text-end">نام دوره</th>
                <th>عملیات</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="(course, index) in courses"
                :key="index"
                class="align-middle bg-light"
              >
                <td class="bg-light">
                  <div class="d-flex align-items-center py-3">
                    <img
                      :src="getMediaUrl(course.image)"
                      alt="Course Image"
                      class="rounded w-100-px h-75-px object-fit-cover"
                    />
                    <div class="me-3">
                      <div>
                        <span class="text-muted small">برگزار کننده :</span>
                        <span class="text-danger1 small">{{ course.organizer }}</span>
                      </div>
                      <h6 class="fw-bold mt-2">{{ course.title }}</h6>
                    </div>
                  </div>
                </td>
                <td class="text-center bg-light">
                  <button
                    class="btn btn-primary btn-sm"
                  >
                  <i class="icon icon-regular-envelope text-white"></i> ارتباط با مدرس
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from "vue";
  
  const { getMediaUrl } = useMediaUrl();
  
  const courses = ref([
    {
      title: "دوره آموزشی HTML, CSS",
      organizer: "های وب",
      image: "https://via.placeholder.com/60",
    },
    {
      title: "دوره آموزشی جاوااسکریپت",
      organizer: "های وب",
      image: "https://via.placeholder.com/60",
    },
    {
      title: "دوره آموزشی React",
      organizer: "های وب",
      image: "https://via.placeholder.com/60",
    },
  ]);
  
 
  definePageMeta({
  layout: "account",
  middleware: ['auth']
});
  </script>
  
  <style scoped>
  .card {
    transform: scale(1) !important;
  }
  .card-title i {
    font-size: 1.5rem;
  }
  </style>
  