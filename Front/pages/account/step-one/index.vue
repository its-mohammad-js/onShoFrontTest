<template>
    <div class="border-none rounded bg-light mt-4">
        <main class="exam-page">
    
      <!-- Header Section -->
      <div class="exam-header d-flex justify-content-between align-items-center bg-danger-subtle p-3 rounded mb-4">
        <div>
          <h6 class="text-danger1 fw-bold mb-0">آزمون نهایی</h6>
        </div>
        <div class="d-flex align-items-center gap-4">
          <span class="text-muted">تعداد سوالات: 20</span>
          <span class="text-muted">زمان آزمون: 45 دقیقه</span>
          <span class="text-danger1 fw-bold">زمان باقی‌مانده: {{ formattedTimer }}</span>
        </div>
      </div>

      <!-- Questions Section -->
     <div class="px-3">
        <div v-for="(question, index) in questions" :key="index" class="question-item p-3 mb-3 rounded bg-light">
        <div class="d-flex justify-content-start gap-2 align-items-center">
          <h6 class="fw-bold badge bg-white rounded-0 p-2 px-3 text-dark border">{{ index + 1 }}</h6>
          <p class="mb-0">{{ question.text }}</p>
        </div>
        <div class="options mt-3 d-flex align-items-center justify-content-between gap-2">
          <button
            v-for="(option, i) in question.options"
            :key="i"
            :class="['btn w-100 py-2 rounded-0', 'me-2', selectedAnswers[index] === i ? (option.isCorrect ? 'btn-success' : 'btn-danger') : 'btn-outline-secondary']"
            @click="selectAnswer(index, i, option.isCorrect)"
          >
            {{ option.text }}
          </button>
        </div>
      </div>
     </div>
   
  </main>
    </div>
  </template>
  
<script setup>
import { ref, computed, onMounted } from 'vue';

const questions = ref([
  {
    text: 'تگ صحیح HTML برای بزرگترین سایز کدام گزینه می‌باشد؟',
    options: [
      { text: 'Headline', isCorrect: false },
      { text: 'H9', isCorrect: false },
      { text: 'H1', isCorrect: true },
      { text: 'H6', isCorrect: false },
    ],
  },
  {
    text: 'تگ صحیح HTML برای بزرگترین سایز کدام گزینه می‌باشد؟',
    options: [
      { text: 'Headline', isCorrect: false },
      { text: 'H9', isCorrect: false },
      { text: 'H1', isCorrect: true },
      { text: 'H6', isCorrect: false },
    ],
  },
  {
    text: 'تگ صحیح HTML برای بزرگترین سایز کدام گزینه می‌باشد؟',
    options: [
      { text: 'Headline', isCorrect: false },
      { text: 'H9', isCorrect: false },
      { text: 'H1', isCorrect: true },
      { text: 'H6', isCorrect: false },
    ],
  },
]);

const selectedAnswers = ref({}); // ذخیره انتخاب‌های کاربر

const selectAnswer = (questionIndex, optionIndex, isCorrect) => {
  selectedAnswers.value[questionIndex] = optionIndex;
};

const timer = ref(2700); // 45 دقیقه = 2700 ثانیه

const formattedTimer = computed(() => {
  const minutes = Math.floor(timer.value / 60)
    .toString()
    .padStart(2, '0');
  const seconds = (timer.value % 60).toString().padStart(2, '0');
  return `${minutes}:${seconds}`;
});

onMounted(() => {
  const interval = setInterval(() => {
    if (timer.value > 0) {
      timer.value--;
    } else {
      clearInterval(interval);
    }
  }, 1000);
});
definePageMeta({
  layout: "account",
  middleware: ['auth']
});
</script>
  
<style scoped>
main {
    min-height: 100vh !important;
}
.exam-header {
  background-color: #fdf7f7;
}
.options .btn {
  min-width: 100px;
}

.btn-success {
  background-color: #28a745 !important;
  border: none;
  color: white;
}

.btn-danger {
  background-color: #dc3545 !important;
  border: none;
  color: white;
}
</style>
  