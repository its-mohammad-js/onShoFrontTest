<template>
  <div>
    <h6 class="mb-3 fw-bold">مدیریت ساختار دوره</h6>

    <div class="mb-4">
    <form @submit.prevent="createChapter">
      <div class="row bg-white p-3 rounded-3 mb-3">
        <div class="col-md-9">
          <label for="chapterName" class="form-label">نام فصل:</label>
          <input
            type="text"
            id="chapterName"
            v-model="data.newChapter"
            class="form-control py-3 shadow-none"
            placeholder="نام فصل را وارد کنید"
          />
        </div>
        <div class="col-md-3 d-flex align-items-end justify-content-center">
          <button type="submit" class="btn btn-danger w-100 py-3">افزودن فصل</button>
        </div>
      </div>
    </form>
  </div>

  <div id="accordion">
    <div
      v-for="(chapter, chapterIndex) in data.chapters"
      :key="chapterIndex"
      class="accordion-item  rounded my-5 p-3 border"
    >
      <h2 class="accordion-header mb-3" :id="'heading' + chapterIndex">
        <button
          class="accordion-button"
          type="button"
          data-bs-toggle="collapse"
          :data-bs-target="'#collapse' + chapterIndex"
          aria-expanded="true"
          :aria-controls="'collapse' + chapterIndex"
        >
          {{ chapter.title }}
        </button>
      </h2>
      <div
        :id="'collapse' + chapterIndex"
        class="accordion-collapse collapse"
        :aria-labelledby="'heading' + chapterIndex"
        data-bs-parent="#accordion"
      >
        <div class="accordion-body">
          <form @submit.prevent="addLesson(chapterIndex)">
            <div class="row bg-white p-3 rounded-3 mb-3">
              <div class="col-md-4 mb-3">
                <label for="lessonName" class="form-label">نام درس:</label>
                <input
                  type="text"
                  id="lessonName"
                  v-model="data.newLesson.title"
                  class="form-control py-3 shadow-none"
                  placeholder="نام درس را وارد کنید"
                />
              </div>
              <div class="col-md-4 mb-3">
                <label for="lessonDescription" class="form-label">توضیحات:</label>
                <input
                  type="text"
                  id="lessonDescription"
                  v-model="data.newLesson.description"
                  class="form-control py-3 shadow-none"
                  placeholder="توضیحات درس"
                />
              </div>
              <div class="col-md-4 mb-3">
                <label for="lessonVideoLink" class="form-label">لینک ویدیو:</label>
                <input
                  type="url"
                  id="lessonVideoLink"
                  v-model="data.newLesson.videoLink"
                  class="form-control py-3 shadow-none"
                  placeholder="https://example.com/video.mp4"
                />
              </div>
              <div class="col-md-12">
                <button type="submit" class="btn btn-danger w-100">افزودن درس</button>
              </div>
            </div>
          </form>

          <ul class="list-group">
            <li
              v-for="(lesson, lessonIndex) in chapter.lessons"
              :key="lessonIndex"
              class="list-group-item d-flex justify-content-between align-items-center"
            >
              <div>
                <div class="d-flex align-items-center mb-1">
                  <strong>{{ lesson.title }}</strong>
                  <span v-if="lesson.is_verified" class="badge bg-success ms-2">
                    <i class="fas fa-check-circle me-1"></i>تأیید شده
                  </span>
                  <span v-else class="badge bg-warning ms-2">
                    <i class="fas fa-clock me-1"></i>در انتظار تأیید
                  </span>
                </div>
                <p class="mb-0 small text-muted">{{ lesson.description }}</p>
                <p v-if="lesson.video_link" class="mb-0 small text-primary">
                  <i class="fas fa-video me-1"></i>
                  <a :href="lesson.video_link" target="_blank" class="text-decoration-none">
                    {{ lesson.video_link }}
                  </a>
                </p>
              </div>
              <button
                class="btn btn-sm btn-danger"
                @click="removeLesson(chapterIndex, lessonIndex)"
              >
                حذف درس
              </button>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
  </div>
</template>

<script setup>
import { ref, computed, watchEffect, onMounted } from "vue";
import { useNuxtApp } from "#app";

const props = defineProps({
  modelValue: {
    type: Object,
    required: true,
  },
});

const { $api, $sweetalert } = useNuxtApp();
const emit = defineEmits(["update:modelValue"]);

const data = computed(() => props.modelValue);
const isLoaded = ref(false);

// Debug logging
console.log("🔍 Chapter-lesson-manager mounted with data:", data.value);
console.log("🔍 CourseId from props:", data.value.courseId);
console.log("🔍 Full data object keys:", Object.keys(data.value));

const fetchChapters = async () => {
  if (!data.value.courseId) {
    console.warn("⚠️ courseId مقدار ندارد!");
    return;
  }

  try {
    const response = await $api.post(
      "/course/user/detail",
      { course_id: data.value.courseId },
      {
        headers: {
          Authorization: "Bearer " + useCookie("token").value,
        },
      }
    );

    const course = response.data.data;

    if (course && course.chapters) {
      // اطمینان از اینکه هر chapter دارای lessons است
      data.value.chapters = course.chapters.map(chapter => ({
        ...chapter,
        lessons: chapter.lessons || []
      }));
    } else {
      data.value.chapters = [];
      console.warn("⚠️ هیچ فصلی دریافت نشد.");
    }
  } catch (error) {
    console.error("❌ خطا در دریافت اطلاعات فصل‌ها:", error);
  }
};

const createChapter = () => {
  if (!data.value.newChapter.trim()) {
    $sweetalert.error("لطفاً نام فصل را وارد کنید.");
    return;
  }

  if (!data.value.courseId) {
    console.error("❌ Course ID is missing:", data.value.courseId);
    $sweetalert.error("شناسه دوره یافت نشد. لطفاً صفحه را رفرش کنید.");
    return;
  }

  console.log("🔍 Creating chapter with courseId:", data.value.courseId);
  const formData = new FormData();
  formData.append("course", data.value.courseId);
  formData.append("title", data.value.newChapter);
  formData.append("order", data.value.chapters.length + 1);

  $api
    .post("/course/chapter/create", formData, {
      headers: {
        Authorization: "Bearer " + useCookie("token").value,
      },
    })
    .then((response) => {
      if (response.data.status) {
        $sweetalert.success("فصل جدید با موفقیت اضافه شد!");
        data.value.newChapter = "";
        data.value.chapters.push(response.data.data);
      }
    })
    .catch((error) => {
      console.error("خطا در ایجاد فصل:", error);
      $sweetalert.error("خطایی در ایجاد فصل رخ داده است.");
    });
};
const addLesson = async (chapterIndex) => {
  const chapter = data.value.chapters[chapterIndex];

  if (!chapter || !chapter.id) {
    console.error("❌ خطا: Chapter ID وجود ندارد!", chapter);
    $sweetalert.error("فصل موردنظر یافت نشد.");
    return;
  }

  if (!data.value.newLesson?.title.trim()) {
    $sweetalert.error("لطفاً نام درس را وارد کنید.");
    return;
  }

  if (!data.value.courseId) {
    console.error("❌ خطا: courseId مقدار ندارد!");
    $sweetalert.error("مشکلی در شناسه دوره وجود دارد.");
    return;
  }

  const formData = new FormData();
  formData.append("chapter", chapter.id); // ID فصل
  formData.append("title", data.value.newLesson?.title || ""); // مقدار title به جای content
  formData.append("course", data.value.courseId || ""); 
  formData.append("content", data.value.newLesson?.description || "");

  // Add video link instead of file
  if (data.value.newLesson?.videoLink) {
    formData.append("video_link", data.value.newLesson.videoLink);
  }

  console.log("📤 داده‌های ارسالی به API:", Object.fromEntries(formData.entries()));

  try {
    const response = await $api.post("/course/lesson/create", formData, {
      headers: {
        Authorization: "Bearer " + useCookie("token").value,
      },
    });

    if (response.data.status) {
      $sweetalert.success("درس جدید با موفقیت اضافه شد!");

      // 🟢 اضافه کردن درس جدید به لیست فصل‌ها بدون نیاز به رفرش
      data.value.chapters[chapterIndex].lessons.push(response.data.data);

      // پاک کردن فرم بعد از ارسال موفق
      data.value.newLesson = { title: "", description: "", videoLink: "" };
    }
  } catch (error) {
    console.error("❌ خطا در ایجاد درس:", error.response?.data || error);
    $sweetalert.error("خطایی در ایجاد درس رخ داده است.");
  }
};

import Swal from "sweetalert2";

const removeLesson = (chapterIndex, lessonIndex) => {
  Swal.fire({
    title: "آیا مطمئن هستید؟",
    text: "این درس برای همیشه حذف خواهد شد!",
    icon: "warning",
    showCancelButton: true,
    confirmButtonColor: "#d33",
    cancelButtonColor: "#3085d6",
    confirmButtonText: "بله، حذف شود!",
    cancelButtonText: "لغو",
  }).then((result) => {
    if (result.isConfirmed) {
      // 🟢 حذف درس از لیست `lessons`
      data.value.chapters[chapterIndex].lessons.splice(lessonIndex, 1);

      // 🟢 ذخیره تغییرات در `modelValue` و ارسال آن به والد
      emit("update:modelValue", { ...data.value });

      // پیام موفقیت
      Swal.fire("حذف شد!", "درس با موفقیت حذف شد.", "success");
    }
  });
};


// File upload function removed - now using video links instead

watchEffect(() => {
  if (!isLoaded.value && data.value.courseId && (!data.value.chapters || data.value.chapters.length === 0)) {
    fetchChapters();
    isLoaded.value = true; // جلوگیری از فراخوانی مکرر
  }
});


onMounted(() => {
  if (!data.value.chapters || data.value.chapters.length === 0) {
    fetchChapters();
  }
  console.log("🔍 مقدار courseId:", data.value.courseId);
  if (!data.value.courseId) {
    console.error("⚠️ courseId مقدار ندارد!");
  }
});
</script>




