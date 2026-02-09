<template>
  <template v-if="Object.keys(data).length > 0">
    <div class="container">
      <div class="row justify-content-between align-items-center">
        <div class="col-12 col-md-3 mb-3 mb-md-0">
          <label class="form-label">{{ data.title }}:</label>
        </div>
        <div class="col-12 col-md-6">
          <div class="d-flex flex-wrap gap-2">
            <div v-for="(value, index) in data.values" :key="index" class="form-check flex-grow-1">
              <label
                class="form-check-label w-100 d-flex align-items-center justify-content-center position-relative"
                :for="'radio-' + data.slug + '-' + index"
              >
                <input
                  class="form-check-input"
                  type="radio"
                  :name="data.slug"
                  :id="'radio-' + data.slug + '-' + index"
                  :value="value"
                  v-model="inputValue"
                />
                <span class="dot"></span>
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
    default: () => ({}),
  },
  modelValue: {
    type: String,
    required: true,
  },
});

const inputValue = ref(props.modelValue);

// واکنش به تغییرات modelValue و تنظیم مقدار اولیه
watch(
  () => props.modelValue,
  (newValue) => {
    inputValue.value = newValue;
  },
  { immediate: true } // مقدار اولیه را هم تنظیم می‌کند
);

// ارسال مقدار انتخاب‌شده به والد
watch(inputValue, (newValue) => {
  emit("update:modelValue", newValue);
});
</script>

<style scoped>
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

.form-check-input:checked ~ .form-check {
  background-color: rgba(220, 53, 69, 1) !important;
  border-color: rgba(220, 53, 69, 1) !important;
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
