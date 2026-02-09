<template>
    <div>
        <div class="row my-4">
          <div class="col-md-12 mb-3">
            <label for="photo" class="form-label">انتخاب عکس:</label>
            <template v-if="previewImage">
              <div class="position-relative w-200-px h-150-px">
                <img
                  :src="previewImage"
                  alt="پیش نمایش عکس"
                  class="img-thumbnail w-200-px h-150-px border-dashed border-dark"
                />
                <button
                  type="button"
                  class="btn btn-danger remove-btn"
                  @click="removePhoto"
                >
                  <i class="icon icon-regular-times font-size-14 mt-1"></i>
                </button>
              </div>
            </template>
            <template v-else>
              <div
                class="photo-box d-flex align-items-center justify-content-center"
                @click="triggerFileInput"
              >
                <i class="icon icon-regular-plus fs-1"></i>
              </div>
              <input
                id="photo"
                type="file"
                class="d-none"
                @change="handleFileUpload"
              />
            </template>
          </div>
        </div>
        <div class="row my-4">
          <div class="col-md-12 mb-3">
            <label for="courseName" class="form-label">نام دوره آموزشی:</label>
            <input
              type="text"
              id="courseName"
              v-model="data.title"
              class="form-control py-3 shadow-none"
              placeholder="عنوان دوره را وارد کنید"
            />
          </div>
        </div>
        <div class="row my-4">
          <div class="col-md-12 mb-3">
            <label for="courseDescription" class="form-label">توضیحات دوره آموزشی:</label>
            <textarea
              id="courseDescription"
              v-model="data.description"
              class="form-control py-3 shadow-none"
              rows="5"
              placeholder="توضیحات دوره را وارد کنید"
            ></textarea>
          </div>
          <div class="col-md-12 mb-3">
            <label for="courseExcerpt" class="form-label">دید کلی دوره:</label>
            <textarea
              id="courseExcerpt"
              v-model="data.excerpt"
              class="form-control py-3 shadow-none"
              rows="5"
              placeholder="دید کلی دوره را وارد کنید"
            ></textarea>
          </div>
        </div>
      </div>
</template>

<script setup>
import { ref, watch, onMounted } from "vue";
import { useAuthStore } from "~/stores/auth";

const auth = useAuthStore();
const props = defineProps({
  modelValue: {
    type: Object,
    required: true,
  },
});
const emit = defineEmits(["update:modelValue"]);

const data = ref(props.modelValue);
const previewImage = ref(null);

const handleFileUpload = (event) => {
  const file = event.target.files[0];
  if (file) {
    data.value.photo = file;
    previewImage.value = URL.createObjectURL(file);
  }
};

const removePhoto = () => {
  data.value.photo = null;
  previewImage.value = null;
};

const triggerFileInput = () => {
  document.getElementById("photo").click();
};
onMounted(() => {
  // Set initial image if available
  if (props.modelValue.course?.image) {
    data.value.photo = props.modelValue.course.image;
    previewImage.value = props.modelValue.course.image;
  }
});

// Watch for changes in the course data
watch(() => props.modelValue.course, (newCourse) => {
  if (newCourse?.image && !data.value.photo) {
    data.value.photo = newCourse.image;
    previewImage.value = newCourse.image;
  }
}, { deep: true });

watch(data, (newValue) => {
  emit("update:modelValue", newValue);
});
</script>


<style scoped>
.img-thumbnail {
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  position: relative;
}
.photo-box {
  width: 200px;
  height: 150px;
  border: 2px dashed rgba(220, 53, 69, 0.8);
  border-radius: 8px;
  cursor: pointer;
  color: rgba(220, 53, 69, 0.8);
  transition: background-color 0.3s, color 0.3s;
}

.photo-box:hover {
  background-color: #f8f9fa;
  color: rgba(220, 53, 69, 0.8);
}

.photo-box-plus {
  font-size: 24px;
  font-weight: bold;
}

.remove-btn {
  position: absolute;
  top: 10px;
  left: 10px;
  background-color: rgba(220, 53, 69, 0.8);
  border: none;
  border-radius: 50%;
  color: #fff;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  cursor: pointer;
}

.remove-btn:hover {
  background-color: rgba(220, 53, 69, 1);
}
</style>
