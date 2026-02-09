<template>
  <div class="learning-paths py-3 py-md-5">
    <h1 class="title">یاد بگیری کار میکنی</h1>
    <p class="subtitle">
      در این بخش مجموعه‌ای از مهارت‌های کاربردی و شغل‌ساز رو برات آماده کردیم؛
      مهارت‌هایی که با یادگیریشون می‌تونی به‌سرعت وارد بازار کار بشی — چه در
      ایران و چه خارج از کشور. تمام دوره‌ها بر اساس نیاز واقعی صنعت، میزان
      درآمد، و فرصت‌های شغلی روز دنیا طراحی شدن تا مسیرت برای رسیدن به یه شغل
      مطمئن و درآمدزا هموار بشه. هر مسیر آموزشی شامل چند مهارت کلیدی، آموزش
      گام‌به‌گام، و پروژه‌های واقعیه تا بعد از اتمام دوره، آماده ورود به بازار
      کار باشی. با ما یاد می‌گیری، تمرین می‌کنی، و کار پیدا می‌کنی.
    </p>

    <div class="paths">
      <div v-for="path in paths" :key="path.title" class="path-card">
        <h2>{{ path.title }}</h2>
        <ul>
          <li v-for="(skill, i) in path.skills" :key="i">
            <button class="skill-btn" @click="goToSkill(skill)">
              {{ skill }}
            </button>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

const paths = ref([
  {
    title: "تعمیرات لوازم خانگی",
    skills: [
      "تعمیر لباسشویی",
      "تعمیر ظرفشویی",
      "تعمیر یخچال فریزر",
      "نصب و تعمیر پکیج دیواری و آبگرم‌کن",
    ],
  },
  {
    title: "برنامه نویسی فرانت‌اند",
    skills: ["HTML", "CSS", "JavaScript", "React"],
  },
  {
    title: "برنامه نویسی بک‌اند",
    skills: [
      "مهارت عمومی برنامه‌نویسی",
      "برنامه‌نویسی مقدماتی جاوا",
      "برنامه‌نویسی پیشرفته جاوا",
      "برنامه‌نویسی پایتون",
      "HTML",
      "CSS",
    ],
  },
]);

const goToSkill = (skill) => {
  alert(`You clicked on: ${skill}`);
  // In real use: router.push(`/skills/${encodeURIComponent(skill)}`)
};
</script>

<style scoped>
.learning-paths {
  direction: rtl;
  text-align: center;
  padding: 2rem;
  background: #e8f5e9; /* پس‌زمینه سبز بسیار ملایم */
  min-height: 100vh;
}

.title {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  color: #1b5e20; /* سبز تیره برای تیتر اصلی */
}

.subtitle {
  color: #2e7d32; /* سبز متوسط برای متن توضیح */
  max-width: 700px;
  margin: 0 auto 2rem;
}

.paths {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 1.5rem;
}

.path-card {
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.08);
  padding: 1.5rem;
  width: 300px;
  transition: 0.3s;
}

.path-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 16px rgba(0, 0, 0, 0.12);
}

.path-card h2 {
  color: #2e7d32; /* سبز برای تیتر کارت‌ها */
  margin-bottom: 1rem;
  font-size: 1.3rem;
}

ul {
  list-style: none;
  padding: 0;
}

.skill-btn {
  background: #c8e6c9; /* سبز روشن دکمه‌ها */
  color: #1b5e20;
  border: none;
  border-radius: 6px;
  padding: 0.6rem 1rem;
  margin: 0.3rem 0;
  width: 100%;
  cursor: pointer;
  font-weight: 700;
  font-size: 0.85rem;
  line-height: 1.3;
  transition: 0.3s;
}

.skill-btn:hover {
  background: #2e7d32;
  color: #ffffff;
}
</style>
