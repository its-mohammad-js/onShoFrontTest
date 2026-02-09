export default defineEventHandler(async (event) => {
  // Handle OPTIONS request for CORS preflight
  if (event.node.req.method === 'OPTIONS') {
    setHeader(event, 'Access-Control-Allow-Origin', '*')
    setHeader(event, 'Access-Control-Allow-Methods', 'GET, HEAD, OPTIONS')
    setHeader(event, 'Access-Control-Allow-Headers', 'Range, Content-Type')
    setHeader(event, 'Access-Control-Max-Age', '86400')
    return ''
  }

  const query = getQuery(event)
  const videoUrl = query.url as string

  if (!videoUrl) {
    throw createError({
      statusCode: 400,
      statusMessage: 'Video URL is required'
    })
  }

  // Validate URL
  try {
    new URL(videoUrl)
  } catch {
    throw createError({
      statusCode: 400,
      statusMessage: 'Invalid video URL'
    })
  }

  try {
    // دریافت Range header از request
    const rangeHeader = getHeader(event, 'range') || ''
    
    // دریافت ویدیو از URL اصلی
    const fetchOptions: RequestInit = {
      method: 'GET',
      headers: {} as HeadersInit
    }

    // اگر Range header وجود دارد، آن را ارسال کن
    if (rangeHeader) {
      fetchOptions.headers = {
        'Range': rangeHeader
      }
    }

    const response = await fetch(videoUrl, fetchOptions)

    if (!response.ok && response.status !== 206) {
      throw createError({
        statusCode: response.status,
        statusMessage: 'Failed to fetch video'
      })
    }

    // تنظیم CORS headers
    setHeader(event, 'Access-Control-Allow-Origin', '*')
    setHeader(event, 'Access-Control-Allow-Methods', 'GET, HEAD, OPTIONS')
    setHeader(event, 'Access-Control-Allow-Headers', 'Range, Content-Type')
    setHeader(event, 'Access-Control-Expose-Headers', 'Content-Range, Content-Length, Accept-Ranges')
    setHeader(event, 'Accept-Ranges', 'bytes')

    // کپی کردن headers از response اصلی
    const contentType = response.headers.get('content-type')
    if (contentType) {
      setHeader(event, 'Content-Type', contentType)
    } else {
      // اگر Content-Type وجود ندارد، بر اساس extension حدس بزن
      const urlObj = new URL(videoUrl)
      const pathname = urlObj.pathname.toLowerCase()
      if (pathname.endsWith('.mp4')) {
        setHeader(event, 'Content-Type', 'video/mp4')
      } else if (pathname.endsWith('.webm')) {
        setHeader(event, 'Content-Type', 'video/webm')
      } else if (pathname.endsWith('.ogg')) {
        setHeader(event, 'Content-Type', 'video/ogg')
      }
    }

    const contentLength = response.headers.get('content-length')
    if (contentLength) {
      setHeader(event, 'Content-Length', contentLength)
    }

    const contentRange = response.headers.get('content-range')
    if (contentRange) {
      setHeader(event, 'Content-Range', contentRange)
      setResponseStatus(event, 206) // Partial Content
    } else if (response.status === 206) {
      setResponseStatus(event, 206)
    }

    // برای streaming، response body را مستقیماً برگردانیم
    // H3/Nitro به صورت خودکار ReadableStream را handle می‌کند
    if (response.body) {
      // تبدیل Web ReadableStream به Node.js Readable
      const { Readable } = await import('stream')
      const nodeStream = Readable.fromWeb(response.body as any)
      return nodeStream
    }
    
    // Fallback: اگر body وجود ندارد
    throw createError({
      statusCode: 500,
      statusMessage: 'Video stream not available'
    })
  } catch (error: any) {
    console.error('Error proxying video:', error)
    throw createError({
      statusCode: error.statusCode || 500,
      statusMessage: error.message || 'Error proxying video'
    })
  }
})

