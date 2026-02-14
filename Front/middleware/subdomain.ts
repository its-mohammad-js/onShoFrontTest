export default defineNuxtRouteMiddleware(async (to, from) => {
  // فقط در client-side اجرا می‌شود (چون SSR: false)
  if (process.server) return

  // اگر در صفحه company هستیم و slug داریم، نیازی به چک مجدد نیست
  if (to.path.startsWith('/company/') && to.params.slug) {
    return
  }

  // اگر در صفحه 404 هستیم، دوباره چک نکن
  if (to.path.startsWith('/error/404')) {
    return
  }

  // استخراج subdomain از host
  const host = window.location.hostname
  const subdomainMatch = host.match(/^([a-z0-9-]+)\.onsho24\.ir$/)
  
  if (!subdomainMatch) {
    // Main domain است، نیازی به چک کردن نیست
    return
  }

  const subdomain = subdomainMatch[1]
  
  // چک کردن که آیا این subdomain معتبر است یا نه
  const { $api } = useNuxtApp()
  
  try {
    // درخواست به API برای چک کردن subdomain
    const response = await $api.post('/course/organization/check-domain', {
      subdomain: subdomain  // API از subdomain استفاده می‌کند
    })
    
    console.log('Subdomain check response:', response.data)
    
    if (response.data.status && response.data.data) {
      // بررسی ساختار پاسخ API
      if (response.data.data.available === false && response.data.data.organizer_id) {
        // subdomain اشغال است، organizer وجود دارد
        // اگر slug مستقیماً در پاسخ وجود دارد، از آن استفاده کن
        if (response.data.data.slug) {
          const targetPath = `/company/${response.data.data.slug}`
          console.log('Redirecting to:', targetPath)
          // Domain معتبر است، به صفحه سازمان redirect کن
          // استفاده از navigateTo برای حفظ subdomain (بدون external)
          if (to.path !== targetPath) {
            return navigateTo(targetPath, { external: false })
          }
          return
        }
        
        // اگر slug در پاسخ نیست، از API list استفاده می‌کنیم (fallback)
        console.log('Slug not found in response, trying fallback API...')
        const listResponse = await $api.post('/course/organization/list', {})
        
        if (listResponse.data.status && listResponse.data.data.data) {
          const organizer = listResponse.data.data.data.find(
            (org) => org.id === response.data.data.organizer_id
          )
          
          if (organizer && organizer.slug) {
            const targetPath = `/company/${organizer.slug}`
            console.log('Found organizer in list, redirecting to:', targetPath)
            // Domain معتبر است، به صفحه سازمان redirect کن
            // استفاده از navigateTo برای حفظ subdomain (بدون external)
            if (to.path !== targetPath) {
              return navigateTo(targetPath, { external: false })
            }
            return
          }
        }
        
        console.error('Organizer not found even though available=false and organizer_id exists')
      }
      
      // اگر organizer پیدا نشد یا subdomain در دسترس است
      console.error('Subdomain check failed - available:', response.data.data.available)
      // به جای throw error، به صفحه 404 برو (بدون ریدایرکت به main domain)
      return navigateTo('/error/404', { external: false })
    } else {
      // Domain معتبر نیست، 404 نمایش بده
      console.error('Invalid API response structure:', response.data)
      // به جای throw error، به صفحه 404 برو (بدون ریدایرکت به main domain)
      return navigateTo('/error/404', { external: false })
    }
  } catch (error: any) {
    // اگر خطا رخ داد (404 یا خطای دیگر)
    if (error.statusCode === 404) {
      console.error('404 error thrown:', error)
      // به جای throw error، به صفحه 404 برو (بدون ریدایرکت به main domain)
      return navigateTo('/error/404', { external: false })
    }
    
    // خطای دیگر - نمایش 404
    console.error('Unexpected error in subdomain check:', error)
    // به جای throw error، به صفحه 404 برو (بدون ریدایرکت به main domain)
    return navigateTo('/error/404', { external: false })
  }
})

