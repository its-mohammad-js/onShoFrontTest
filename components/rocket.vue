<template>
  <section class="py-5" ref="section">
    <div class="container">
      <div class="text-center mb-5">
        <div class="d-flex justify-content-center align-items-center">
          <i class="icon icon-filled-rocket text-danger1 fs-1"></i>
          <span class="text-danger1 me-1 fs-1">------</span>
        </div>
        <h2 class="fw-bold">مسیر فنی و حرفه ای تا <span class="text-danger1">استخدام</span></h2>
      </div>
      <div class="py-5"></div>
      <div class="row align-items-center">
        <!-- تصویر موشک (جایگزین شده با انیمیشن) -->
        <div class="col-md-7 text-center p-5 d-flex justify-content-center" style="margin-bottom: -300px">
          <div class="w-100 rocket-wrapper me-5">
            <div class="rocket-container">
              <img ref="rocketShadow" src="/images/rocket/rocket_shadow.png" class="rocket-part shadow_1" />
              <img ref="personShadow" src="/images/rocket/rocket_shadow.png" class="rocket-part shadow_2" />
              <img ref="rocketTower" src="/images/rocket/tower.png" class="rocket-part tower" />
              <img ref="rocketPerson" src="/images/rocket/character.png" class="rocket-part person" />
              <div class="rocket">
                <img ref="rocketBase" src="/images/rocket/rocket_base.png" class="rocket-part base" />
                <img ref="rocketBody1" src="/images/rocket/rocket_body1.png" class="rocket-part body1" />
                <img ref="rocketBody2" src="/images/rocket/rocket_body2.png" class="rocket-part body2" />
                <img ref="rocketTop" src="/images/rocket/rocket_top.png" class="rocket-part top" />
                <img ref="rocketBooster" src="/images/rocket/rocket_booster.png" class="rocket-part booster" />
              </div>
            </div>
          </div>
        </div>

        <!-- مراحل تایم‌لاین (بدون تغییر) -->
        <div class="col-md-5 order-md-1 order-2">
          <div class="d-flex flex-column">
            <!-- گذراندن دوره -->
            <div>
              <div class="d-flex align-items-center">
                <h4 class="fw-bold mb-0 fs-2">گذراندن دوره</h4>
                <div class="flex-grow-1 me-1 border-top h-2-px bg-dark"></div>
                <div
                  class="d-flex justify-content-center align-items-center border border-2 border-dark rounded-circle bg-white h-100-px w-100-px"
                >
                  <i class="icon icon-filled-graduation-cap text-danger1 fs-1"></i>
                </div>
              </div>
              <p class="text-muted max-w-600-px text-end mt-3">لورم ایپسوم متن ساختگی با تولید سادگی نامفهوم از صنعت چاپ...</p>
            </div>

            <!-- استخدام کاری -->
            <div>
              <div class="d-flex align-items-center">
                <h4 class="fw-bold mb-0 fs-2">استخدام کاری</h4>
                <div class="flex-grow-1 me-1 border-top h-2-px bg-dark"></div>
                <div
                  class="d-flex justify-content-center align-items-center border border-2 border-dark rounded-circle bg-white h-100-px w-100-px"
                >
                  <i class="icon icon-filled-briefcase text-danger1 fs-1"></i>
                </div>
              </div>
              <p class="text-muted max-w-600-px text-end mt-3">لورم ایپسوم متن ساختگی با تولید سادگی نامفهوم از صنعت چاپ...</p>
            </div>

            <!-- منتور شغلی -->
            <div>
              <div class="d-flex align-items-center">
                <h4 class="fw-bold mb-0 fs-2">منتور شغلی</h4>
                <div class="flex-grow-1 me-1 border-top h-2-px bg-dark"></div>
                <div
                  class="d-flex justify-content-center align-items-center border border-2 border-dark rounded-circle bg-white h-100-px w-100-px"
                >
                  <i class="icon icon-filled-user-star text-danger1 fs-1"></i>
                </div>
              </div>
              <p class="text-muted max-w-600-px text-end mt-3">لورم ایپسوم متن ساختگی با تولید سادگی نامفهوم از صنعت چاپ...</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from "vue";

const section = ref(null);

onMounted(() => {
  // بررسی اندازه صفحه و تنظیم مقدار threshold مناسب
  const thresholdValue = window.innerWidth < 768 ? 0.4 : 0.7;

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          startAnimation();
        } else {
          resetAnimation(); // وقتی سکشن از دید خارج شد، ریست شود
        }
      });
    },
    { threshold: thresholdValue }
  );

  if (section.value) {
    observer.observe(section.value);
  }
});

const startAnimation = () => {
  setTimeout(() => {
    document.querySelector(".base").classList.add("move-base");
    document.querySelector(".body1").classList.add("move-body1");
    document.querySelector(".body2").classList.add("move-body2");
    document.querySelector(".top").classList.add("move-top");
    document.querySelector(".booster").classList.add("move-booster");
  }, 500);
};

const resetAnimation = () => {
  document.querySelector(".base").classList.remove("move-base");
  document.querySelector(".body1").classList.remove("move-body1");
  document.querySelector(".body2").classList.remove("move-body2");
  document.querySelector(".top").classList.remove("move-top");
  document.querySelector(".booster").classList.remove("move-booster");
};
</script>

<style scoped>
.rocket-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
}

.rocket-container {
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  width: 500px;
  height: 500px;
}

.rocket {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  left: -100px;
}

.rocket-part {
  width: 100px;
  position: absolute;
  transition: transform 1s ease-in-out;
}

.base {
  width: 70px !important;
}

.tower {
  width: 120px;
  position: absolute;
  right: 180px;
  top: 0;
}

.person {
  width: 150px;
  position: absolute;
  right: -50px;
  top: -25px;
}

.shadow_1 {
  width: 150px;
  position: absolute;
  bottom: 100px;
  right: 275px;
  opacity: 0.5;
  z-index: -1;
}

.shadow_2 {
  width: 180px;
  position: absolute;
  right: -75px;
  bottom: 100px;
  opacity: 0.5;
  z-index: -1;
}

/* موقعیت اولیه قطعات برای نمایش یک موشک کامل */
.body1 {
  transform: translateY(-100px);
}
.body2 {
  transform: translateY(-150px);
}
.top {
  transform: translateY(-220px);
}
.booster {
  transform: translateY(-300px);
}

/* حرکت جداگانه برای هر قطعه */
.move-base {
  transform: translateY(0px);
}
.move-body1 {
  transform: translateY(-120px);
}
.move-body2 {
  transform: translateY(-200px);
}
.move-top {
  transform: translateY(-300px);
}
.move-booster {
  transform: translateY(-420px);
}

/* تغییر اندازه برای موبایل */
@media (max-width: 768px) {
  .rocket-part {
    width: 80px;
  }
  .base {
    width: 60px !important;
  }
  .tower {
    width: 100px !important;
    right: 100px;
  }
  .person {
    width: 100px !important;
    right: -50px;
  }
  .shadow_1,
  .shadow_2 {
    width: 100px;
    bottom: 60px;
  }
  .shadow_2 {
    right: -110px;
  }
  .rocket-wrapper {
    margin-bottom: 100px;
  }
  .rocket {
    left: -75px;
  }
  .col-md-7 {
    overflow: hidden;
  }

  .body1 {
    transform: translateY(-50px);
  }
  .body2 {
    transform: translateY(-100px);
  }
  .top {
    transform: translateY(-170px);
  }
  .booster {
    transform: translateY(-250px);
  }

  .move-base {
    transform: translateY(0px);
  }
  .move-body1 {
    transform: translateY(-100px);
  }
  .move-body2 {
    transform: translateY(-150px);
  }
  .move-top {
    transform: translateY(-220px);
  }
  .move-booster {
    transform: translateY(-320px);
  }
  .icon {
    font-size: 2rem !important; /* افزایش سایز آیکون‌ها */
  }

  /* افزایش اندازه‌ی دایره‌های اطراف آیکون‌ها */
  .h-100-px,
  .w-100-px {
    height: 80px !important;
    width: 80px !important;
  }
}
</style>
