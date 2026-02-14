<template>
  <div class="container py-5">
    <div class="card shadow-sm p-4">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h4 class="fw-bold">
          <i class="fa-solid fa-layer-group text-danger"></i> ایجاد تمرین
        </h4>
      </div>

      <form @submit.prevent="submitForm">
        <!-- انتخاب دوره -->
        <div class="mb-3">
          <label for="course" class="form-label fw-bold">انتخاب دوره:</label>
          <select
            id="course"
            v-model="data.course_id"
            @change="onCourseChange"
            class="form-control py-3 shadow-none"
          >
            <option value="">انتخاب دوره</option>
            <option v-for="course in courses" :key="course.id" :value="course.id">
              {{ course.title }}
            </option>
          </select>
        </div>

        <!-- انتخاب درس -->
        <div class="mb-3">
          <label for="lesson" class="form-label fw-bold">انتخاب درس:</label>
          <select
            id="lesson"
            v-model="data.lesson_id"
            class="form-control py-3 shadow-none"
            :disabled="!data.course_id"
          >
            <option value="">انتخاب درس (اختیاری)</option>
            <option v-for="lesson in selectedLessons" :key="lesson.id" :value="lesson.id">
              {{ lesson.title }} 
              <template v-if="lesson.chapter_title || lesson.chapter">
                ({{ lesson.chapter_title || lesson.chapter }})
              </template>
            </option>
          </select>
        </div>

        <!-- نام تمرین -->
        <div class="mb-3">
          <label for="title" class="form-label fw-bold">نام تمرین:</label>
          <input
            type="text"
            id="title"
            class="form-control py-3 shadow-none"
            placeholder="نام تمرین را وارد کنید"
            v-model="data.title"
          />
        </div>

        <!-- توضیحات تمرین -->
        <div class="mb-3">
          <label for="description" class="form-label fw-bold">توضیحات تمرین:</label>
          <textarea
            id="description"
            class="form-control py-3 shadow-none"
            rows="4"
            placeholder="توضیحات تمرین را وارد کنید"
            v-model="data.description"
          ></textarea>
        </div>

        <!-- درجه سختی -->
        <div class="mb-3">
          <label class="form-label fw-bold">درجه سختی:</label>
          <div class="d-flex flex-wrap gap-2">
            <div v-for="(label, key) in difficultyMapping" :key="key" class="form-check flex-grow-1">
              <label
                class="form-check-label w-100 d-flex align-items-center justify-content-center position-relative"
                :for="'radio-difficulty-' + key"
              >
                <input
                  class="form-check-input"
                  type="radio"
                  name="difficulty"
                  :id="'radio-difficulty-' + key"
                  :value="key"
                  v-model="data.selectedDifficulty"
                />
                <span class="dot"></span>
                <span class="label-text">{{ label }}</span>
              </label>
            </div>
          </div>
        </div>

        <!-- زمان پاسخ‌دهی -->
        <div class="mb-3">
          <label for="time_limit" class="form-label fw-bold">زمان پاسخ‌دهی (دقیقه):</label>
          <input
            type="number"
            id="time_limit"
            class="form-control py-3 shadow-none"
            placeholder="زمان پاسخ‌دهی به دقیقه (اختیاری)"
            v-model="data.time_limit"
            min="1"
            max="1440"
          />
          <small class="form-text text-muted">زمان پاسخ‌دهی به دقیقه (حداکثر 1440 دقیقه = 24 ساعت)</small>
        </div>

        <!-- پیوست -->
        <div class="my-5 d-flex align-items-center justify-content-between">
          <label class="form-label fw-bold d-flex align-items-center ms-5">
            <i class="fa-solid fa-paperclip text-muted ms-2"></i> پیوست:
          </label>
          <div class="file-upload-box text-center" @click="triggerFileInput">
            <input
              type="file"
              ref="fileInput"
              class="d-none"
              @change="handleFileUpload"
            />
            <span class="file-text" :class="{ 'text-danger': !data.file }">
              {{ data.file ? data.file.name : "انتخاب فایل تمرین" }}
            </span>
          </div>
        </div>

        <!-- دکمه ثبت -->
        <div class="text-center mt-4">
          <button type="submit" class="btn btn-danger py-3 px-4">ثبت تمرین</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from "vue";
import { useNuxtApp, useCookie } from "#app";
import { useRouter } from "vue-router";

definePageMeta({
  layout: "account",
  middleware: ["auth"],
});

const { $api, $sweetalert } = useNuxtApp();
const router = useRouter();
const { canCreateTask, organizationStatusMessage, fetchOrganization } = useOrganization()

// اطلاعات فرم
const data = reactive({
  title: "",
  description: "",
  course_id: "",
  lesson_id: "",
  file: null,
  selectedDifficulty: "beginner", // مقدار پیش‌فرض
  time_limit: null, // زمان پاسخ‌دهی به دقیقه
});

// داده‌های دوره‌ها و دروس
const courses = ref([]);
const selectedLessons = ref([]);

// نگاشت درجه سختی (نمایش فارسی، ارسال انگلیسی)
const difficultyMapping = {
  beginner: "مبتدی",
  intermediate: "متوسط",
  advanced: "پیشرفته",
};

// مقدار difficulty نهایی که به API ارسال خواهد شد
const difficultyToSend = computed(() => data.selectedDifficulty);

const fileInput = ref(null);

// انتخاب فایل
const triggerFileInput = () => {
  fileInput.value.click();
};

// پردازش فایل آپلود شده
const handleFileUpload = (event) => {
  const file = event.target.files[0];
  if (file) {
    data.file = file;
  }
};

// بارگذاری دوره‌ها و دروس
const loadCoursesAndLessons = async () => {
  try {
    const token = useCookie("token").value;
    
    if (!token) {
      console.error('❌ No token found');
      $sweetalert.error('لطفاً ابتدا وارد حساب کاربری خود شوید');
      return;
    }

    console.log('📡 Fetching courses from /course/modares/list');
    
    // استفاده از API که دوره‌های مدرس را برمی‌گرداند
    const response = await $api.post('/course/modares/list', {}, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    console.log('📊 API Response:', response.data);
    
    if (response.data.status && response.data.data) {
      let coursesData = [];
      
      // بررسی ساختار پاسخ
      if (Array.isArray(response.data.data)) {
        coursesData = response.data.data;
      } else if (response.data.data.results && Array.isArray(response.data.data.results)) {
        coursesData = response.data.data.results;
      } else if (response.data.data.data && Array.isArray(response.data.data.data)) {
        coursesData = response.data.data.data;
      }
      
      // دریافت جزئیات کامل هر دوره شامل chapters و lessons
      const coursesWithDetails = await Promise.all(
        coursesData.map(async (course) => {
          try {
            const detailResponse = await $api.post(
              '/course/user/detail',
              { course_id: course.id },
              {
                headers: {
                  Authorization: `Bearer ${token}`,
                },
              }
            );
            
            if (detailResponse.data.status && detailResponse.data.data) {
              const courseDetail = detailResponse.data.data;
              return {
                id: course.id,
                title: course.title || courseDetail.title,
                chapters: courseDetail.chapters || [],
                lessons: courseDetail.lessons || [] // برای سازگاری با ساختار قدیمی
              };
            }
            return {
              id: course.id,
              title: course.title,
              chapters: [],
              lessons: []
            };
          } catch (error) {
            console.error(`❌ Error fetching details for course ${course.id}:`, error);
            return {
              id: course.id,
              title: course.title,
              chapters: [],
              lessons: []
            };
          }
        })
      );
      
      // اطمینان از اینکه هر دوره دارای ساختار درستی است
      courses.value = coursesWithDetails.map(course => {
        if (course.chapters && Array.isArray(course.chapters)) {
          course.chapters = course.chapters.map(chapter => ({
            ...chapter,
            lessons: chapter.lessons || []
          }));
        }
        return course;
      });
      
      console.log('✅ Courses loaded:', courses.value);
      console.log('📚 Courses structure:', courses.value.map(c => ({
        id: c.id,
        title: c.title,
        hasChapters: !!c.chapters,
        chaptersCount: c.chapters?.length || 0,
        totalLessons: c.chapters?.reduce((sum, ch) => sum + (ch.lessons?.length || 0), 0) || 0
      })));
      
      if (courses.value.length === 0) {
        $sweetalert.fire({
          title: 'هیچ دوره‌ای یافت نشد',
          text: 'لطفاً ابتدا یک دوره ایجاد کنید',
          icon: 'info',
          confirmButtonText: 'متوجه شدم'
        });
      }
    } else {
      console.error('❌ API returned status false:', response.data);
      $sweetalert.error('خطا در دریافت لیست دوره‌ها');
    }
  } catch (error) {
    console.error('❌ Error loading courses and lessons:', error);
    console.error('Error details:', error.response?.data);
    $sweetalert.error('خطا در دریافت اطلاعات دوره‌ها. لطفاً دوباره تلاش کنید.');
  }
};

// تغییر دوره
const onCourseChange = () => {
  data.lesson_id = '';
  
  if (data.course_id) {
    const selectedCourse = courses.value.find(course => course.id == data.course_id);
    
    if (selectedCourse) {
      // اگر دوره دارای chapters است (ساختار جدید)
      if (selectedCourse.chapters && Array.isArray(selectedCourse.chapters)) {
        // استخراج همه درس‌ها از همه فصل‌ها
        const allLessons = [];
        selectedCourse.chapters.forEach(chapter => {
          if (chapter.lessons && Array.isArray(chapter.lessons)) {
            chapter.lessons.forEach(lesson => {
              allLessons.push({
                ...lesson,
                chapter_title: chapter.title || chapter.name || 'بدون فصل',
                chapter_id: chapter.id
              });
            });
          }
        });
        selectedLessons.value = allLessons;
      }
      // اگر دوره دارای lessons مستقیم است (ساختار قدیمی)
      else if (selectedCourse.lessons && Array.isArray(selectedCourse.lessons)) {
        selectedLessons.value = selectedCourse.lessons;
      }
      // اگر هیچکدام نیست
      else {
        selectedLessons.value = [];
      }
    } else {
      selectedLessons.value = [];
    }
  } else {
    selectedLessons.value = [];
  }
  
  console.log('📚 Selected lessons:', selectedLessons.value);
};

// Check organization status on mount
onMounted(async () => {
  await fetchOrganization();
  
  if (!canCreateTask.value) {
    await $sweetalert.fire({
      title: 'دسترسی محدود',
      text: organizationStatusMessage.value || 'سازمان شما فعال نیست',
      icon: 'warning',
      confirmButtonText: 'متوجه شدم'
    });
    router.push('/account');
    return;
  }
  
  // Load courses and lessons
  await loadCoursesAndLessons();
});

// ارسال فرم به API
const submitForm = async () => {
  try {
    const token = useCookie("token").value; // دریافت مقدار توکن
    if (!token) {
      $sweetalert.error("توکن یافت نشد! لطفا مجددا وارد شوید.");
      return;
    }

    console.log("📌 مقدار difficulty که ارسال می‌شود:", difficultyToSend.value); // بررسی مقدار difficulty

    const formData = new FormData();
    formData.append("title", data.title);
    formData.append("description", data.description);
    formData.append("difficulty", difficultyToSend.value); // ارسال مقدار انتخاب‌شده
    formData.append("course_id", data.course_id);
    if (data.lesson_id) {
      formData.append("lesson_id", data.lesson_id);
    }
    if (data.time_limit) {
      formData.append("time_limit", data.time_limit);
    }
    if (data.file) {
      formData.append("file", data.file);
    }

    // ارسال درخواست با استفاده از $api
    const response = await $api.post("/course/task/create", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
        Authorization: `Bearer ${token}`,
      },
    });

    $sweetalert.success("تمرین با موفقیت ثبت شد!");
    console.log("✅ تمرین با موفقیت ارسال شد:", response.data);
  } catch (error) {
    console.error("❌ خطا در ارسال فرم:", error.response ? error.response.data : error);
    $sweetalert.error(error.response?.data?.message || "مشکلی رخ داده است، لطفا دوباره امتحان کنید.");
  }
};
</script>
  
  
  <style scoped>
  .card {
    transform: scale(1) !important;
  }
  
  .input-group-text {
    border-radius: 8px 0 0 8px !important;
  }
  
  .form-control {
    border-radius: 8px;
  }
  
  .cursor-pointer {
    cursor: pointer;
  }
  
  /* استایل دکمه‌های انتخاب درجه سختی */
  .form-check {
    border: 1px solid rgba(251, 241, 242, 1);
    border-radius: 120px;
    background-color: rgba(251, 241, 242, 1);
    position: relative;
    transition: all 0.3s ease;
    padding: 10px 20px;
    text-align: center;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .form-check-input {
    display: none;
  }
  
  .form-check-input:checked + .dot {
    background-color: rgba(220, 53, 69, 1);
  }
  
  .form-check-input:checked ~ .label-text {
    color: #000;
    font-weight: bold;
  }
  
  .form-check-label {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #000;
    font-weight: bold;
    padding: 5px 10px;
    text-align: center;
    transition: color 0.3s ease;
  }
  
  .dot {
    width: 8px;
    height: 8px;
    background-color: transparent;
    border-radius: 50%;
    position: absolute;
    top: 50%;
    right: 10px;
    transform: translateY(-50%);
    transition: background-color 0.3s ease;
  }
  
  .label-text {
    margin-right: 15px;
    color: #000;
    transition: color 0.3s ease;
  }
  
  .form-check:hover {
    background-color: rgba(220, 53, 69, 0.1);
  }
  
  .file-upload-box {
    width: 100%;
    padding: 15px;
    border: 2px dashed #d1d1d1;
    border-radius: 8px;
    background-color: #f8f9fa;
    cursor: pointer;
    transition: all 0.3s ease;
  }
  
  .file-upload-box:hover {
    background-color: #f1f1f1;
  }
  
  .file-text {
    font-weight: bold;
    font-size: 16px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    display: block;
  }
  
  @media (max-width: 768px) {
    .form-check {
      padding: 8px 15px;
    }
    .label-text {
      font-size: 14px;
    }
    .dot {
      width: 6px;
      height: 6px;
    }
  }
  </style>
  