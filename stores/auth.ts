import { defineStore } from "pinia";
import { useCookie } from "#app"; // Nuxt's built-in composable for cookies

// Define interfaces for better type safety
interface LoginForm {
  email: string;
  password: string;
}

interface User {
  id: number;
  name: string;
  email: string;
  // Add other user properties as needed
}

interface AuthState {
  user: User | null;
  token: string | null;
  authenticated: boolean;
  permissions: string[];
  permissionsFetched: boolean;
}

export const useAuthStore = defineStore("auth", {
  state: (): AuthState => ({
    user: null,
    token: useCookie("token").value || null,
    authenticated: false,
    permissions: [], // 🔥 اضافه شد: نگه‌داری مجوزها
    permissionsFetched: false, // 🔥 اضافه شد: جلوگیری از درخواست اضافه
  }),
  actions: {
    async login(form: LoginForm) {
      const { $api } = useNuxtApp();

      await $api
        .post("/auth/login", form)
        .then((value) => {
          this.setToken(value.data.data.token);
          setTimeout(() => {
            this.init(); // 🔥 بعد از لاگین، اطلاعات کاربر و مجوزها رو بگیر
          }, 300);
        })
        .catch((error) => {
          console.error("🚨 خطای ورود:", error);
        });
    },

    setToken(token: string) {
      const tokenCookie = useCookie("token");
      this.token = token;
      tokenCookie.value = token;
    },

    setUser(user: User) {
      this.user = user;
    },

    async logout() {
      const tokenCookie = useCookie("token");
      const router = useRouter();

      this.token = null;
      this.user = null;
      this.authenticated = false;
      this.permissions = []; // 🔥 مجوزها را پاک کن
      this.permissionsFetched = false; // 🔥 ریست کن

      tokenCookie.value = "";
      router.push("/");
    },

    async init() {
      this.authenticated = true;
      const { $api } = useNuxtApp();

      if (!this.token) {
        this.authenticated = false;
        return;
      }

      await $api
        .post(
          "/auth/init",
          {},
          {
            headers: {
              Authorization: `Bearer ${this.token}`,
            },
          }
        )
        .then(async (value) => {
          this.setUser(value.data.data);
          this.authenticated = true;

          // 🔥 بعد از دریافت اطلاعات کاربر، مجوزها را بگیر
          await this.fetchPermissions();
        })
        .catch((error) => {
          console.error("❌ خطا در دریافت اطلاعات کاربر:", error);
          this.authenticated = false;
        });
    },

    async fetchPermissions() {
      if (this.permissionsFetched) return; // اگر قبلاً گرفته شده، دوباره درخواست نده

      const { $api } = useNuxtApp();
      try {
        const response = await $api.post(
          "/auth/permissions/user",
          {},
          {
            headers: { Authorization: `Bearer ${this.token}` },
          }
        );

        this.permissions = response.data.data.map((perm: any) => perm.slug);
        this.permissionsFetched = true; // وضعیت رو علامت‌گذاری کن
      } catch (error) {
        console.error("🚨 خطا در دریافت مجوزها:", error);
        this.permissions = [];
        this.permissionsFetched = true;
      }
    },
  },
});
