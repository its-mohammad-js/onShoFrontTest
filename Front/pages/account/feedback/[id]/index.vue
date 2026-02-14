<template>
  <div class="container py-5">
   
    <div class="card mb-4 shadow-none border-0 bg-light px-5">
      <div class="card-body">
        <div class="mb-4">
          <h6 class="mb-3 text-center">احساس شما نسبت به این دوره چیست؟</h6>
          <hr class="fs-5 my-3" />
          <div class="d-flex justify-content-center align-items-center gap-5 py-5">
            <span
              v-for="emotion in emotions"
              :key="emotion.id"
              :class="['emotion-icon', { 'selected': data.feedback.emotion === emotion.id }]"
              @click="setEmotion(emotion.id)"
            >
              <img :src="emotion.icon" :alt="emotion.label" class="w-40-px h-40-px" />
            </span>
          </div>
        </div>
      </div>
    </div>
    <div class="card mb-4 shadow-none border-0 bg-light px-5">
      <div class="card-body">
        <div class="mb-4">
          <h6 class="mb-3 text-center">میزان رضایت شما از این دوره چقدر است؟</h6>
          <hr class="fs-5 my-3" />
          <div class="d-flex justify-content-center align-items-center gap-3 py-3">
            <span
              v-for="star in 5"
              :key="star"
              class="star"
              :class="{ 'active': star <= data.feedback.rating }"
              @click="setRating(star)"
            >

          <i class="icon icon-filled-star fs-2"></i> 
            </span>
          </div>
        </div>
      </div>
    </div>
    <!-- Feedback Section -->
    <div class="card shadow-none border-0 bg-light px-5">
      <div class="card-body">
        <div class="mb-4">
          <h6 class="mb-3 text-center">ثبت بازخورد</h6>
          <hr class="fs-5 my-3" />
          <textarea
            v-model="data.feedback.comment"
            rows="8"
            class="form-control rounded-3"
            placeholder="نظر خود را با دیگران به اشتراک بگذارید."
          ></textarea>
        </div>

        <div class="text-start my-3">
          <button class="btn btn-danger" @click="submitFeedback">ثبت امتیاز و بازخورد</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
const { $api, $sweetalert } = useNuxtApp();
import Swal from "sweetalert2";
import { useRoute } from "vue-router";

const route = useRoute();

const data = reactive({
  feedback: {
    emotion: null,
    rating: "",
    comment: "",
  },
});

const emotions = ref([
  { id: 1, label: "خیلی بد", icon: "https://openmoji.org/data/color/svg/1F621.svg" },
  { id: 2, label: "بد", icon: "https://openmoji.org/data/color/svg/1F641.svg" },
  { id: 3, label: "متوسط", icon: "https://openmoji.org/data/color/svg/1F610.svg" },
  { id: 4, label: "خوب", icon: "https://openmoji.org/data/color/svg/1F642.svg" },
  { id: 5, label: "عالی", icon: "https://openmoji.org/data/color/svg/1F60D.svg" },
]);

const setEmotion = (id) => {
  data.feedback.emotion = id;
};

const setRating = (star) => {
  data.feedback.rating = star;
};


const courseId = route.params.id
const submitFeedback = async () => {
  const payload = {
    course: courseId,
    content: data.feedback.comment,
    rate: data.feedback.rating,
    emotion: data.feedback.emotion,
  };

  await $api
    .post("/course/comment/add", payload, {
      headers: {
        Authorization: "Bearer " + useCookie("token").value,
      },
    })
    .then((value) => {
      Swal.fire({
        icon: "success",
        title: "بازخورد شما ثبت شد!",
        text: "از اینکه نظرتان را با ما به اشتراک گذاشتید، متشکریم . بازخورد شما پس از تایید کارشناسان ما در دوره مربوطه به اشتراک گذاشته خواهد شد .",
      });
    })
    .catch(() => {
      Swal.fire({
        icon: "error",
        title: "خطا در ثبت بازخورد",
        text: error.response?.data?.message || "لطفاً دوباره تلاش کنید.",
      });
    });
};

definePageMeta({
  layout: "account",
  middleware: ['auth']
});
</script>

<style scoped>
.emotion-icon {
  cursor: pointer;
  transition: transform 0.2s;
}
.emotion-icon:hover {
  transform: scale(1.2);
}
.emotion-icon.selected {
  border: 2px solid #dc3545;
  border-radius: 50%;
  padding: 5px;
}

.star {
  cursor: pointer;
  font-size: 1.5rem;
  color: #ddd;
  transition: color 0.2s;
}
.star.active {
  color: #c1121f;
}
.card {
  transform: scale(1) !important;
}
</style>
