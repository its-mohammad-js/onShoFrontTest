<template>
    <div class="container py-5">
      <!-- Feedback Section -->
      <div v-if="courses.length === 0" class="card mb-4 bg-light">
        <div
          class="card-header border-bottom-0 shadow-none bg-light d-flex align-items-center justify-content-between py-3"
        >
          <h5 class="mb-0 text-dark">
            <i class="fas fa-comment-dots ms-1 text-danger1 fs-4"></i> ثبت بازخورد دوره‌ها
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
                  <span class="d-dlex align-items-center fs-5"><i class="fa-solid fa-triangle-exclamation ms-2 text-warning fs-3"></i> هنوز دوره‌ای برای بازخورد ثبت نشده است.</span>
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
          <h5 class="mb-0 text-dark">
           <i class="icon icon-filled-comment-dots text-dark fs-4"></i> ثبت بازخورد دوره‌ها
          </h5>
        </div>
  
        <!-- Body Section -->
        <div class="card-body min-vh-25 d-flex flex-column justify-content-between">
          <div class="d-none d-md-block">
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
                  <nuxtLink
                  :to="`/account/feedback/${course.id}`"
                    class="btn btn-success btn-sm"
                  >
                  <i class="icon icon-filled-pen"></i>  ثبت بازخورد
                  </nuxtLink>
                </td>
              </tr>
            </tbody>
          </table>
          </div>
          <div class="d-block d-md-none">
  <div v-for="(course, index) in courses" :key="index" class="course-card">
   
      <div class="course-image">
        <img :src="getMediaUrl(course.image)" alt="Course Image" class="w-100 h-100 object-fit-cover rounded">
        <div class="course-overlay">
          <h6 class="fw-bold text-white">{{ course.title }}</h6>
        </div>
      </div>
   

    <!-- اطلاعات تکمیلی دوره -->
    <div class="course-info p-3">
      <p class="text-muted small mb-1">برگزار کننده: <span class="text-danger1">{{ course.organizer }}</span></p>

      <nuxtLink
                  :to="`/account/feedback/${course.id}`"
                    class="btn btn-success btn-sm"
                  >
                  <i class="icon icon-filled-pen"></i>  ثبت بازخورد
                  </nuxtLink>
    </div>
  </div>
</div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
import { ref, onMounted } from "vue";
import { useAuthStore } from "~/stores/auth";

const authStore = useAuthStore();

const { $api } = useNuxtApp();
const { getMediaUrl } = useMediaUrl();
const courses = ref([]);
const purchasedCourses = ref(0);
const inProgressCourses = ref(0);
const completedCourses = ref(0);

const fetchCourses = async () => {
  const token = useCookie("token").value;
  if (!token) {
    return;
  }

  try {
    const response = await $api.post("/course/user/list", {}, {
      headers: {
        Authorization: "Bearer " + token,
      },
    });

    if (response.data.status && response.data.data.results) {
      courses.value = response.data.data.results.map(item => ({
        id: item.course.id, // باید از `course` مقدار `id` را بگیریم
        title: item.course.title, // عنوان دوره از `course`
        organizer: item.course.organizer?.name || "نامشخص", // بررسی وجود `organizer`
        image: item.course.image || "/default-image.jpg", // بررسی وجود تصویر و مقدار پیش‌فرض
        slug: item.course.slug || "", // مقدار `slug` در صورت وجود
        progress: {
          completed: 0,
          total: 100,
          percentage: 0,
        },
        status: item.status === "completed" ? "تکمیل شده" : "در حال اجرا",
      }));

      purchasedCourses.value = courses.value.length;
      inProgressCourses.value = courses.value.filter(course => course.status === "در حال اجرا").length;
      completedCourses.value = courses.value.filter(course => course.status === "تکمیل شده").length;
    }
  } catch (error) {
    console.error(error.response?.data?.detail || "خطا در دریافت اطلاعات دوره‌ها.");
  }
};


onMounted(fetchCourses);

definePageMeta({
  layout: "account",
  middleware: ["auth"],
});
</script>
  
  <style scoped>
  .card {
    transform: scale(1) !important;
  }
  .card-title i {
    font-size: 1.5rem;
  }
  @media (max-width: 768px) {
  /* مخفی کردن جدول در موبایل */
  .table {
    display: none;
  }

  /* استایل کارت دوره‌ها در موبایل */
  .course-card {
    display: flex;
    flex-direction: column;
    background: white;
    border-radius: 10px;
    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
    margin-bottom: 15px;
    overflow: hidden;
  }

  /* تصویر دوره */
  .course-image {
    position: relative;
    width: 100%;
    height: 200px;
  }

  .course-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  /* لایه شفاف روی تصویر */
  .course-overlay {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    background: rgba(0, 0, 0, 0.5);
    color: white;
    padding: 10px;
    text-align: center;
    font-weight: bold;
  }

  /* اطلاعات دوره */
  .course-info {
    text-align: center;
    padding: 15px;
  }

  .progress-container {
    text-align: center;
  }

  .progress {
    height: 6px;
    border-radius: 5px;
    background-color: #e9ecef;
    overflow: hidden;
  }

  .progress-bar {
    height: 100%;
    transition: width 0.5s ease-in-out;
  }

  .badge {
    font-size: 14px;
    padding: 8px 12px;
    display: inline-block;
  }
}  /* بررسی کنید که این } به درستی بسته شده باشد */

  </style>
  