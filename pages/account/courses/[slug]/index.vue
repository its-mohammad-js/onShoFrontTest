<template>
    <div class="container py-5">
      <div class="row">
        <!-- Main Content -->
        <div class="col-md-9">
          <div v-if="selectedLesson" class="card border-0">
            <div class="card-header border-0 bg-white py-3">
              <h5>{{ selectedLesson.title }}</h5>
              <div class="d-flex align-items-center justify-content-start gap-4 mt-3">
                <span>
                  <i class="fa-solid fa-clock text-danger1 ms-1"></i>
                   <span class="text-dark">{{ selectedLesson.duration }} دقیقه</span>
                </span>
                <span>
                 
                برگزارکننده : <span class="text-danger1">{{ selectedLesson.organizer }}</span>
                </span>
                <span>
                  <i class="fa-solid fa-chalkboard-teacher text-danger1 ms-1"></i>
                  مدرس : <span class="text-danger1">{{ selectedLesson.teacher }}</span>
                </span>
              </div>
            </div>
            <div class="card-body">
              <!-- Video Section -->
              <div class="video-wrapper mb-4">
                <video
                  :src="selectedLesson.video"
                   :poster="selectedLesson.preview"
                  class="w-100 rounded"
                  controls
                  crossorigin="anonymous"
                  preload="metadata"
                ></video>
              </div>
              <!-- Lesson Notes -->
              <div class="d-flex align-items-center">
                <h5 class="text-danger1 py-3 border-bottom border-danger border-5">توضیحات</h5>
              </div>
              <ul class="list-group list-group-flush bg-light rounded-3">
                <li
                  v-for="(note, noteIndex) in selectedLesson.notes"
                  :key="noteIndex"
                  class="list-group-item bg-light py-3"
                >
                  <i class="fa-solid fa-circle-check text-success ms-1"></i>
                  {{ note }}
                </li>
              </ul>
            </div>
          </div>
          <div v-else class="text-center">
            <p class="text-muted">لطفاً یک جلسه را انتخاب کنید.</p>
          </div>
        </div>
  
        <!-- Sidebar with Accordion -->
        <div class="col-md-3">
          <div id="accordion bg-light border-o">
            <div
              v-for="(chapter, chapterIndex) in chapters"
              :key="chapterIndex"
              class="card border-0 shadow-none"
            >
              <div
                class="card-header cursor-pointer d-flex justify-content-between align-items-center"
                @click="toggleChapter(chapterIndex)"
              >
                <h5 class="mb-0">
                  <a
                    class="btn text-dark text-decoration-none"
                    :class="chapterIndex === activeChapter ? 'text-danger1' : ''"
                  >
                    {{ chapter.title }}
                  </a>
                </h5>
                <span
                  class="badge bg-danger text-white"
                  v-if="chapter.lessons.length > 0"
                >
                  {{ chapter.lessons.length }}
                </span>
              </div>
              <div v-show="chapterIndex === activeChapter" class="card-body p-0">
                <ul class="list-group border-0">
                  <li
                    v-for="(lesson, lessonIndex) in chapter.lessons"
                    :key="lessonIndex"
                    class="list-group-item d-flex justify-content-between align-items-center bg-light cursor-pointer"
                    @click="loadLesson(lesson)"
                  >
                    <span>
                      <i
                        class="fa-solid fa-check text-success ms-1"
                        v-if="lesson.completed"
                      ></i>
                      {{ lesson.title }}
                    </span>
                    <i
                      class="fa-solid fa-play-circle text-danger1"
                      style="cursor: pointer"
                    ></i>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from "vue";
  
  const chapters = ref([
  {
    title: "فصل اول",
    lessons: [
      {
        title: "ساخت فرم های ثبت نام",
        teacher: "مریم نجفی",
        duration: 40,
        organizer: "های وب",
        video: "https://via.placeholder.com/640x360",
        preview: "https://via.placeholder.com/640x360?text=Preview+1",
        notes: ["لورم ایپسوم متن ساختگی با تولید سادگی.", "یادداشت دوم."],
        completed: true,
      },
      {
        title: "آشنایی با ورودی ها",
        teacher: "مریم نجفی",
        duration: 35,
        organizer: "های وب",
        video: "https://via.placeholder.com/640x360",
        preview: "https://via.placeholder.com/640x360?text=Preview+2",
        notes: ["یادداشت ۱.", "یادداشت ۲."],
        completed: false,
      },
    ],
  },
  {
    title: "فصل دوم",
    lessons: [
      {
        title: "مقدمات جاوااسکریپت",
        teacher: "مریم نجفی",
        duration: 50,
        organizer: "های وب",
        video: "https://via.placeholder.com/640x360",
        preview: "/images/home/rocket.png",
        notes: ["یادداشت جلسه ۱.", "یادداشت جلسه ۲."],
        completed: false,
      },
    ],
  },
]);
  
  const activeChapter = ref(null);
  const selectedLesson = ref(null);
  
  const toggleChapter = (index) => {
    activeChapter.value = activeChapter.value === index ? null : index;
  };
  
  const loadLesson = (lesson) => {
    selectedLesson.value = lesson;
  };
  definePageMeta({
  layout: "account",
  middleware: ['auth']
});
  </script>
  
  <style scoped>
  .video-wrapper {
    position: relative;
    width: 650px !important;
    height: 525px !important;
    padding-top: 56.25%;
    overflow: hidden;
  }
  
  .video-wrapper video {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
  .cursor-pointer {
    cursor: pointer;
  }
  .card {
  transform: scale(1) !important;
}
  </style>
  