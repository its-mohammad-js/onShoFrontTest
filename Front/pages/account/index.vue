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
          <p v-if="authStore.user?.role === 'مدرس' || authStore.user?.role === 'مدیر-کل'">دوره‌های ایجاد شده</p>
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
          <i class="icon icon-filled-book text-dark fs-4"></i>  دوره‌های اخیر
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
              <span class="d-dlex align-items-center fs-5"><i class="fa-solid fa-triangle-exclamation ms-2 text-warning fs-3"></i> هنوز دوره‌ای ثبت
                نام نکرده‌اید.</span>
              </td>
            </tr>
            <tr>
              <td
                colspan="3"
                class="text-center text-danger1 shadow-none bg-light border-bottom-0 py-5"
              >
              <nuxt-link to="/courses"  v-if="authStore.user?.role === 'دانشجو'" class="btn btn-danger py-2">مشاهده تمام دوره‌ها</nuxt-link>
              <nuxt-link 
                v-if="canCreateCourse"
                to="/account/create"
                v-permission="'course_create'" 
                class="btn btn-danger py-2"
              >
                ایجاد دوره
              </nuxt-link>
              <button 
                v-else-if="organizationStatusMessage"
                class="btn btn-secondary py-2" 
                :title="organizationStatusMessage"
                disabled
              >
                <i class="icon icon-filled-exclamation-triangle me-2"></i>
                ایجاد دوره (غیرفعال)
              </button>
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
              v-permission="'course_view'"
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
               v-permission="'course_edit'"
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

      <!-- دکمه ویرایش برای مدرس و مدیر -->
      <div v-if="authStore.user?.role === 'مدرس' || authStore.user?.role === 'مدیر-کل'" class="mt-3 text-center">
        <nuxtLink v-permission="'course_edit'" :to="`/account/edit/${course.id}`" class="btn btn-success btn-sm">
          <i class="icon icon-filled-pen"></i> ویرایش دوره
        </nuxtLink>
      </div>
    </div>
  </div>
</div>


    </div>
  </div>

  <!-- Subdomain Settings Card (For Organization and School) -->
  <div class="card mb-4 bg-light" v-if="currentOrganization">
    <div class="card-header border-bottom-0 shadow-none bg-light d-flex align-items-center justify-content-between py-3">
      <h5 class="mb-0 text-dark">
        <i class="icon icon-regular-globe text-dark fs-4 me-2"></i>
        تنظیمات زیردامنه
      </h5>
    </div>
    <div class="card-body">
      <div class="row align-items-center">
        <div class="col-md-8">
          <label class="form-label fw-bold text-dark mb-2">
            زیردامنه {{ currentOrganization.user_type === 'school' ? 'آموزشگاه' : 'سازمان' }}
          </label>
          <div v-if="!isEditingDomain" class="d-flex align-items-center">
            <span class="text-dark fs-6">
              <i class="icon icon-regular-globe me-2"></i>
              {{ currentOrganization.subdomain || 'زیردامنه تنظیم نشده است' }}
            </span>
            <button 
              @click="startEditingDomain" 
              class="btn btn-sm btn-outline-primary ms-3"
            >
              <i class="icon icon-filled-pen me-1"></i>
              ویرایش
            </button>
          </div>
          <div v-else class="d-flex align-items-center gap-2">
            <div class="flex-grow-1">
              <div class="input-group">
                <input
                  v-model="domainInput"
                  type="text"
                  class="form-control"
                  placeholder="subdomain"
                  :class="{ 'is-invalid': domainError }"
                />
                <span class="input-group-text bg-light">
                  <i class="icon icon-regular-globe"></i>
                </span>
              </div>
              <div v-if="domainError" class="invalid-feedback d-block">
                {{ domainError }}
              </div>
              <small class="text-muted d-block mt-1">
                زیردامنه اختصاصی سازمان خود را وارد کنید
              </small>
            </div>
            <button 
              @click="saveDomain" 
              class="btn btn-sm btn-success"
              :disabled="savingDomain"
            >
              <span v-if="savingDomain" class="spinner-border spinner-border-sm me-1"></span>
              <i v-else class="icon icon-filled-check me-1"></i>
              ذخیره
            </button>
            <button 
              @click="cancelEditingDomain" 
              class="btn btn-sm btn-secondary"
              :disabled="savingDomain"
            >
              انصراف
            </button>
          </div>
        </div>
        <div class="col-md-4 text-end">
          <nuxt-link 
            to="/account/organization"
            class="btn btn-outline-primary btn-sm"
          >
            <i class="icon icon-filled-settings me-1"></i>
            تنظیمات کامل
          </nuxt-link>
        </div>
      </div>
    </div>
  </div>

  <div class="card mb-4 bg-light" v-if="authStore.user?.role === 'دانشجو'">
    <!-- Header Section -->
    <div
      class="card-header border-bottom-0 shadow-none bg-light d-flex align-items-center justify-content-between py-3"
    >
    <h5 class="mb-0 text-dark">
          <i class="icon icon-filled-clipboard-text text-dark fs-4"></i> تمرین‌های من
        </h5>
    </div>

    <!-- Body Section -->
    <div class="card-body">
      <!-- حالت بدون تمرین -->
      <div v-if="tasks.length === 0" class="text-center py-5">
        <i class="fa-solid fa-triangle-exclamation text-warning fs-3"></i>
        <p class="text-dark fs-5 mt-3 fw-bold" v-if="authStore.user?.role === 'دانشجو'">هنوز تمرینی برای شما ثبت نشده است.</p>
        <p class="text-dark fs-5 mt-3 fw-bold" v-else>هنوز تمرینی ثبت نکرده اید.</p>
      </div>

      <!-- حالت با تمرین -->
      <div v-else class="row gy-4">
          <div class="col-lg-6">
            <div class="list-group">
              <div class="list-group-item bg-light p-3 my-2 border-0 border-bottom border-5 border-warning">
                <div class="d-flex align-items-center justify-content-between">
                  <span>لیست تمرین ها</span>
                  <span>({{ tasks.length }})</span>
                </div>
              </div>

              <div
                v-for="(task, index) in tasks"
                :key="index"
                class="list-group-item bg-white border-0 p-3 my-2 rounded shadow-sm cursor-pointer"
                @click="openTaskDetails(task)"
              >
                <span
                  class="badge p-2 mb-2 rounded-pill"
                  :class="task.level === 'پیشرفته' ? 'bg-success-subtle opacity-75 text-white' : 'bg-info-subtle  text-dark'"
                >
                  {{ task.level }}
                </span>
                <h6 class="mt-2 fw-bold">{{ task.title }}</h6>
                <hr>
                <div class="d-flex align-items-center justify-content-between">
                  <small class="text-muted"> مهلت انجام : </small>
                  <small class="text-muted d-flex align-items-center justify-content-center gap-1">
                    <i class="icon icon-regular-calendar text-danger1"></i>
                    {{ task.deadline || "نامشخص" }}
                  </small>
                </div>
              </div>
            </div>
          </div>
          <div class="col-lg-6">
            <div class="list-group">
              <div class="list-group-item bg-light p-3 my-2 border-0 border-bottom border-5 border-success">
                <div class="d-flex align-items-center justify-content-between">
                  <span>تمرین‌های انجام شده</span>
                  <span>({{ completedTasks.length }})</span>
                </div>
              </div>

              <div
                v-for="(task, index) in completedTasks"
                :key="index"
                class="list-group-item bg-white border-0 p-3 my-2 rounded shadow-sm"
              >
                <span class="badge p-2 mb-2 bg-success opacity-75 text-white"> تکمیل شده </span>
                <h6 class="mt-2 fw-bold">{{ task.title }}</h6>
                <hr />
                <div class="d-flex align-items-center justify-content-between">
                  <small class="text-muted"> تاریخ تکمیل: </small>
                  <small class="text-muted d-flex align-items-center justify-content-center gap-1">
                    <i class="icon icon-regular-calendar-check text-success"></i>
                    {{ task.completedDate || "نامشخص" }}
                  </small>
                </div>
              </div>

              <div class="list-group-item bg-light p-3 my-2 border-0 text-center">
                <button class="btn btn-outline-success w-100">
                  آپلود فایل تمرین <i class="icon icon-regular-cloud-upload"></i>
                </button>
              </div>
            </div>
          </div>
        </div>
        <teleport to="body">
        <!-- پس‌زمینه‌ی خاکستری برای Offcanvas -->
        <div v-if="showOffcanvas" class="offcanvas-overlay" @click="closeTaskDetails"></div>

        <!-- Offcanvas -->
        <transition name="slide">
          <div v-if="showOffcanvas" class="offcanvas-content" @click.stop>
            <div class="offcanvas-header d-flex align-items-center justify-content-between pb-3 border-bottom border-3">
              <h5 class="offcanvas-title">{{ selectedTask?.title || "بدون عنوان" }}</h5>
              <button type="button" class="btn-close" @click="closeTaskDetails"></button>
            </div>
            <div class="offcanvas-body">
              <div class="list-group-item p-3 my-2 border-0 border-bottom border-5 border-warning">
                <div class="d-flex align-items-center justify-content-between">
                  <span>لیست تمرین ها</span>
                </div>
              </div>
              <h5 class="my-4 text-dark">{{ selectedTask?.title || "بدون عنوان" }}</h5>
              <p class="my-4"><span class="text-muted">درجه سختی: </span>{{ selectedTask?.level || "نامشخص" }}</p>
              <p class="my-4"><span class="text-muted">مهلت انجام: </span>{{ selectedTask?.deadline || "نامشخص" }}</p>
              <p class="my-4"><span class="text-muted">توضیحات: </span><br><br>
               <span class="p-3 border rounded-3 d-block border-2"> {{ selectedTask?.description || "بدون توضیحات" }}</span>
              </p>

              <!-- فایل‌های تمرین -->
              <div>
                <h6>فایل‌ تمرین:</h6>
                <ul class="list-group">
                  <li v-if="selectedTask.file" class="list-group-item d-flex align-items-center p-3 rounded-3 border-2">
  <i class="fa-solid fa-file-pdf text-danger ms-2"></i>
  <a :href="selectedTask.file" target="_blank" class="text-danger text-decoration-none">
    دانلود و نمایش
  </a>
</li>

                </ul>
              </div>

              <!-- آپلود فایل تمرین -->
              <div class="upload-section mt-4">
  <h6>آپلود فایل تمرین:</h6>
  
  <!-- مخفی کردن input -->
  <input type="file" id="fileInput" class="d-none" @change="handleFileUpload">

  <!-- دکمه انتخاب فایل -->
  <button class="btn btn-outline-danger upload-btn w-100" @click="triggerFileInput">
    <i class="fa-solid fa-cloud-upload-alt"></i> {{ selectedFileName || "انتخاب فایل تمرین" }}
  </button>
</div>

            </div>
          </div>
        </transition>
      </teleport>
    </div>
  </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useAuthStore } from "~/stores/auth";

const authStore = useAuthStore();
const { canCreateCourse, organizationStatusMessage, fetchOrganization, organization } = useOrganization()

const { $api, $sweetalert } = useNuxtApp();
const { getMediaUrl } = useMediaUrl();
const courses = ref([]);
const purchasedCourses = ref(0);
const inProgressCourses = ref(0);
const completedCourses = ref(0);

// Domain editing
const isEditingDomain = ref(false);
const domainInput = ref('');
const domainError = ref('');
const savingDomain = ref(false);

// Computed for organization (to unwrap readonly ref)
const currentOrganization = computed(() => organization.value);


import { useNuxtApp } from "#app";
const completedTasks = ref([]);


const loading = ref(true);
const tasks = ref([]);
const selectedTask = ref(null);
const showOffcanvas = ref(false);

// دریافت تمرین‌ها از API
const fetchTasks = async () => {
  const token = useCookie("token").value;
  if (!token) {
    return;
  }

  try {
    const response = await $api.post(
      "/course/user/task/list",
      {},
      {
        headers: {
          Authorization: "Bearer " + token,
        },
      }
    );

    if (response.data.status && Array.isArray(response.data.data)) {
      tasks.value = response.data.data.map(task => ({
        title: task.title,
        level: difficultyMap[task.difficulty] || "نامشخص",
        deadline: task.deadline || "نامشخص",
        description: task.description || "بدون توضیحات",
        file: task.file || [],
      }));
    }
  } catch (error) {
    console.error("خطا در دریافت داده‌ها:", error.message);
  } finally {
    loading.value = false;
  }
};

const difficultyMap = {
  beginner: "مبتدی",
  intermediate: "متوسط",
  advanced: "پیشرفته",
};

// باز کردن offcanvas
const openTaskDetails = (task) => {
  if (!task) return;
  selectedTask.value = task;
  showOffcanvas.value = true;
  document.body.style.overflow = "hidden";
};

// بستن offcanvas
const closeTaskDetails = () => {
  setTimeout(() => {
    showOffcanvas.value = false;
    selectedTask.value = null;
    document.body.style.overflow = "auto";
  }, 50); // تأخیر برای جلوگیری از بسته شدن ناگهانی
};

const selectedFileName = ref("");

const triggerFileInput = () => {
  document.getElementById("fileInput").click();
};

const handleFileUpload = (event) => {
  const file = event.target.files[0];
  if (file) {
    selectedFileName.value = file.name;
  } else {
    selectedFileName.value = "انتخاب فایل تمرین";
  }
};


definePageMeta({
  layout: "account",
  middleware: ["auth"],
});

onMounted(fetchTasks);
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

    console.log("📡 API Response for courses:", response.data);

    if (response.data.status) {
      // Handle different response structures
      const data = response.data.data || {}
      const results = data.results || data.data || data || []
      const userRole = response.data.role || (authStore.user?.role === 'مدرس' ? 'teacher' : 'student')

      if (userRole === "student" || authStore.user?.role === 'دانشجو') {
        courses.value = results.map(item => {
          // Handle both structures: item.course (enrollment) or item (direct course)
          const course = item.course || item
          return {
            id: course.id,
            title: course.title,
            organizer: course.organizer?.name || "نامشخص",
            image: course.image || "/default-course.jpg",
            slug: course.slug,
            progress: {
              completed: item.progress?.completed || 0,
              total: item.progress?.total || 100,
              percentage: item.progress?.percentage || 0,
            },
            status: item.status === "not_started" ? "شروع نشده" : 
                   item.status === "in_progress" ? "در حال اجرا" :
                   item.status === "completed" ? "تکمیل شده" :
                   item.status || "شروع نشده",
          }
        });

        purchasedCourses.value = courses.value.length;
        inProgressCourses.value = courses.value.filter(course => course.status === "در حال اجرا").length;
        completedCourses.value = courses.value.filter(course => course.status === "تکمیل شده").length;

      } else if (userRole === "teacher" || authStore.user?.role === 'مدرس') {
        courses.value = results.map(item => ({
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

        purchasedCourses.value = courses.value.length;
        inProgressCourses.value = courses.value.filter(course => course.status === "در حال اجرا").length;
        completedCourses.value = courses.value.filter(course => course.status === "تکمیل شده").length;
      }

      console.log("📌 دوره‌های پردازش‌شده:", courses.value);
      console.log("📊 آمار: خریداری شده:", purchasedCourses.value, "در حال اجرا:", inProgressCourses.value, "تکمیل شده:", completedCourses.value);
    } else {
      console.warn("هیچ داده‌ای دریافت نشد.");
      courses.value = [];
    }
  } catch (error) {
    console.error("🚨 خطا در دریافت اطلاعات دوره‌ها:", error.response?.data || error.message);
    courses.value = [];
  }
};

// Domain editing functions
const startEditingDomain = () => {
  domainInput.value = organization.value?.subdomain || '';
  domainError.value = '';
  isEditingDomain.value = true;
};

const cancelEditingDomain = () => {
  isEditingDomain.value = false;
  domainInput.value = '';
  domainError.value = '';
};

const validateDomain = (subdomain) => {
  if (!subdomain || subdomain.trim() === '') {
    return '';
  }
  
  // Validate subdomain format (alphanumeric and hyphens only, no spaces)
  const subdomainRegex = /^[a-z0-9]([a-z0-9-]*[a-z0-9])?$/i;
  if (!subdomainRegex.test(subdomain)) {
    return 'فرمت زیردامنه صحیح نیست. فقط حروف، اعداد و خط تیره مجاز است';
  }
  
  return '';
};

const saveDomain = async () => {
  domainError.value = '';
  
  const error = validateDomain(domainInput.value);
  if (error) {
    domainError.value = error;
    return;
  }
  
  savingDomain.value = true;
  const token = useCookie("token").value;
  
  try {
    const formData = new FormData();
    formData.append('subdomain', domainInput.value.trim() || '');
    
    // If organization already exists, update it
    if (organization.value) {
      formData.append('name', organization.value.name || '');
      formData.append('description', organization.value.description || '');
      if (organization.value.website_url) {
        formData.append('website_url', organization.value.website_url);
      }
    }
    
    const response = await $api.post('/course/organization/edit', formData, {
      headers: {
        Authorization: "Bearer " + token,
        'Content-Type': 'multipart/form-data',
      },
    });
    
    if (response.data.status) {
      // Refresh organization data
      await fetchOrganization();
      
      $sweetalert.fire({
        title: 'موفقیت',
        text: 'زیردامنه با موفقیت به‌روزرسانی شد',
        icon: 'success',
        confirmButtonText: 'متوجه شدم'
      });
      
      isEditingDomain.value = false;
    }
  } catch (error) {
    console.error('خطا در به‌روزرسانی زیردامنه:', error);
    $sweetalert.fire({
      title: 'خطا',
      text: error.response?.data?.message || 'خطا در به‌روزرسانی دامنه',
      icon: 'error',
      confirmButtonText: 'متوجه شدم'
    });
  } finally {
    savingDomain.value = false;
  }
};

onMounted(async () => {
  fetchCourses();
  await fetchOrganization();
  // Debug: Check if organization is loaded
  console.log('Organization loaded:', currentOrganization.value);
  
  // Check school verification status
  if (authStore.user && (authStore.user.user_type === 'school' || authStore.user.role === 'school')) {
    if (currentOrganization.value && !currentOrganization.value.is_verified) {
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
  }
});

// definePageMeta({
//   layout: "account",
//   middleware: ["auth"],
// });
</script>




<style scoped>
.card {
  transform: scale(1) !important;
}
.card-title i {
  font-size: 1.5rem;
}
/* Overlay */
.offcanvas-overlay {
  position: fixed;
  top: 0;
  right: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.5);
  z-index: 1050;
}

/* Offcanvas */
.offcanvas-content {
  position: fixed;
  top: 0;
  left: 0;
  width: 40%;
  height: 100%;
  background: white;
  box-shadow: -5px 0 15px rgba(0, 0, 0, 0.2);
  padding: 20px;
  z-index: 1060;
}
.slide-enter-active,
.slide-leave-active {
  transition: transform 0.3s ease-in-out, opacity 0.2s ease-in-out;
}

.slide-enter-from,
.slide-leave-to {
  transform: translateX(-100%);
  opacity: 0;
}

.slide-enter-to {
  transform: translateX(0);
  opacity: 1;
}


.upload-btn {
  border-radius: 12px;
  font-weight: bold;
  padding: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-size: 1rem;
}

.upload-btn i {
  font-size: 1.2rem;
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
}
</style>
