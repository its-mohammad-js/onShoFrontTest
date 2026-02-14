<template>
  <div>
    <!-- Header Section -->
    <section class="bg-light py-5">
      <div class="container">
        <div class="text-center">
          <h1 class="display-4 fw-bold mb-3">{{ pageData.title }}</h1>
          <p class="lead text-muted content-text" v-html="processedShortDescription"></p>
        </div>
      </div>
    </section>

    <!-- Main Content Section -->
    <section class="py-5">
      <div class="container">
        <div class="row justify-content-center">
          <div class="col-lg-8">
            <div class="content-body">
              <div class="mb-4">
                <div class="text-muted lh-lg content-text" v-html="processedDescription"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Related Links Section -->
    <section class="bg-light py-5">
      <div class="container">
        <div class="row">
          <div class="col-12">
            <h3 class="fw-bold mb-4 text-center">لینک‌های مرتبط</h3>
            <div class="row g-4">
              <div 
                v-for="(link, index) in pageData.relatedLinks" 
                :key="index"
                class="col-md-6 col-lg-4"
              >
                <div class="card border-0 shadow-sm h-100">
                  <div class="card-body d-flex flex-column">
                    <h5 class="card-title fw-bold mb-3">{{ link.title }}</h5>
                    <p class="card-text text-muted flex-grow-1">{{ link.description }}</p>
                     <nuxt-link
                       v-if="link.to"
                       :to="link.to"
                       class="btn btn-danger mt-auto"
                     >
                       مشاهده بیشتر
                       <i class="fa-solid fa-arrow-left me-2"></i>
                     </nuxt-link>
                     <a
                       v-else
                       :href="link.url"
                       class="btn btn-danger mt-auto"
                       :target="link.external ? '_blank' : '_self'"
                     >
                       مشاهده بیشتر
                       <i class="fa-solid fa-arrow-left me-2"></i>
                     </a>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
 import { ref, onMounted, watch, computed } from 'vue';
 import { useRoute, useRouter } from 'vue-router';
 
 const route = useRoute();
 const router = useRouter();

 // Function to normalize multiple consecutive line breaks to single line break
 const normalizeLineBreaks = (text) => {
   if (!text) return '';
   
   // Check if content is HTML (contains HTML tags)
   const isHTML = /<[^>]+>/.test(text);
   
   if (isHTML) {
     // For HTML content, normalize multiple consecutive <br> tags to single <br>
     // Also normalize line breaks in text nodes
     return text
       .replace(/(<br\s*\/?>)\s*(<br\s*\/?>)+/gi, '<br>') // Multiple consecutive <br> to single <br>
       .replace(/\r\n\r\n+/g, '\n') // Multiple \r\n to single \n
       .replace(/\n\n+/g, '\n') // Multiple \n to single \n
       .replace(/\r\r+/g, '\n'); // Multiple \r to single \n
   } else {
     // For plain text, normalize line breaks
     return text
       .replace(/\r\n\r\n+/g, '\n') // Multiple \r\n to single \n
       .replace(/\n\n+/g, '\n') // Multiple \n to single \n
       .replace(/\r\r+/g, '\n') // Multiple \r to single \n
       .replace(/\r\n/g, '<br>')
       .replace(/\n/g, '<br>')
       .replace(/\r/g, '<br>');
   }
 };

const pageData = ref({
   title: '',
   shortDescription: '',
   description: '',
   relatedLinks: []
});

// Computed properties for processed content
const processedShortDescription = computed(() => {
  return normalizeLineBreaks(pageData.value.shortDescription);
});

const processedDescription = computed(() => {
  return normalizeLineBreaks(pageData.value.description);
});

 const currentId = ref(route.query.id ? String(route.query.id) : null);
 
 // Helper function to generate slug from title
 const generateSlug = (title) => {
   if (!title) return '';
   return title
     .toLowerCase()
     .replace(/[^\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFFa-z0-9]+/g, '-')
     .replace(/^-+|-+$/g, '');
 };

 // Helper function to get slug from data
 const getSlug = (data) => {
   return data?.slug || generateSlug(data?.title) || String(data?.id || '');
 };

  const loadAll = async () => {
    if (!currentId.value) {
      // If no id, redirect to home or show error
      router.push('/');
      return;
    }

    const { $api } = useNuxtApp();

    try {
      const res = await $api.get(`/static-content/detail?id=${currentId.value}`);
      const data = res?.data?.data ?? res?.data ?? res;

      // Get slug from the data
      const slug = getSlug(data);
      
      // Redirect to slug-based URL
      if (slug) {
        router.replace(`/content/${slug}`);
        return;
      }

      // Set main page data (fallback if redirect doesn't happen)
      pageData.value.title = data?.title ?? '';
      pageData.value.shortDescription = data?.short_description ?? data?.shortDescription ?? '';
      pageData.value.description = data?.description ?? '';

      // Read related links from detail API response
      pageData.value.relatedLinks = (Array.isArray(data?.related_links) ? data.related_links : []).map(link => {
        const linkSlug = getSlug(link);
        return {
          title: link.title ?? 'بدون عنوان',
          description: link.description ?? '',
          to: link.external ? link.url : `/content/${linkSlug}`,
          external: !!link.external
        };
      });

    } catch (e) {
      console.error('Error loading detail:', e);
      pageData.value.relatedLinks = [];
    }
  };
//  const loadDetail = async () => {
//    const { $api } = useNuxtApp();
//    try {
//      const res = await $api.get(`/static-content/detail?id=${currentId.value}`);
//      const data = res?.data?.data ?? res?.data ?? res;
//      pageData.value.title = data?.title ?? '';
//      pageData.value.shortDescription = data?.short_description ?? data?.shortDescription ?? '';
//      pageData.value.description = data?.description ?? '';
//    } catch (e) {
//      console.error('Error loading detail:', e);
//    }
//  };
 
//  const loadRelatedLinks = async () => {
//    const { $api } = useNuxtApp();
//    try {
//      const res = await $api.get('/static-content/list');
//      const list = res?.data?.data ?? res?.data ?? res ?? [];
//      pageData.value.relatedLinks = (Array.isArray(list) ? list : []).filter(item => String(item.id) !== currentId.value).map(item => ({
//        title: item.title ?? 'بدون عنوان',
//        description: item.short_description ?? '',
//        to: `/content?id=${item.id}`
//      }));
//    } catch (e) {
//      console.error('Error loading related links:', e);
//      pageData.value.relatedLinks = [];
//    }
//  };
 
//  const loadAll = async () => {
//    await Promise.all([loadDetail(), loadRelatedLinks()]);
//  };
 
 onMounted(loadAll);
 
 watch(() => route.query.id, (newId) => {
   const id = newId ? String(newId) : '1';
   if (id !== currentId.value) {
     currentId.value = id;
     loadAll();
   }
 });
</script>

<style scoped>
.content-body {
  direction: rtl;
  text-align: right;
}

.card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15) !important;
}

.btn-danger {
  background-color: #dc3545;
  border-color: #dc3545;
}

.btn-danger:hover {
  background-color: #bb2d3b;
  border-color: #b02a37;
}

/* Mobile spacing adjustments */
@media (max-width: 768px) {
  .container {
    padding-left: 20px;
    padding-right: 20px;
  }
  
  .content-body {
    padding-left: 0;
    padding-right: 0;
  }
  
  .content-text {
    padding-left: 12px;
    padding-right: 12px;
  }
  
  .lead.content-text {
    padding-left: 16px;
    padding-right: 16px;
  }
}
</style>

