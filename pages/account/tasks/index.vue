<template>
  <div class="container py-5">
    <div class="card mb-4 bg-light">
      <div class="card-header border-bottom-0 shadow-none bg-light d-flex align-items-center justify-content-between py-3">
        <h5 class="mb-0 text-dark">
          <i class="icon icon-filled-clipboard-text text-dark fs-4"></i> 
          {{ authStore.user?.role === 'دانشجو' ? 'تمرین‌های من' : 'مدیریت تمرین‌ها' }}
        </h5>
      </div>

      <div class="card-body">
        <div v-if="loading" class="text-center py-5">
          <i class="fa-solid fa-spinner fa-spin text-primary fs-3"></i>
          <p class="text-muted fs-5 mt-3">در حال دریافت تمرین‌ها...</p>
        </div>

        <div v-else-if="tasks.length === 0" class="text-center py-5">
          <i class="fa-solid fa-triangle-exclamation text-warning fs-3"></i>
          <p class="text-dark fs-5 mt-3 fw-bold" v-if="authStore.user?.role === 'دانشجو'">هنوز تمرینی برای شما ثبت نشده است.</p>
          <p class="text-dark fs-5 mt-3 fw-bold" v-else>هنوز تمرینی ثبت نکرده اید.</p>
        </div>

        <!-- Student View -->
        <div v-else-if="authStore.user?.role === 'دانشجو'" class="row gy-4">
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
                <div class="d-flex justify-content-between align-items-start mb-2">
                  <span
                    class="badge p-2 rounded-pill"
                    :class="getDifficultyClass(task.difficulty)"
                  >
                    {{ task.difficulty }}
                  </span>
                  <span
                    v-if="task.submission"
                    class="badge p-2 rounded-pill"
                    :class="getSubmissionStatusClass(task.submission.status)"
                  >
                    {{ task.submission.status || 'ارسال شده' }}
                  </span>
                  <span
                    v-else
                    class="badge p-2 rounded-pill bg-warning text-dark"
                  >
                    در انتظار ارسال
                  </span>
                </div>
                
                <h6 class="mt-2 fw-bold">{{ task.title }}</h6>
                <p class="text-muted small mb-2">{{ task.description ? task.description.substring(0, 100) + '...' : 'بدون توضیحات' }}</p>
                
                <div class="d-flex justify-content-between align-items-center">
                  <small class="text-muted">
                    <i class="icon icon-regular-book text-primary"></i>
                    {{ task.course.title }}
                  </small>
                  <small class="text-muted">
                    <i class="icon icon-regular-calendar text-danger1"></i>
                    {{ formatDate(task.create_date) }}
                  </small>
                </div>
                
                <div v-if="task.lesson" class="mt-2">
                  <small class="text-muted">
                    <i class="icon icon-regular-play text-success"></i>
                    درس: {{ task.lesson.title }}
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
                <span 
                  class="badge p-2 mb-2 text-white"
                  :class="getSubmissionStatusClass(task.submission?.status)"
                >
                  {{ task.submission?.status || 'در انتظار بررسی' }}
                </span>
                <h6 class="mt-2 fw-bold">{{ task.title }}</h6>
                <hr />
                <div class="d-flex align-items-center justify-content-between">
                  <small class="text-muted"> تاریخ ارسال: </small>
                  <small class="text-muted d-flex align-items-center justify-content-center gap-1">
                    <i class="icon icon-regular-calendar-check text-success"></i>
                    {{ formatDate(task.submission?.submitted_at) || "نامشخص" }}
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

        <!-- Teacher View -->
        <div v-else class="row gy-4">
          <!-- Tasks Section -->
          <div class="col-lg-6">
            <div class="list-group">
              <div class="list-group-item bg-light p-3 my-2 border-0 border-bottom border-5 border-info">
                <div class="d-flex align-items-center justify-content-between">
                  <span>تمرین‌های ایجاد شده</span>
                  <span>({{ tasks.length }})</span>
                </div>
                <!-- Debug info -->
                <small class="text-muted">Debug: {{ tasks.length }} tasks loaded</small>
              </div>

              <div
                v-for="(task, index) in tasks"
                :key="index"
                class="list-group-item bg-white border-0 p-3 my-2 rounded shadow-sm"
              >
                <div class="d-flex justify-content-between align-items-start mb-2">
                  <span
                    class="badge p-2 rounded-pill"
                    :class="getDifficultyClass(task.difficulty)"
                  >
                    {{ task.difficulty }}
                  </span>
                  <div class="d-flex gap-2">
                    <span class="badge bg-primary text-white">
                      {{ task.submission_count }} ارسال
                    </span>
                    <span v-if="task.pending_count > 0" class="badge bg-warning text-dark">
                      {{ task.pending_count }} در انتظار
                    </span>
                  </div>
                </div>
                
                <h6 class="mt-2 fw-bold">{{ task.title }}</h6>
                <p class="text-muted small mb-2">{{ task.description ? task.description.substring(0, 100) + '...' : 'بدون توضیحات' }}</p>
                
                <div class="d-flex justify-content-between align-items-center">
                  <small class="text-muted">
                    <i class="icon icon-regular-book text-primary"></i>
                    {{ task.course.title }}
                  </small>
                  <small class="text-muted">
                    <i class="icon icon-regular-calendar text-danger1"></i>
                    {{ formatDate(task.create_date) }}
                  </small>
                </div>
                
                <div v-if="task.lesson" class="mt-2">
                  <small class="text-muted">
                    <i class="icon icon-regular-play text-success"></i>
                    درس: {{ task.lesson.title }}
                  </small>
                </div>

                <!-- Task Actions -->
                <div class="mt-3">
                  <div class="d-flex gap-2">
                    <button 
                      class="btn btn-outline-primary btn-sm"
                      @click="viewTaskDetails(task)"
                    >
                      <i class="icon icon-regular-eye"></i> مشاهده
                    </button>
                    <button 
                      class="btn btn-outline-warning btn-sm"
                      @click="editTask(task)"
                    >
                      <i class="icon icon-regular-edit"></i> ویرایش
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Submissions Section -->
          <div class="col-lg-6">
            <div class="list-group">
              <div class="list-group-item bg-light p-3 my-2 border-0 border-bottom border-5 border-primary">
                <div class="d-flex align-items-center justify-content-between">
                  <span>ارسالات دانشجویان</span>
                  <span>({{ submissions.length }})</span>
                </div>
              </div>

              <div
                v-for="(submission, index) in submissions"
                :key="index"
                class="list-group-item bg-white border-0 p-3 my-2 rounded shadow-sm"
              >
                <div class="d-flex justify-content-between align-items-start mb-3">
                  <div>
                    <h6 class="fw-bold mb-1">{{ submission.task?.title || 'بدون عنوان' }}</h6>
                    <p class="text-muted small mb-2">{{ submission.task.description ? submission.task.description.substring(0, 100) + '...' : 'بدون توضیحات' }}</p>
                  </div>
                  <span
                    class="badge p-2 rounded-pill"
                    :class="getSubmissionStatusClass(submission.submission.status)"
                  >
                    {{ submission.submission.status || 'در انتظار بررسی' }}
                  </span>
                </div>

                <div class="row">
                  <div class="col-md-6">
                    <div class="d-flex align-items-center mb-2">
                      <i class="icon icon-regular-user text-primary me-2"></i>
                      <span class="text-muted small">دانشجو:</span>
                      <span class="fw-bold ms-2">{{ submission.student.first_name }} {{ submission.student.last_name }}</span>
                    </div>
                    <div class="d-flex align-items-center mb-2">
                      <i class="icon icon-regular-book text-success me-2"></i>
                      <span class="text-muted small">دوره:</span>
                      <span class="ms-2">{{ submission.course.title }}</span>
                    </div>
                  </div>
                  <div class="col-md-6">
                    <div class="d-flex align-items-center mb-2">
                      <i class="icon icon-regular-calendar text-warning me-2"></i>
                      <span class="text-muted small">تاریخ ارسال:</span>
                      <span class="ms-2">{{ formatDate(submission.submission.submitted_at) }}</span>
                    </div>
                    <div v-if="submission.task?.lesson" class="d-flex align-items-center mb-2">
                      <i class="icon icon-regular-play text-info me-2"></i>
                      <span class="text-muted small">درس:</span>
                      <span class="ms-2">{{ submission.task.lesson?.title || 'بدون درس' }}</span>
                    </div>
                  </div>
                </div>

                <div class="mt-3">
                  <div class="d-flex gap-2">
                    <button 
                      class="btn btn-outline-primary btn-sm"
                      @click="viewSubmissionDetails(submission)"
                    >
                      <i class="icon icon-regular-eye"></i> مشاهده جزئیات
                    </button>
                    <button 
                      class="btn btn-outline-success btn-sm"
                      @click="updateSubmissionStatus(submission, 'approved')"
                      v-if="submission.submission.status !== 'تأیید شده'"
                    >
                      <i class="icon icon-regular-check"></i> تأیید
                    </button>
                    <button 
                      class="btn btn-outline-danger btn-sm"
                      @click="updateSubmissionStatus(submission, 'rejected')"
                      v-if="submission.submission.status !== 'رد شده'"
                    >
                      <i class="icon icon-regular-times"></i> رد
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- استفاده از teleport برای نمایش خارج از layout -->
      <teleport to="body">
  <!-- پس‌زمینه‌ی خاکستری برای Offcanvas -->
  <div v-if="showOffcanvas" class="offcanvas-overlay" @click="closeTaskDetails"></div>

  <!-- Offcanvas -->
  <transition name="slide">
    <div v-if="showOffcanvas" class="offcanvas-content" @click.stop>
      <div class="offcanvas-header d-flex align-items-center justify-content-between pb-3 border-bottom border-3">
        <h5 class="offcanvas-title">
          {{ authStore.user?.role === 'دانشجو' 
            ? (selectedTask?.title || "بدون عنوان") 
            : (selectedTask?.task?.title || "جزئیات ارسال") 
          }}
        </h5>
        <button type="button" class="btn-close" @click="closeTaskDetails"></button>
      </div>
      <div class="offcanvas-body">
        <!-- Student View -->
        <div v-if="authStore.user?.role === 'دانشجو'">
          <div class="list-group-item p-3 my-2 border-0 border-bottom border-5 border-warning">
            <div class="d-flex align-items-center justify-content-between">
              <span>لیست تمرین ها</span>
            </div>
          </div>
          <h5 class="my-4 text-dark">{{ selectedTask?.title || "بدون عنوان" }}</h5>
          <p class="my-4"><span class="text-muted">درجه سختی: </span>{{ selectedTask?.difficulty || "نامشخص" }}</p>
          <p class="my-4"><span class="text-muted">مهلت انجام: </span>{{ selectedTask?.deadline || "نامشخص" }}</p>
          <p class="my-4"><span class="text-muted">توضیحات: </span><br><br>
            <span class="p-3 border rounded-3 d-block border-2"> {{ selectedTask?.description || "بدون توضیحات" }}</span>
          </p>

          <!-- فایل‌های تمرین -->
          <div>
            <h6>فایل‌ تمرین:</h6>
            <ul class="list-group">
              <li v-if="selectedTask?.file" class="list-group-item d-flex align-items-center p-3 rounded-3 border-2">
                <i class="fa-solid fa-file-pdf text-danger ms-2"></i>
                <a :href="selectedTask.file" target="_blank" class="text-danger text-decoration-none">
                  دانلود و نمایش
                </a>
              </li>
            </ul>
          </div>

          <div class="list-group-item p-3 my-2 border-0 border-bottom border-5 border-success-subtle"></div>

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

          <!-- فیلد توضیحات برای آپلود تمرین -->
          <div class="mt-3">
            <h6>توضیحات تمرین:</h6>
            <textarea 
              v-model="uploadDescription" 
              class="form-control" 
              rows="3" 
              placeholder="توضیحات مربوط به تمرین را وارد کنید..."
            ></textarea>
          </div>

          <!-- دکمه ارسال تمرین -->
          <div class="mt-4">
            <button class="btn btn-success w-100" @click="handleSubmitExercise">
              <i class="fa-solid fa-paper-plane"></i> ارسال تمرین
            </button>
          </div>
        </div>

         <!-- Teacher View -->
         <div v-else>
           <div class="list-group-item p-3 my-2 border-0 border-bottom border-5 border-primary">
             <div class="d-flex align-items-center justify-content-between">
               <span>جزئیات ارسال</span>
             </div>
           </div>
           
           <h5 class="my-4 text-dark">{{ selectedTask?.task?.title || "بدون عنوان" }}</h5>
           
           <div class="row mb-3">
             <div class="col-md-6">
               <p><span class="text-muted">دانشجو:</span> 
                 <strong>{{ selectedTask?.student?.first_name || '' }} {{ selectedTask?.student?.last_name || '' }}</strong>
               </p>
               <p><span class="text-muted">دوره:</span> 
                 <strong>{{ selectedTask?.course?.title || 'نامشخص' }}</strong>
               </p>
             </div>
             <div class="col-md-6">
               <p><span class="text-muted">تاریخ ارسال:</span> 
                 <strong>{{ formatDate(selectedTask?.submission?.submitted_at) }}</strong>
               </p>
               <p><span class="text-muted">وضعیت:</span> 
                 <span class="badge" :class="getSubmissionStatusClass(selectedTask?.submission?.status)">
                   {{ selectedTask?.submission?.status || 'در انتظار بررسی' }}
                 </span>
               </p>
             </div>
           </div>

           <div class="mb-3">
             <h6>توضیحات دانشجو:</h6>
             <div class="p-3 border rounded-3 bg-light">
               {{ selectedTask?.submission?.description || "بدون توضیحات" }}
             </div>
           </div>

           <div v-if="selectedTask?.submission?.file" class="mb-3">
             <h6>فایل ارسالی:</h6>
             <div class="list-group-item d-flex align-items-center p-3 rounded-3 border-2">
               <i class="fa-solid fa-file-pdf text-danger ms-2"></i>
               <a :href="selectedTask.submission.file" target="_blank" class="text-danger text-decoration-none">
                 <i class="fa-solid fa-download me-2"></i>
                 دانلود فایل ارسالی
               </a>
             </div>
           </div>

           <div v-else class="mb-3">
             <h6>فایل ارسالی:</h6>
             <div class="p-3 border rounded-3 bg-light text-muted">
               <i class="fa-solid fa-file-slash me-2"></i>
               هیچ فایلی ارسال نشده است
             </div>
           </div>

           <div class="mt-4">
             <div class="d-flex gap-2">
               <button 
                 class="btn btn-outline-success"
                 @click="updateSubmissionStatus(selectedTask, 'approved')"
                 v-if="selectedTask?.submission?.status !== 'تأیید شده'"
               >
                 <i class="icon icon-regular-check"></i> تأیید
               </button>
               <button 
                 class="btn btn-outline-danger"
                 @click="updateSubmissionStatus(selectedTask, 'rejected')"
                 v-if="selectedTask?.submission?.status !== 'رد شده'"
               >
                 <i class="icon icon-regular-times"></i> رد
               </button>
             </div>
           </div>
         </div>
      </div>
    </div>
  </transition>
</teleport>

      <!-- Edit Task Modal -->
      <teleport to="body">
        <div v-if="showEditModal" class="offcanvas-overlay" @click="closeEditModal"></div>
        <transition name="slide">
          <div v-if="showEditModal" class="offcanvas-content" @click.stop>
            <div class="offcanvas-header d-flex align-items-center justify-content-between pb-3 border-bottom border-3">
              <h5 class="offcanvas-title">ویرایش تمرین</h5>
              <button type="button" class="btn-close" @click="closeEditModal"></button>
            </div>
            <div class="offcanvas-body">
              <form @submit.prevent="saveTaskEdit">
                <div class="mb-3">
                  <label class="form-label">عنوان تمرین</label>
                  <input 
                    v-model="editForm.title" 
                    type="text" 
                    class="form-control" 
                    required
                  />
                </div>

                <div class="mb-3">
                  <label class="form-label">توضیحات</label>
                  <textarea 
                    v-model="editForm.description" 
                    class="form-control" 
                    rows="4"
                    required
                  ></textarea>
                </div>

                <div class="mb-3">
                  <label class="form-label">درجه سختی</label>
                  <select v-model="editForm.difficulty" class="form-select" required>
                    <option value="beginner">مبتدی</option>
                    <option value="intermediate">متوسط</option>
                    <option value="advanced">پیشرفته</option>
                  </select>
                </div>

                <div class="mb-3">
                  <label class="form-label">محدودیت زمانی (دقیقه)</label>
                  <input 
                    v-model="editForm.time_limit" 
                    type="number" 
                    class="form-control" 
                    min="1"
                  />
                </div>

                <div class="mb-3">
                  <label class="form-label">فایل تمرین (اختیاری)</label>
                  <input 
                    type="file" 
                    class="form-control" 
                    @change="handleEditFileUpload"
                    accept=".pdf,.doc,.docx,.txt"
                  />
                  <small class="text-muted">فایل فعلی: {{ currentTask?.file ? 'موجود' : 'ندارد' }}</small>
                </div>

                <div class="mt-4">
                  <div class="d-flex gap-2">
                    <button type="submit" class="btn btn-success">
                      <i class="icon icon-regular-save"></i> ذخیره تغییرات
                    </button>
                    <button type="button" class="btn btn-outline-secondary" @click="closeEditModal">
                      <i class="icon icon-regular-times"></i> انصراف
                    </button>
                  </div>
                </div>
              </form>
            </div>
          </div>
        </transition>
      </teleport>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useNuxtApp } from "#app";
import { useAuthStore } from "~/stores/auth";
const completedTasks = ref([]);
const authStore = useAuthStore();
const { $api,$sweetalert } = useNuxtApp();

const loading = ref(true);
const tasks = ref([]);
const submissions = ref([]);
const selectedTask = ref(null);
const showOffcanvas = ref(false);
const answerStatuses = ref([]);

// Edit task functionality
const showEditModal = ref(false);
const currentTask = ref(null);
const editForm = ref({
  title: '',
  description: '',
  difficulty: 'beginner',
  time_limit: null,
  file: null
});
const editFile = ref(null);

// دریافت تمرین‌ها از API
const fetchTasks = async () => {
  const token = useCookie("token").value;
  if (!token) {
    return;
  }

  try {
    if (authStore.user?.role === 'دانشجو') {
      // Student view - get tasks for enrolled courses
      const response = await $api.get(
        "/course/task/student-tasks",
        {
          headers: {
            Authorization: "Bearer " + token,
          },
        }
      );

      if (response.data.status && Array.isArray(response.data.data)) {
        const allTasks = response.data.data.map(task => ({
          id: task.id,
          title: task.title,
          description: task.description || "بدون توضیحات",
          difficulty: task.difficulty,
          file: task.file,
          course: task.course,
          lesson: task.lesson,
          submission: task.submission,
          create_date: task.create_date
        }));

        // Separate tasks into pending and completed
        tasks.value = allTasks.filter(task => !task.submission);
        completedTasks.value = allTasks.filter(task => task.submission);
      }
    } else {
      // Teacher view - get task submissions
      const response = await $api.get(
        "/course/task/teacher-submissions",
        {
          headers: {
            Authorization: "Bearer " + token,
          },
        }
      );

      if (response.data.status && response.data.data) {
        console.log("📊 Teacher submissions response:", response.data.data);
        tasks.value = response.data.data.tasks || [];
        submissions.value = response.data.data.submissions || [];
        console.log("📋 Updated tasks count:", tasks.value.length);
        console.log("📝 Updated submissions count:", submissions.value.length);
        console.log("📋 Tasks data:", tasks.value);
        console.log("📝 Submissions data:", submissions.value);
      }
    }
  } catch (error) {
    console.error("خطا در دریافت داده‌ها:", error.message);
  } finally {
    loading.value = false;
  }
};

// دریافت وضعیت‌های موجود برای پاسخ‌ها
const fetchAnswerStatuses = async () => {
  try {
    const response = await $api.get("/course/task/answer/statuses");
    if (response.data.status && Array.isArray(response.data.data)) {
      answerStatuses.value = response.data.data;
    }
  } catch (error) {
    console.error("خطا در دریافت وضعیت‌ها:", error.message);
  }
};

const difficultyMap = {
  beginner: "مبتدی",
  intermediate: "متوسط",
  advanced: "پیشرفته",
};

// باز کردن offcanvas
const openTaskDetails = (task) => {
  if (!task || !task.id) {
    console.error("⚠ خطا: task یا شناسه آن نامعتبر است!", task);
    return;
  }
  selectedTask.value = task;
  console.log("✅ task انتخاب شده:", selectedTask.value);
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

// Helper functions for styling
const getDifficultyClass = (difficulty) => {
  switch (difficulty) {
    case 'پیشرفته':
      return 'bg-danger text-white';
    case 'متوسط':
      return 'bg-warning text-dark';
    case 'مبتدی':
      return 'bg-success text-white';
    default:
      return 'bg-secondary text-white';
  }
};

const getSubmissionStatusClass = (status) => {
  switch (status) {
    case 'Approved':
    case 'تأیید شده':
      return 'bg-success text-white';
    case 'Rejected':
    case 'رد شده':
      return 'bg-danger text-white';
    case 'Pending Review':
    case 'در انتظار بررسی':
      return 'bg-warning text-dark';
    case 'Under Review':
    case 'در حال بررسی':
      return 'bg-info text-white';
    case 'Needs Revision':
    case 'نیاز به بازنگری':
      return 'bg-warning text-dark';
    default:
      return 'bg-info text-white';
  }
};

const formatDate = (dateString) => {
  if (!dateString) return 'نامشخص';
  try {
    const date = new Date(dateString);
    if (isNaN(date.getTime())) return 'نامشخص';
    return date.toLocaleDateString('fa-IR', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  } catch (error) {
    console.error('Date formatting error:', error);
    return 'نامشخص';
  }
};

const selectedFileName = ref("");
const selectedFile = ref(null);
const uploadDescription = ref(""); // توضیحات آپلود تمرین
const triggerFileInput = () => {
  document.getElementById("fileInput").click();
};

const handleFileUpload = (event) => {
  const file = event.target.files[0];
  if (file) {
    selectedFile.value = file;
    selectedFileName.value = file.name;
  }
};

const handleSubmitExercise = async () => {
  const token = useCookie("token").value;
  if (!token) {
    $sweetalert.error("⚠ خطا: کاربر احراز هویت نشده است.");
    return;
  }

  if (!selectedTask.value || !selectedTask.value.id) {
    $sweetalert.error("⚠ خطا: تمرین انتخاب نشده است!");
    return;
  }

  if (!selectedFile.value) {
    $sweetalert.error("⚠ لطفاً یک فایل برای ارسال انتخاب کنید!");
    return;
  }

  console.log("📌 ارسال تمرین با task_id:", selectedTask.value.id);

  const formData = new FormData();
  formData.append("task_id", selectedTask.value.id); 
  formData.append("description", uploadDescription.value || "بدون توضیح");
  formData.append("file", selectedFile.value);

  try {
    const response = await $api.post("/course/task/answer/create", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
        Authorization: `Bearer ${token}`,
      },
    });

    console.log("📊 Response status:", response.status);
    console.log("📊 Response data:", response.data);

    if (response.data.status === true || response.status === 200 || response.status === 201) {
      $sweetalert.success("✅ تمرین با موفقیت ارسال شد!");
      selectedFileName.value = "";
      selectedFile.value = null;
      uploadDescription.value = "";
      // Close the offcanvas dialog
      showOffcanvas.value = false;
      document.body.style.overflow = "auto";
      // Refresh tasks after submission
      await fetchTasks();
    } else {
      console.warn("⚠️ Unexpected response status:", response.status);
      // Still close dialog and refresh as fallback
      showOffcanvas.value = false;
      document.body.style.overflow = "auto";
      await fetchTasks();
    } 
  } catch (error) {
    console.error("❌ خطا در ارسال تمرین:", error.response?.data || error.message);
    $sweetalert.error("❌ ارسال تمرین با خطا مواجه شد!");
  }
};

// Teacher functions
const viewSubmissionDetails = (submission) => {
  // Open modal or offcanvas to show submission details
  selectedTask.value = submission;
  console.log('Viewing submission details:', selectedTask.value);
  showOffcanvas.value = true;
  document.body.style.overflow = "hidden";
};

const updateSubmissionStatus = async (submission, status) => {
  const token = useCookie("token").value;
  if (!token) {
    $sweetalert.error("⚠ خطا: کاربر احراز هویت نشده است.");
    return;
  }

  // Map status to slug
  const statusMap = {
    'approved': 'approved',
    'rejected': 'rejected'
  };

  const statusSlug = statusMap[status];
  if (!statusSlug) {
    $sweetalert.error("⚠ وضعیت نامعتبر است!");
    return;
  }

  try {
    const response = await $api.post("/course/task/answer/changestatus", {
      answer_id: submission.submission.id,
      status_slug: statusSlug
    }, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (response.data.status) {
      $sweetalert.success(`✅ وضعیت با موفقیت به ${status === 'approved' ? 'تأیید شده' : 'رد شده'} تغییر یافت!`);
      console.log("🔄 Refreshing tasks after status update...");
      // Small delay to ensure database transaction is committed
      await new Promise(resolve => setTimeout(resolve, 500));
      // Force refresh by clearing and refetching
      tasks.value = [];
      submissions.value = [];
      await fetchTasks();
      console.log("✅ Tasks refreshed successfully");
    }
  } catch (error) {
    console.error("❌ خطا در تغییر وضعیت:", error.response?.data || error.message);
    $sweetalert.error("❌ تغییر وضعیت با خطا مواجه شد!");
  }
};

// Task viewing and editing functions
const viewTaskDetails = (task) => {
  selectedTask.value = task;
  showOffcanvas.value = true;
  document.body.style.overflow = "hidden";
};

const editTask = (task) => {
  currentTask.value = task;
  editForm.value = {
    title: task.title,
    description: task.description,
    difficulty: task.difficulty === 'مبتدی' ? 'beginner' : 
                task.difficulty === 'متوسط' ? 'intermediate' : 'advanced',
    time_limit: task.time_limit || null,
    file: null
  };
  editFile.value = null;
  showEditModal.value = true;
  document.body.style.overflow = "hidden";
};

const closeEditModal = () => {
  showEditModal.value = false;
  currentTask.value = null;
  editForm.value = {
    title: '',
    description: '',
    difficulty: 'beginner',
    time_limit: null,
    file: null
  };
  editFile.value = null;
  document.body.style.overflow = "auto";
};

const handleEditFileUpload = (event) => {
  const file = event.target.files[0];
  if (file) {
    editFile.value = file;
  }
};

const saveTaskEdit = async () => {
  const token = useCookie("token").value;
  if (!token) {
    $sweetalert.error("⚠ خطا: کاربر احراز هویت نشده است.");
    return;
  }

  if (!currentTask.value || !currentTask.value.id) {
    $sweetalert.error("⚠ خطا: تمرین انتخاب نشده است!");
    return;
  }

  const formData = new FormData();
  formData.append("task_id", currentTask.value.id);
  formData.append("title", editForm.value.title);
  formData.append("description", editForm.value.description);
  formData.append("difficulty", editForm.value.difficulty);
  
  if (editForm.value.time_limit) {
    formData.append("time_limit", editForm.value.time_limit);
  }
  
  if (editFile.value) {
    formData.append("file", editFile.value);
  }

  try {
    const response = await $api.post("/course/task/edit", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
        Authorization: `Bearer ${token}`,
      },
    });

    if (response.data.status) {
      $sweetalert.success("✅ تمرین با موفقیت ویرایش شد!");
      closeEditModal();
      // Refresh tasks
      await fetchTasks();
    }
  } catch (error) {
    console.error("❌ خطا در ویرایش تمرین:", error.response?.data || error.message);
    $sweetalert.error("❌ ویرایش تمرین با خطا مواجه شد!");
  }
};




definePageMeta({
  layout: "account",
  middleware: ["auth"],
});

onMounted(async () => {
  await Promise.all([
    fetchTasks(),
    fetchAnswerStatuses()
  ]);
});
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
</style>
