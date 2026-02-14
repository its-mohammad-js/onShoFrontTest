# راهنمای حل مشکل Google OAuth - redirect_uri_mismatch

## مشکل: Error 400: redirect_uri_mismatch

این خطا زمانی رخ می‌دهد که `redirect_uri` که به Google ارسال می‌شود با `redirect_uri` که در Google Cloud Console ثبت شده است مطابقت ندارد.

## مراحل حل مشکل:

### 1. بررسی redirect_uri که به Google ارسال می‌شود

وقتی روی دکمه "ورود با گوگل" کلیک می‌کنید، URL باید شبیه این باشد:
```
http://127.0.0.1:8000/auth/google/login?redirect_uri=http%3A%2F%2Flocalhost%3A3000%2Fauth%2Fgoogle%2Fcallback
```

که decode شده می‌شود به:
```
http://127.0.0.1:8000/auth/google/login?redirect_uri=http://localhost:3000/auth/google/callback
```

### 2. تنظیم Authorized Redirect URIs در Google Cloud Console

1. به [Google Cloud Console](https://console.cloud.google.com/) بروید
2. پروژه خود را انتخاب کنید
3. به **APIs & Services** > **Credentials** بروید
4. روی OAuth 2.0 Client ID خود کلیک کنید (یا ایجاد کنید)
5. در بخش **Authorized redirect URIs**، این URI ها را اضافه کنید:

#### برای Development:
```
http://localhost:3000/auth/google/callback
http://127.0.0.1:3000/auth/google/callback
```

#### برای Production:
```
https://yourdomain.com/auth/google/callback
https://www.yourdomain.com/auth/google/callback
```

**نکات مهم:**
- ✅ باید دقیقاً مطابق باشد (حتی `/` در انتها مهم است)
- ✅ باید `http://` یا `https://` داشته باشد
- ✅ نباید trailing slash اضافی داشته باشد (مگر اینکه در URL شما باشد)
- ✅ Port number مهم است (`:3000`)

### 3. بررسی Backend

Backend باید `redirect_uri` را دقیقاً همان‌طور که از frontend دریافت می‌کند به Google ارسال کند.

**مثال کد Backend (Laravel/PHP):**

```php
public function googleLogin(Request $request)
{
    $redirectUri = $request->query('redirect_uri');
    
    // مطمئن شوید که redirect_uri را encode نمی‌کنید (Google خودش این کار را می‌کند)
    // و دقیقاً همان‌طور که دریافت کردید به Google ارسال کنید
    
    $googleClient = new \Google_Client();
    $googleClient->setClientId(config('services.google.client_id'));
    $googleClient->setClientSecret(config('services.google.client_secret'));
    $googleClient->setRedirectUri($redirectUri); // استفاده از redirect_uri دریافتی
    $googleClient->addScope('email');
    $googleClient->addScope('profile');
    
    $authUrl = $googleClient->createAuthUrl();
    
    return redirect($authUrl);
}
```

**مثال کد Backend (Node.js/Express):**

```javascript
app.get('/auth/google/login', (req, res) => {
  const redirectUri = req.query.redirect_uri;
  
  const oauth2Client = new google.auth.OAuth2(
    process.env.GOOGLE_CLIENT_ID,
    process.env.GOOGLE_CLIENT_SECRET,
    redirectUri // استفاده از redirect_uri دریافتی
  );
  
  const authUrl = oauth2Client.generateAuthUrl({
    access_type: 'offline',
    scope: ['email', 'profile'],
    prompt: 'select_account'
  });
  
  res.redirect(authUrl);
});
```

### 4. بررسی مشکلات رایج

#### مشکل 1: Backend redirect_uri را تغییر می‌دهد
**راه حل:** مطمئن شوید که backend دقیقاً همان `redirect_uri` را که از frontend دریافت می‌کند به Google ارسال می‌کند.

#### مشکل 2: Port number متفاوت است
**راه حل:** اگر frontend روی port دیگری اجرا می‌شود، باید آن port را در Google Cloud Console اضافه کنید.

#### مشکل 3: http vs https
**راه حل:** در development از `http://` و در production از `https://` استفاده کنید.

#### مشکل 4: Trailing slash
**راه حل:** مطمئن شوید که در Google Cloud Console دقیقاً همان URL را ثبت کنید که در کد استفاده می‌کنید (با یا بدون `/` در انتها).

### 5. تست کردن

1. مطمئن شوید که redirect_uri در Google Cloud Console ثبت شده است
2. Backend را restart کنید
3. Frontend را restart کنید
4. دوباره روی دکمه "ورود با گوگل" کلیک کنید
5. باید به صفحه Google OAuth هدایت شوید (بدون خطا)

### 6. Debug کردن

برای debug کردن، می‌توانید این اطلاعات را چک کنید:

**در Frontend (Console):**
```javascript
const redirectUri = `${window.location.origin}/auth/google/callback`;
console.log('Redirect URI:', redirectUri);
// باید: http://localhost:3000/auth/google/callback
```

**در Backend (Log):**
```php
// Laravel
Log::info('Redirect URI received:', ['uri' => $request->query('redirect_uri')]);
Log::info('Redirect URI sent to Google:', ['uri' => $redirectUri]);
```

```javascript
// Node.js
console.log('Redirect URI received:', req.query.redirect_uri);
console.log('Redirect URI sent to Google:', redirectUri);
```

### 7. چک‌لیست نهایی

- [ ] Redirect URI در Google Cloud Console ثبت شده است
- [ ] Redirect URI دقیقاً مطابق است (با port، http/https، trailing slash)
- [ ] Backend redirect_uri را تغییر نمی‌دهد
- [ ] Backend redirect_uri را به درستی به Google ارسال می‌کند
- [ ] Client ID و Client Secret درست هستند
- [ ] OAuth Consent Screen تنظیم شده است

## اگر مشکل حل نشد:

1. **بررسی Console Logs:** در مرورگر و backend
2. **بررسی Network Tab:** ببینید چه request هایی ارسال می‌شود
3. **تست با Postman:** ببینید آیا backend درست کار می‌کند
4. **بررسی Google Cloud Console:** مطمئن شوید که همه تنظیمات درست است

## منابع:

- [Google OAuth 2.0 Documentation](https://developers.google.com/identity/protocols/oauth2)
- [OAuth 2.0 Playground](https://developers.google.com/oauthplayground/)

