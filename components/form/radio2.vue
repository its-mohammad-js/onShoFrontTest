<template>
  <template v-if="Object.keys(data).length > 0">
    <div class="container">
      <div class="row justify-content-between align-items-center">
        <div class="col-12 col-md-3 mb-3 mb-md-0">
          <label class="form-label">{{ data.title }}:</label>
        </div>
        <div class="col-12 col-md-6">
          <div class="d-flex flex-wrap justify-content-between">
            <div
              v-for="(value, index) in data.values"
              :key="index"
              class="form-check p-0 w-49"
            >
              <label
                class="form-check-label w-100 d-flex align-items-center justify-content-center position-relative"
                :for="'radio-' + data.slug + '-' + index"
                :class="{ active: inputValue === value }"
              >
                <input
                  class="form-check-input"
                  type="radio"
                  :name="data.slug"
                  :id="'radio-' + data.slug + '-' + index"
                  :value="value"
                  v-model="inputValue"
                />
                <span class="label-text">{{ value }}</span>
              </label>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
</template>

<script setup>
import { ref, watch } from "vue";

const emit = defineEmits(["update:modelValue"]);
const props = defineProps({
  data: {
    type: Object,
    default: {},
  },
  modelValue: {
    type: String,
    required: true,
  },
});

const inputValue = ref(props.modelValue);

// مشاهده تغییرات در props.modelValue و تنظیم مقدار inputValue
watch(
  () => props.modelValue,
  (newValue) => {
    inputValue.value = newValue;
  },
  { immediate: true } // مقدار اولیه را هم تنظیم می‌کند
);

// ارسال مقدار به والد هنگام تغییر
watch(inputValue, (newValue) => {
  emit("update:modelValue", newValue);
});
</script>
<style scoped>
.form-check {
  border: 1px solid rgba(220, 220, 220, 1);
  border-radius: 12px;
  background-color: #fff;
  position: relative;
  transition: all 0.3s ease;
  padding: 10px 20px;
  text-align: center;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.w-49 {
  width: 49%;
}

.form-check-input {
  display: none;
}

.form-check-label {
  color: #000;
  font-weight: bold;
  padding: 10px 20px;
  border-radius: 12px;
  transition: background-color 0.3s ease, color 0.3s ease;
}

.form-check-label.active {
  background-color: rgba(220, 53, 69, 1) !important;
  color: #fff !important;
  border-color: rgba(220, 53, 69, 1) !important;
}

.form-check:hover .form-check-label {
  background-color: rgba(220, 53, 69, 0.1);
}

.label-text {
  font-size: 16px;
}

@media (max-width: 768px) {
  .form-check {
    padding: 8px 15px;
  }
  .label-text {
    font-size: 14px;
  }
}
</style>
