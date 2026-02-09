<template>
  <div class="container py-5">
    <!-- Tabs Section -->
    <div class="row mb-4">
  <!-- دوره‌های خریداری‌شده (برای دانشجو) یا دوره‌های ایجادشده (برای مدرس) -->
  <div class="col-lg-4 col-md-4 mb-3">
    <div class="card border-none shadow-none bg-light h-100">
      <div class="card-body d-flex align-items-center justify-content-between">
        <div class="card-title text-muted">
          <h4 class="mb-3 text-dark">{{ purchasedCourses }}</h4>
          <p v-if="authStore.user?.role === 'مدرس'">دوره‌های ایجاد شده</p>
          <p v-else>دوره‌های خریداری شده</p>
        </div>
        <div class="p-2 w-40-px h-40-px bg-danger rounded-circle d-flex align-items-center justify-content-center">
          <i class="fas fa-wallet text-white"></i>
        </div>
      </div>
    </div>
  </div>

  <!-- دوره‌های درحال اجرا -->
  <div class="col-lg-4 col-md-4 mb-3">
    <div class="card border-none shadow-none bg-light h-100">
      <div class="card-body d-flex align-items-center justify-content-between">
        <div class="card-title text-muted">
          <h4 class="mb-3 text-dark">{{ inProgressCourses }}</h4>
          <p>دوره‌های درحال اجرا</p>
        </div>
        <div class="p-2 w-40-px h-40-px bg-danger rounded-circle d-flex align-items-center justify-content-center">
          <i class="fas fa-chart-line text-white"></i>
        </div>
      </div>
    </div>
  </div>

  <!-- دوره‌های تکمیل‌شده -->
  <div class="col-lg-4 col-md-4 mb-3">
    <div class="card border-none shadow-none bg-light h-100">
      <div class="card-body d-flex align-items-center justify-content-between">
        <div class="card-title text-muted">
          <h4 class="mb-3 text-dark">{{ completedCourses }}</h4>
          <p>دوره‌های تکمیل شده</p>
        </div>
        <div class="p-2 w-40-px h-40-px bg-danger rounded-circle d-flex align-items-center justify-content-center">
          <i class="fa-solid fa-graduation-cap text-white"></i>
        </div>
      </div>
    </div>
  </div>
</div>


    <!-- My Courses Section -->
    <div v-if="courses.length === 0" class="card mb-4 bg-light">
      <div
        class="card-header border-bottom-0 shadow-none bg-light d-flex align-items-center justify-content-between py-3"
      >
        <h5 class="mb-0 text-dark">
          <i class="icon icon-filled-book text-dark fs-4"></i> دوره‌های اخیر
        </h5>
      </div>
      <div
        class="card-body min-vh-25 d-flex flex-column justify-content-between"
      >
        <table class="table table-striped">
          <thead class="bg-white rounded">
            <tr class="text-center">
              <th>نام دوره</th>
              <th>فرایند</th>
              <th>وضعیت</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td
                colspan="3"
                class="text-center fw-bold shadow-none bg-light border-bottom-0 py-5"
              >
              <span class="d-dlex align-items-center fs-5" v-if="authStore.user?.role === 'دانشجو'"><i class="fa-solid fa-triangle-exclamation ms-2 text-warning fs-3"></i> هنوز دوره‌ای ثبت
                نام نکرده‌اید.</span>
                <span class="d-dlex align-items-center fs-5" v-else><i class="fa-solid fa-triangle-exclamation ms-2 text-warning fs-3"></i> هنوز دوره‌ای ثبت
                 نکرده اید.</span>
              </td>
            </tr>
            <tr>
              <td
                colspan="3"
                class="text-center text-danger1 shadow-none bg-light border-bottom-0 py-5"
              >
                <nuxt-link to="/courses"  v-if="authStore.user?.role === 'دانشجو'" class="btn btn-danger py-2">مشاهده تمام دوره‌ها</nuxt-link>
                <nuxt-link  to="/account/create"v-permission="'create_course'" class="btn btn-danger py-2">ایجاد دوره</nuxt-link>
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
        <i class="icon icon-filled-book text-dark fs-4"></i> دوره‌های من
      </h5>
    </div>

    <!-- Body Section -->
    <div class="card-body min-vh-25 d-flex flex-column justify-content-between">
      <div class="d-none d-md-block">
        <table class="table ">
        <thead class="bg-white rounded">
          <tr class="text-center">
            <th>نام دوره</th>
            <th v-if="authStore.user?.role === 'دانشجو'">فرایند</th>
            <th>وضعیت</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(course, index) in courses" :key="index" class="align-middle bg-light">
            <td class="bg-light">
              <nuxt-link :to="`/courses/${course.slug}`" class="text-dark">
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
              </nuxt-link>
             
            </td>
            <td class="bg-light"  v-if="authStore.user?.role === 'دانشجو'">
              <nuxt-link :to="`/courses/${course.slug}`" class="text-dark">
                <div>
                <span class="d-block fw-bold text-muted">
                  {{ course.progress.completed }}/{{ course.progress.total }}
                  درس انجام شده
                </span>
                <div class="progress mt-1 h-6-px">
                  <div
                    class="progress-bar"
                    :class="course.status === 'در حال اجرا' ? 'bg-danger' : 'bg-success'"
                    role="progressbar"
                    :style="{ width: course.progress.percentage + '%' }"
                  ></div>
                </div>
              </div>
              </nuxt-link>
            </td>
            <td class="text-center bg-light">
              <span
              v-permission="'status_course'"
                class="badge p-2"
                :class="course.status === 'در حال اجرا' ? 'bg-warning text-dark' : 'bg-success opacity-75'"
              >
                <i
                  :class="course.status === 'در حال اجرا' ? 'fa-solid fa-repeat' : 'fa-solid fa-check'"
                  class="ms-1"
                ></i>
                {{ course.status }}
                
              </span>
              <nuxtLink
               v-permission="'update_course'"
                  :to="`/account/edit/${course.id}`"
                    class="btn btn-success btn-sm p-1"
                  >
                  <i class="icon icon-filled-pen"></i>  ویرایش دوره
                  </nuxtLink>
            </td>
          </tr>
        </tbody>
      </table>
      </div>
     

<!-- نمایش در موبایل -->
<!-- نمایش در موبایل -->
<div class="d-block d-md-none">
  <div v-for="(course, index) in courses" :key="index" class="course-card">
    <nuxt-link :to="`/courses/${course.slug}`" class="text-dark">
      <div class="course-image">
        <img :src="getMediaUrl(course.image)" alt="Course Image" class="w-100 h-100 object-fit-cover rounded">
        <div class="course-overlay">
          <h6 class="fw-bold text-white">{{ course.title }}</h6>
        </div>
      </div>
    </nuxt-link>

    <!-- اطلاعات تکمیلی دوره -->
    <div class="course-info p-3">
      <p class="text-muted small mb-1">برگزار کننده: <span class="text-danger1">{{ course.organizer }}</span></p>

      <!-- نمایش پیشرفت دوره برای دانشجو -->
      <div v-if="authStore.user?.role === 'دانشجو'" class="progress-container mt-2">
        <p class="fw-bold text-muted">
          {{ course.progress.completed }}/{{ course.progress.total }} درس انجام شده
        </p>
        <div class="progress">
          <div class="progress-bar"
               :class="course.status === 'در حال اجرا' ? 'bg-danger' : 'bg-success'"
               role="progressbar"
               :style="{ width: course.progress.percentage + '%' }">
          </div>
        </div>
      </div>

      <!-- وضعیت دوره -->
      <div class="mt-2">
        <span class="badge p-2"
          :class="course.status === 'در حال اجرا' ? 'bg-warning text-dark' : 'bg-success opacity-75'">
          <i :class="course.status === 'در حال اجرا' ? 'fa-solid fa-repeat' : 'fa-solid fa-check'"></i>
          {{ course.status }}
        </span>
      </div>

      <!-- دکمه ویرایش برای مدرس -->
      <div v-if="authStore.user?.role === 'مدرس'" class="mt-3 text-center">
        <nuxtLink v-permission="'update_course'" :to="`/account/edit/${course.id}`" class="btn btn-success btn-sm">
          <i class="icon icon-filled-pen"></i> ویرایش دوره
        </nuxtLink>
      </div>
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
    console.warn("توکن یافت نشد. لطفاً وارد حساب کاربری خود شوید.");
    return;
  }

  try {
    const response = await $api.post("/course/user/list", {}, {
      headers: {
        Authorization: "Bearer " + token,
      },
    });

    if (response.data.status && response.data.data.results) {
      const userRole = response.data.role; // نقش کاربر (student یا teacher)

      if (userRole === "student") {
        courses.value = response.data.data.results.map(item => ({
          id: item.course.id,
          title: item.course.title,
          organizer: item.course.organizer?.name || "نامشخص",
          image: item.course.image || "/default-course.jpg",
          slug: item.course.slug,
          progress: {
            completed: 0,
            total: 100,
            percentage: 0,
          },
          status: item.status === "not_started" ? "شروع نشده" : "در حال اجرا",
        }));

        purchasedCourses.value = courses.value.length;
        inProgressCourses.value = courses.value.filter(course => course.status === "در حال اجرا").length;
        completedCourses.value = courses.value.filter(course => course.status === "تکمیل شده").length;

      } else if (userRole === "teacher") {
        courses.value = response.data.data.results.map(item => ({
          id: item.id,
          title: item.title,
          organizer: item.organizer?.name || "نامشخص",
          image: item.image || "/default-course.jpg",
          slug: item.slug,
          price: item.price,
          category: item.category?.title || "نامشخص",
          attributes: item.attributes || [],
          status: item.status || "در حال اجرا",
        }));

        purchasedCourses.value = courses.value.length; // تعداد دوره‌های ایجادشده
        inProgressCourses.value = courses.value.filter(course => course.status === "در حال اجرا").length;
        completedCourses.value = courses.value.filter(course => course.status === "تکمیل شده").length;
      }

      console.log("📌 دوره‌های پردازش‌شده:", courses.value);
    } else {
      console.warn("هیچ داده‌ای دریافت نشد.");
      courses.value = [];
    }
  } catch (error) {
    console.error("🚨 خطا در دریافت اطلاعات دوره‌ها:", error.response?.data?.detail || error.message);
  }
};

onMounted(fetchCourses);


onMounted(fetchCourses);


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
