export default defineNuxtRouteMiddleware(async (to, from) => {
  // فقط در client-side اجرا می‌شود (چون SSR: false)
  if (process.server) return

  // استخراج subdomain از host
  const host = window.location.hostname
  const subdomainMatch = host.match(/^([a-z0-9-]+)\.onsho24\.ir$/)
  
  if (!subdomainMatch) {
    // Main domain است، نیازی به چک کردن نیست
    return
  }

  // اگر در صفحه company هستیم و slug داریم، نیازی به چک مجدد نیست
  if (to.path.startsWith('/company/') && to.params.slug) {
    return
  }

  // اگر در صفحه 404 هستیم، دوباره چک نکن
  if (to.path.startsWith('/error/404')) {
    return
  }

  const subdomain = subdomainMatch[1]
  
  // چک کردن که آیا این subdomain معتبر است یا نه
  // استفاده از fetch با relative path برای اطمینان از HTTPS
  try {
    // استفاده از fetch با relative URL که با HTTPS کار می‌کند
    const apiUrl = '/api/course/organization/check-domain'
    
    const response = await fetch(apiUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        subdomain: subdomain
      }),
      credentials: 'same-origin'
    })
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    const result = await response.json()
    
    // تبدیل به فرمت axios response برای سازگاری
    const responseData = {
      data: result
    }
    
    console.log('Subdomain check response:', responseData.data)
    
    if (responseData.data.status && responseData.data.data) {
      // بررسی ساختار پاسخ API
      if (responseData.data.data.available === false && responseData.data.data.organizer_id) {
        // subdomain اشغال است، organizer وجود دارد
        // اگر slug مستقیماً در پاسخ وجود دارد، از آن استفاده کن
        if (responseData.data.data.slug) {
          const targetPath = `/company/${responseData.data.data.slug}`
          console.log('Redirecting to:', targetPath, 'Current path:', to.path)
          // Domain معتبر است، به صفحه سازمان redirect کن
          // استفاده از navigateTo با external: false برای حفظ subdomain
          if (to.path !== targetPath) {
            // navigateTo با relative path subdomain را حفظ می‌کند
            return navigateTo(targetPath, { external: false })
          }
          return
        }
        
        // اگر slug در پاسخ نیست، از API list استفاده می‌کنیم (fallback)
        console.log('Slug not found in response, trying fallback API...')
        const listResponse = await fetch('/api/course/organization/list', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          credentials: 'same-origin'
        })
        
        if (listResponse.ok) {
          const listResult = await listResponse.json()
          if (listResult.status && listResult.data.data) {
            const organizer = listResult.data.data.find(
              (org: any) => org.id === responseData.data.data.organizer_id
            )
            
            if (organizer && organizer.slug) {
              const targetPath = `/company/${organizer.slug}`
              console.log('Found organizer in list, redirecting to:', targetPath, 'Current path:', to.path)
              // Domain معتبر است، به صفحه سازمان redirect کن
              // استفاده از navigateTo با external: false برای حفظ subdomain
              if (to.path !== targetPath) {
                // navigateTo با relative path subdomain را حفظ می‌کند
                return navigateTo(targetPath, { external: false })
              }
              return
            }
          }
        }
        
        console.error('Organizer not found even though available=false and organizer_id exists')
      }
      
      // اگر organizer پیدا نشد یا subdomain در دسترس است
      console.error('Subdomain check failed - available:', responseData.data.data.available)
      // به جای throw error، به صفحه 404 برو (بدون ریدایرکت به main domain)
      return navigateTo('/error/404', { external: false })
    } else {
      // Domain معتبر نیست، 404 نمایش بده
      console.error('Invalid API response structure:', responseData.data)
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

