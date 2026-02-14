import { nextTick } from "vue";
import type { Directive } from "vue";
import { useAuthStore } from "~/stores/auth";

const permissionDirective: Directive = {
  async mounted(el, binding) {
    const authStore = useAuthStore();

    if (!authStore.authenticated) {
      el.parentNode?.removeChild(el); // حذف المنت در صورت نداشتن مجوز
      return;
    }

    // دریافت مجوزها از API اگر قبلاً دریافت نشده‌اند
    if (!authStore.permissionsFetched) {
      await authStore.fetchPermissions();
    }

    await nextTick(); // اطمینان از پردازش Vue قبل از بررسی مجوزها

    // دریافت مجوزهای به‌روز شده از استور
    const userPermissions = authStore.permissions || [];
    const requiredPermissions = Array.isArray(binding.value) ? binding.value : [binding.value];

    const hasPermission = requiredPermissions.some(permission => userPermissions.includes(permission));

    // Debug logging for missing sections
    if (requiredPermissions.includes('webinar_manage') || requiredPermissions.includes('comment_manage')) {
      console.log('🔐 Permission Check for missing sections:', {
        required: requiredPermissions,
        userPermissions: userPermissions,
        hasPermission: hasPermission
      });
    }

    if (!hasPermission) {
      el.parentNode?.removeChild(el); // حذف المنت در صورت نداشتن مجوز
    }
  }
};

export default permissionDirective;
