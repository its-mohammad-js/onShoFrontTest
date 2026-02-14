<template>
  <div class="container mt-5">
    <h1>API Test Page</h1>
    <div class="row">
      <div class="col-12">
        <button @click="testAPI" class="btn btn-primary mb-3">Test API Connection</button>
        
        <div v-if="loading" class="alert alert-info">
          <i class="fas fa-spinner fa-spin"></i> Testing API connection...
        </div>
        
        <div v-if="error" class="alert alert-danger">
          <strong>Error:</strong> {{ error }}
        </div>
        
        <div v-if="success" class="alert alert-success">
          <strong>Success!</strong> API is working correctly.
        </div>
        
        <div v-if="courseData" class="mt-4">
          <h3>Course Data:</h3>
          <div class="card">
            <div class="card-body">
              <h5 class="card-title">{{ courseData.title }}</h5>
              <p class="card-text">{{ courseData.excerpt }}</p>
              
              <h6>Attributes:</h6>
              <ul class="list-group list-group-flush">
                <li v-for="attr in courseData.attributes" :key="attr.id" class="list-group-item">
                  <strong>{{ attr.title }}:</strong> {{ attr.value }}
                  <small class="text-muted">(slug: {{ attr.slug }})</small>
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
import { ref } from 'vue'

const loading = ref(false)
const error = ref('')
const success = ref(false)
const courseData = ref(null)
const { $api } = useNuxtApp()

const testAPI = async () => {
  loading.value = true
  error.value = ''
  success.value = false
  courseData.value = null
  
  try {
    console.log('🔍 Testing API connection...')
    
    const response = await $api.post('/course/list', {
      search: '',
      category_id: null,
      organizer_id: null,
      min_price: null,
      max_price: null,
      ordering: '-create_date'
    })
    
    console.log('📡 API Response:', response.data)
    
    if (response.data.status && response.data.data.data.length > 0) {
      success.value = true
      courseData.value = response.data.data.data[0]
      console.log('✅ API test successful!')
    } else {
      error.value = 'No courses found in response'
    }
  } catch (err) {
    error.value = err.message || 'Unknown error occurred'
    console.error('❌ API test failed:', err)
  } finally {
    loading.value = false
  }
}
</script>
