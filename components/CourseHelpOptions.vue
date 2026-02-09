<template>
  <section class="help-section py-3 py-md-5">
    <div class="container" dir="rtl">
      <!-- Title + description (keep these) -->
      <div class="text-center mb-5">
        <h4 class="fw-bold">آموزش مورد نیاز خود را پیدا نکردید؟</h4>
        <p class="lead desc">
          پلتفرم تلاش خود را کرده است تا مرجع جامعی از دوره‌های حضوری و غیرحضوری
          آموزشگاه‌های کشور گردآوری کند. اما اگر آموزش مورد نیازتان را نیافتید،
          از یکی از راه‌های زیر استفاده کنید.
        </p>
      </div>

      <!-- Cards row (like the image) -->
      <!-- Desktop: Grid layout -->
      <div
        class="cards-container-desktop d-none d-md-flex justify-content-center"
      >
        <div v-for="item in items" :key="item.id" class="help-card-wrapper">
          <div
            class="help-card"
            @click="onClick(item)"
            :aria-label="item.label"
            role="button"
            tabindex="0"
            @keydown.enter="onClick(item)"
          >
            <div class="help-card-icon">
              <i :class="item.icon"></i>
            </div>
            <h5 class="help-card-title">{{ item.label }}</h5>
          </div>
        </div>
      </div>

      <!-- Mobile: Grid layout (4 items in one row) -->
      <div class="cards-container-mobile d-md-none">
        <div class="cards-grid-wrapper">
          <div v-for="item in items" :key="item.id" class="help-card-mobile">
            <div
              class="help-card"
              @click="onClick(item)"
              :aria-label="item.label"
              role="button"
              tabindex="0"
              @keydown.enter="onClick(item)"
            >
              <div class="help-card-icon">
                <i :class="item.icon"></i>
              </div>
              <h5 class="help-card-title">{{ item.label }}</h5>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
const items = [
  {
    id: 1,
    label: "پیش ثبت‌نام دوره‌های حضوری",
    action: "preRegister",
    icon: "icon icon-filled-calendar",
  },
  {
    id: 2,
    label: "ویکی مهارت",
    action: "wiki",
    icon: "icon icon-filled-book",
  },
  {
    id: 3,
    label: "کتابخانه",
    action: "library",
    icon: "icon icon-filled-graduation-cap",
  },
  {
    id: 4,
    label: "درخواست ضبط دوره",
    action: "requestRecord",
    icon: "icon icon-filled-camera",
  },
];

const onClick = (item) => {
  // placeholder action — you can replace with router push or emit
  // e.g. useRouter().push({ name: 'search', query: { q: '...' }})
  console.log("clicked:", item);
  // Example: emit or router navigation can be added here
};
</script>

<style scoped>
.help-section {
  background: #d6e6f6; /* پس‌زمینه آبی روشن */
  background-image:
    radial-gradient(
      circle at 20% 50%,
      rgba(147, 112, 219, 0.1) 0%,
      transparent 50%
    ),
    radial-gradient(
      circle at 80% 80%,
      rgba(147, 112, 219, 0.08) 0%,
      transparent 50%
    ),
    radial-gradient(
      circle at 40% 20%,
      rgba(147, 112, 219, 0.06) 0%,
      transparent 50%
    );
  direction: rtl;
  color: #111;
  padding-top: 3rem;
  padding-bottom: 3rem;
  position: relative;
  overflow: hidden;
}

/* title & description */
.desc {
  max-width: 900px;
  margin: 0 auto;
  color: #222;
  line-height: 1.9;
  font-size: 14px;
}

/* Cards container - Desktop */
.cards-container-desktop {
  flex-wrap: wrap;
  gap: 1rem;
}

.help-card-wrapper {
  flex: 0 0 auto;
  width: calc(25% - 0.75rem);
  max-width: 220px;
  min-width: 180px;
}

@media (min-width: 992px) {
  .help-card-wrapper {
    flex: 0 0 calc(25% - 0.75rem);
    max-width: 220px;
    min-width: 180px;
  }
}

/* Cards container - Mobile (Grid layout - 4 items in one row) */
.cards-container-mobile {
  padding: 0;
  margin: 0;
}

.cards-grid-wrapper {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 0.5rem;
  padding: 0.5rem 0;
}

.help-card-mobile {
  width: 100%;
  min-width: 0;
}

/* Cards - like the image */
.help-card {
  background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
  border-radius: 16px;
  padding: 2rem 1.25rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border: 1px solid rgba(0, 0, 0, 0.05);
  position: relative;
  overflow: hidden;
}

/* Gradient background overlay */
.help-card::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(
    135deg,
    rgba(147, 112, 219, 0.05) 0%,
    rgba(147, 112, 219, 0.02) 50%,
    transparent 100%
  );
  opacity: 0;
  transition: opacity 0.3s ease;
  pointer-events: none;
}

.help-card:hover::before {
  opacity: 1;
}

.help-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.help-card:focus {
  outline: 2px solid #ff8c14;
  outline-offset: 2px;
}

/* Icon container */
.help-card-icon {
  margin-bottom: 1.25rem;
  color: #0066cc; /* آبی - مثل تصویر */
  font-size: 3.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 85px;
  height: 85px;
  position: relative;
  z-index: 1;
}

.help-card-icon i {
  color: #0066cc;
  font-size: 3.5rem !important;
}

/* دسکتاپ - آیکون بزرگتر (2-3 برابر) */
@media (min-width: 992px) {
  .help-card-icon {
    width: 100px;
    height: 100px;
  }

  .help-card-icon i {
    font-size: 5rem !important;
  }
}

/* Card title */
.help-card-title {
  font-size: 0.9rem;
  font-weight: 600;
  color: #111;
  margin: 0;
  line-height: 1.4;
  position: relative;
  z-index: 1;
}

/* Responsive tweaks */
@media (max-width: 991px) {
  .help-card-wrapper {
    width: calc(33.333% - 0.75rem);
    max-width: 200px;
  }
}

@media (max-width: 768px) {
  .help-card {
    padding: 1rem 0.5rem;
  }

  .help-card-icon {
    font-size: 2rem;
    width: 50px;
    height: 50px;
    margin-bottom: 0.5rem;
  }

  .help-card-title {
    font-size: 0.7rem;
    line-height: 1.3;
  }

  .help-card-mobile {
    width: 100%;
    min-width: 0;
  }
}

@media (max-width: 576px) {
  .help-card {
    padding: 0.75rem 0.25rem;
  }

  .help-card-icon {
    font-size: 1.75rem;
    width: 45px;
    height: 45px;
    margin-bottom: 0.5rem;
  }

  .help-card-icon i {
    font-size: 1.75rem !important;
  }

  .help-card-title {
    font-size: 0.65rem;
    line-height: 1.2;
  }

  .help-card-mobile {
    width: 100%;
    min-width: 0;
  }

  .help-section {
    padding-top: 2rem;
    padding-bottom: 2rem;
  }

  .cards-container-mobile {
    padding: 0;
    margin: 0;
  }

  .cards-grid-wrapper {
    gap: 0.4rem;
  }
}
</style>
