# راهنمای تنظیم Google OAuth

این راهنما به شما کمک می‌کند تا Google OAuth را برای لاگین با گوگل در پروژه تنظیم کنید.

## مراحل دریافت Google OAuth Credentials

### 1. رفتن به Google Cloud Console

1. به [Google Cloud Console](https://console.cloud.google.com/) بروید
2. با حساب Google خود وارد شوید

### 2. ایجاد یا انتخاب پروژه

1. در بالای صفحه، از منوی پروژه، یک پروژه جدید ایجاد کنید یا پروژه موجود را انتخاب کنید
2. اگر پروژه جدید می‌سازید، نام مناسبی برای آن انتخاب کنید (مثلاً: `mahoverse-auth`)

### 3. فعال‌سازی Google+ API

1. به **APIs & Services** > **Library** بروید
2. در جستجو، "Google+ API" یا "Google Identity" را جستجو کنید
3. روی API کلیک کرده و **Enable** را بزنید

### 4. ایجاد OAuth Client ID

1. به **APIs & Services** > **Credentials** بروید
2. روی **+ CREATE CREDENTIALS** کلیک کنید
3. **OAuth client ID** را انتخاب کنید

### 5. تنظیمات OAuth Consent Screen

اگر قبلاً OAuth Consent Screen را تنظیم نکرده‌اید:
1. روی **CONFIGURE CONSENT SCREEN** کلیک کنید
2. **External** را انتخاب کنید (برای تست) یا **Internal** (برای سازمان‌های Google Workspace)
3. اطلاعات زیر را پر کنید:
   - **App name**: نام اپلیکیشن شما (مثلاً: Mahoverse)
   - **User support email**: ایمیل پشتیبانی
   - **Developer contact information**: ایمیل شما
4. روی **SAVE AND CONTINUE** کلیک کنید
5. در بخش **Scopes**، روی **SAVE AND CONTINUE** کلیک کنید
6. در بخش **Test users** (اگر External انتخاب کردید)، ایمیل‌های تست را اضافه کنید
7. روی **SAVE AND CONTINUE** کلیک کنید

### 6. ایجاد OAuth Client ID

1. به **Credentials** برگردید
2. روی **+ CREATE CREDENTIALS** > **OAuth client ID** کلیک کنید
3. **Application type** را **Web application** انتخاب کنید
4. **Name** را وارد کنید (مثلاً: `Mahoverse Web Client`)
5. **Authorized JavaScript origins** را اضافه کنید:
   - برای development: `http://localhost:3000`
   - برای production: `https://yourdomain.com`
6. **Authorized redirect URIs** را اضافه کنید:
   - برای development: 
     - `http://localhost:3000/auth/google/callback`
     - `http://127.0.0.1:3000/auth/google/callback` (اگر از IP استفاده می‌کنید)
   - برای production: 
     - `https://yourdomain.com/auth/google/callback`
     - `https://www.yourdomain.com/auth/google/callback` (اگر www استفاده می‌کنید)
   
   **⚠️ نکات مهم:**
   - URI ها باید دقیقاً مطابق باشند (حتی `/` در انتها مهم است)
   - باید `http://` یا `https://` داشته باشند
   - Port number مهم است (`:3000`)
   - نباید trailing slash اضافی داشته باشند
   
7. روی **CREATE** کلیک کنید

### 7. دریافت Client ID و Client Secret

بعد از ایجاد، یک پنجره باز می‌شود که شامل:
- **Client ID**: این را کپی کنید
- **Client Secret**: این را کپی کنید (مهم: این را محرمانه نگه دارید!)

## تنظیمات در پروژه

### 1. اضافه کردن Client ID به Environment Variables

یک فایل `.env` در ریشه پروژه ایجاد کنید (یا اگر وجود دارد، آن را ویرایش کنید):

```env
GOOGLE_CLIENT_ID=your-client-id-here.apps.googleusercontent.com
```

**نکته**: Client Secret فقط باید در backend استفاده شود، نه در frontend!

### 2. بررسی تنظیمات Backend

Backend شما باید این endpoint‌ها را داشته باشد:

#### `GET /auth/google/login`
این endpoint باید:
- دریافت `redirect_uri` از query parameter
- ساخت Google OAuth URL با استفاده از Client ID و Client Secret
- Redirect کردن کاربر به Google OAuth
- بعد از تأیید کاربر، Google کاربر را به `redirect_uri` با `code` و `state` برمی‌گرداند

**مثال کد (Laravel/PHP):**
```php
public function googleLogin(Request $request)
{
    $redirectUri = $request->query('redirect_uri');
    
    $googleClient = new \Google_Client();
    $googleClient->setClientId(config('services.google.client_id'));
    $googleClient->setClientSecret(config('services.google.client_secret'));
    $googleClient->setRedirectUri($redirectUri);
    $googleClient->addScope('email');
    $googleClient->addScope('profile');
    
    $authUrl = $googleClient->createAuthUrl();
    
    return redirect($authUrl);
}
```

#### `POST /auth/google/callback`
این endpoint باید:
- دریافت `code` و `state` از body
- تبادل `code` با Google برای دریافت access token
- دریافت اطلاعات کاربر از Google
- ایجاد یا یافتن کاربر در دیتابیس
- ایجاد JWT token برای کاربر
- بازگرداندن token در response

**مثال Response:**
```json
{
  "status": true,
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```

**مثال کد (Laravel/PHP):**
```php
public function googleCallback(Request $request)
{
    $code = $request->input('code');
    $redirectUri = $request->input('redirect_uri') ?? config('app.frontend_url') . '/auth/google/callback';
    
    $googleClient = new \Google_Client();
    $googleClient->setClientId(config('services.google.client_id'));
    $googleClient->setClientSecret(config('services.google.client_secret'));
    $googleClient->setRedirectUri($redirectUri);
    
    $token = $googleClient->fetchAccessTokenWithAuthCode($code);
    
    if (isset($token['error'])) {
        return response()->json([
            'status' => false,
            'message' => 'خطا در احراز هویت گوگل'
        ], 400);
    }
    
    $googleClient->setAccessToken($token);
    $oauth2 = new \Google_Service_Oauth2($googleClient);
    $userInfo = $oauth2->userinfo->get();
    
    // پیدا کردن یا ایجاد کاربر
    $user = User::firstOrCreate(
        ['email' => $userInfo->email],
        [
            'name' => $userInfo->name,
            'google_id' => $userInfo->id,
            'avatar' => $userInfo->picture,
        ]
    );
    
    // ایجاد JWT token
    $jwtToken = auth()->login($user);
    
    return response()->json([
        'status' => true,
        'data' => [
            'token' => $jwtToken
        ]
    ]);
}
```

## تست

1. مطمئن شوید که `.env` فایل را با `GOOGLE_CLIENT_ID` پر کرده‌اید
2. سرور development را اجرا کنید: `npm run dev`
3. به صفحه `/auth` بروید
4. روی دکمه "ورود با گوگل" کلیک کنید
5. باید به صفحه Google OAuth هدایت شوید
6. بعد از تأیید، به `/auth/google/callback` برمی‌گردید
7. در صورت موفقیت، به `/account` هدایت می‌شوید

## نکات امنیتی

1. **هرگز Client Secret را در frontend قرار ندهید!**
2. Client Secret فقط باید در backend استفاده شود
3. در production، از HTTPS استفاده کنید
4. Authorized redirect URIs را محدود کنید و فقط دامنه‌های مجاز را اضافه کنید
5. OAuth Consent Screen را به درستی تنظیم کنید

## عیب‌یابی

برای راهنمای کامل حل مشکلات، به [راهنمای عیب‌یابی Google OAuth](GOOGLE_OAUTH_TROUBLESHOOTING.md) مراجعه کنید.

### مشکل: "redirect_uri_mismatch"
- مطمئن شوید که redirect URI در Google Cloud Console دقیقاً با URL callback شما مطابقت دارد
- شامل `http://` یا `https://` باشد
- شامل trailing slash نباشد (مگر اینکه در URL شما باشد)
- Port number را در نظر بگیرید (`:3000`)

### مشکل: "invalid_client"
- مطمئن شوید که Client ID درست است
- مطمئن شوید که Client ID در Google Cloud Console فعال است

### مشکل: "access_denied"
- کاربر ممکن است دسترسی را رد کرده باشد
- یا OAuth Consent Screen به درستی تنظیم نشده باشد

## منابع

- [Google OAuth 2.0 Documentation](https://developers.google.com/identity/protocols/oauth2)
- [Google Cloud Console](https://console.cloud.google.com/)
- [OAuth 2.0 Playground](https://developers.google.com/oauthplayground/)

