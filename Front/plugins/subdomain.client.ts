export default defineNuxtPlugin(() => {
  // فقط در client-side اجرا می‌شود
  if (process.server) return

  const route = useRoute()
  const router = useRouter()
  
  // استخراج subdomain از host
  const host = window.location.hostname
  const subdomainMatch = host.match(/^([a-z0-9-]+)\.onsho24\.ir$/)
  
  if (!subdomainMatch) {
    // Main domain است، نیازی به چک کردن نیست
    return
  }

  const subdomain = subdomainMatch[1]
  
  // Router guard: اگر از subdomain به صفحاتی غیر از company می‌رود، URL را به main domain تغییر بده
  router.beforeEach((to, from) => {
    // اگر در subdomain هستیم
    if (subdomainMatch) {
      // اگر به صفحه company می‌رود، اجازه بده subdomain بماند
      if (to.path.startsWith('/company/') && to.params.slug) {
        return true // اجازه navigation، subdomain بماند
      }
      
      // اگر به صفحات دیگر می‌رود (از company خارج می‌شود یا از ابتدا در صفحه دیگری است)، URL را به main domain تغییر بده
      const mainDomain = 'onsho24.ir'
      const protocol = window.location.protocol
      const newUrl = `${protocol}//${mainDomain}${to.fullPath}`
      
      // استفاده از window.location برای تغییر کامل URL
      window.location.href = newUrl
      return false // جلوگیری از navigation معمولی
    }
    
    return true
  })
  
  // اگر در صفحه 404 هستیم، دوباره چک نکن
  if (route.path.startsWith('/error/404')) {
    return
  }

  // اگر قبلاً در صفحه company هستیم و slug داریم، نیازی به چک مجدد نیست
  if (route.path.startsWith('/company/') && route.params.slug) {
    return
  }

  // چک کردن که آیا این subdomain معتبر است یا نه
  // استفاده از relative path برای API که با HTTPS کار می‌کند
  // nginx مسیر /api/ را به backend proxy می‌کند
  const apiUrl = '/api/course/organization/check-domain'
  
  // استفاده از fetch با relative URL که با HTTPS کار می‌کند
  // این روش mixed content error نمی‌دهد
  fetch(apiUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      subdomain: subdomain  // API از subdomain استفاده می‌کند نه domain
    }),
    credentials: 'same-origin' // برای ارسال cookies اگر نیاز باشد
  })
    .then(async (response) => {
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      const result = await response.json()
      
      // بررسی ساختار پاسخ API
      if (result.status && result.data) {
        // اگر subdomain اشغال است (available: false)، organizer وجود دارد
        if (result.data.available === false && result.data.organizer_id) {
          // اگر slug مستقیماً در پاسخ وجود دارد، از آن استفاده کن
          if (result.data.slug) {
            // اگر در صفحه اصلی یا صفحه دیگری هستیم (نه company)، به آن navigate کن
            // URL همچنان subdomain.onsho24.ir خواهد ماند
            if (!route.path.startsWith('/company/')) {
              router.push(`/company/${result.data.slug}`)
            }
            return
          }
          
          // اگر slug در پاسخ نیست، از API list استفاده می‌کنیم (fallback)
          const { $api } = useNuxtApp()
          
          try {
            const listResponse = await $api.post('/course/organization/list', {})
            
            if (listResponse.data.status && listResponse.data.data.data) {
              // پیدا کردن organizer با ID
              const organizer = listResponse.data.data.data.find(
                (org: any) => org.id === result.data.organizer_id
              )
              
              if (organizer && organizer.slug) {
                // اگر در صفحه اصلی یا صفحه دیگری هستیم (نه company)، به آن navigate کن
                // URL همچنان subdomain.onsho24.ir خواهد ماند
                if (!route.path.startsWith('/company/')) {
                  router.push(`/company/${organizer.slug}`)
                }
                return
              }
            }
          } catch (listError) {
            console.error('Error fetching organizer list:', listError)
          }
          
          // اگر نتوانستیم organizer را پیدا کنیم، 404 نمایش بده
          if (route.path !== '/error/404') {
            router.replace('/error/404?reason=domain_not_found')
          }
        } else if (result.data.available === true) {
          // subdomain در دسترس است اما organizer ندارد
          // این یعنی subdomain ثبت نشده است
          if (route.path !== '/error/404') {
            router.replace('/error/404?reason=domain_not_found')
          }
        } else {
          // ساختار پاسخ غیرمنتظره
          console.warn('Unexpected API response structure:', result)
          if (route.path !== '/error/404') {
            router.replace('/error/404?reason=domain_check_failed')
          }
        }
      } else {
        // پاسخ نامعتبر
        if (route.path !== '/error/404') {
          router.replace('/error/404?reason=domain_check_failed')
        }
      }
    })
    .catch((error: any) => {
      console.error('Error checking domain:', error)
      console.error('Subdomain:', subdomain)
      console.error('API URL:', apiUrl)
      console.error('Protocol:', window.location.protocol)
      console.error('Full error:', error.message || error)
      
      // در صورت خطا، 404 نمایش بده
      if (route.path !== '/error/404') {
        router.replace('/error/404?reason=domain_check_failed')
      }
    })
})

