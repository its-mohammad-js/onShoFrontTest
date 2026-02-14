<template>
  <div class="organization-logo-upload">
    <div class="position-relative d-inline-block">
      <img 
        :src="logoUrlWithApi" 
        :alt="altText"
        class="rounded-circle border border-3 border-primary"
        :style="imageStyle"
      />
      <button 
        @click="triggerFileInput"
        class="btn btn-sm btn-primary position-absolute bottom-0 end-0 rounded-circle upload-btn"
        :disabled="uploading"
      >
        <span v-if="uploading" class="spinner-border spinner-border-sm"></span>
        <i v-else class="icon icon-filled-camera text-white"></i>
      </button>
    </div>
    <input 
      ref="fileInput"
      type="file" 
      accept="image/*" 
      @change="handleFileSelect"
      class="d-none"
    />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

// Props
const props = defineProps({
  logoUrl: {
    type: String,
    default: ''
  },
  altText: {
    type: String,
    default: 'Organization Logo'
  },
  size: {
    type: String,
    default: '150px'
  },
  uploading: {
    type: Boolean,
    default: false
  }
})

// Emits
const emit = defineEmits(['file-selected', 'upload'])

// Refs
const fileInput = ref(null)
const { getMediaUrl } = useMediaUrl();

// Computed
const imageStyle = computed(() => ({
  width: props.size,
  height: props.size,
  objectFit: 'cover'
}))

// تبدیل آدرس logo به آدرس با /api
const logoUrlWithApi = computed(() => {
  const defaultUrl = '/images/user.png'
  const url = props.logoUrl || defaultUrl
  return getMediaUrl(url)
})

// Methods
const triggerFileInput = () => {
  fileInput.value?.click()
}

const handleFileSelect = (event) => {
  const file = event.target.files[0]
  if (file) {
    // Validate file type
    if (!file.type.startsWith('image/')) {
      alert('لطفاً یک فایل تصویری انتخاب کنید')
      return
    }
    
    // Validate file size (max 5MB)
    if (file.size > 5 * 1024 * 1024) {
      alert('حجم فایل نباید بیشتر از 5 مگابایت باشد')
      return
    }
    
    emit('file-selected', file)
  }
}
</script>

<style scoped>
.organization-logo-upload {
  display: inline-block;
}

.upload-btn {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.upload-btn:disabled {
  opacity: 0.6;
}

.border-primary {
  border-color: #FF8C14 !important;
}

.btn-primary {
  background-color: #FF8C14;
  border-color: #FF8C14;
}

.btn-primary:hover:not(:disabled) {
  background-color: #E67A0F;
  border-color: #D66A0A;
}

.icon {
  font-size: 1rem;
}
</style>
