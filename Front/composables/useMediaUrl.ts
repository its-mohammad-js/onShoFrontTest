export const useMediaUrl = () => {
  const getMediaUrl = (url: string | null | undefined): string => {
    if (!url) return ''
    
    if (!url.trim()) return url
    
    if (url.startsWith('http://') || url.startsWith('https://')) {
      try {
        const urlObj = new URL(url)
        const pathname = urlObj.pathname
        
        if (pathname.startsWith('/media/')) {
          if (!pathname.startsWith('/api/')) {
            return urlObj.origin + '/api' + pathname
          }
          return url
        }
        
        return url
      } catch (e) {
        return url
      }
    }
    
    if (url.startsWith('/media/')) {
      if (!url.startsWith('/api/')) {
        return '/api' + url
      }
      return url
    }
    
    return url
  }
  
  const getVideoUrl = (url: string | null | undefined): string => {
    if (!url) return ''
    
    if (!url.trim()) return url
    
    // اگر URL از همان origin است یا از /media/ شروع می‌شود، از proxy استفاده کن
    if (url.startsWith('http://') || url.startsWith('https://')) {
      try {
        const urlObj = new URL(url)
        const pathname = urlObj.pathname
        const hostname = urlObj.hostname.toLowerCase()
        
        // اگر از /media/ شروع می‌شود، از proxy API استفاده کن
        if (pathname.startsWith('/media/')) {
          if (!pathname.startsWith('/api/')) {
            return urlObj.origin + '/api' + pathname
          }
          return url
        }
        
        // برای ویدیوهای Aparat، از embed API استفاده کن
        if (hostname.includes('aparat.com')) {
          // استخراج video ID از URL
          const videoIdMatch = url.match(/\/v\/([a-zA-Z0-9]+)/)
          if (videoIdMatch && videoIdMatch[1]) {
            // برگرداندن embed URL برای Aparat
            return `https://www.aparat.com/video/video/embed/videohash/${videoIdMatch[1]}/vt/frame`
          }
        }
        
        // اگر از origin دیگری است، از video proxy استفاده کن
        if (typeof window !== 'undefined') {
          const currentOrigin = window.location.origin
          
          // اگر URL از همان origin است، همان را برگردان
          if (urlObj.origin === currentOrigin) {
            return url
          }
          
          // برای ویدیوهای خارجی دیگر، از video proxy استفاده کن
          return `/api/video-proxy?url=${encodeURIComponent(url)}`
        }
        
        // در غیر این صورت (SSR)، همان URL را برگردان
        return url
      } catch (e) {
        return url
      }
    }
    
    // اگر از /media/ شروع می‌شود، از proxy استفاده کن
    if (url.startsWith('/media/')) {
      if (!url.startsWith('/api/')) {
        return '/api' + url
      }
      return url
    }
    
    return url
  }
  
  // بررسی اینکه آیا URL یک embed URL است (مثل Aparat)
  const isEmbedUrl = (url: string | null | undefined): boolean => {
    if (!url) return false
    try {
      const urlObj = new URL(url)
      return urlObj.hostname.includes('aparat.com') && urlObj.pathname.includes('/embed/')
    } catch {
      return false
    }
  }
  
  return {
    getMediaUrl,
    getVideoUrl,
    isEmbedUrl
  }
}

