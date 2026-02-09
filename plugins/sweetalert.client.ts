// plugins/sweetalert.client.ts
import Swal, {type SweetAlertOptions } from 'sweetalert2'

export default defineNuxtPlugin(() => {
    // Define a reusable function for showing toast notifications
    const showToast = (options: SweetAlertOptions) => {
        // @ts-ignore
        Swal.fire({
            ...options,
            toast: true,
            position: options.position || 'top-end',
            background: '#343a40',
            showConfirmButton: false,
            timer: 3000,
            timerProgressBar: true,
            didOpen: (toast) => {
                toast.addEventListener('mouseenter', Swal.stopTimer)
                toast.addEventListener('mouseleave', Swal.resumeTimer)
            }
        })
    }

    const confirmToast = (callback: () => void) => {
        // @ts-ignore
        Swal.fire({
            title: 'آیا از انجام این کار اطمینان دارید؟',
            text: 'پس از حذف امکان بازگردانی وجود ندارد.',
            icon: "warning",
            showCancelButton: true,
            confirmButtonColor: "#3b82f6",
            cancelButtonColor: "#d6293e",
            confirmButtonText: 'بله، مطمئنم!',
            cancelButtonText: 'خیر، منصرف شدم.',
        }).then((isConfirm) => {
            if (isConfirm.isConfirmed) {
                callback();
            }
        });
    }

    // Success notification
    const success = (title: string) => {
        showToast({
            icon: 'success',
            title,
            customClass: { title: 'text-white' }
        })
    }

    // Validation notification
    const validation = (title: string) => {
        showToast({
            icon: 'warning',
            title,
            customClass: { title: 'text-white' },
            position: 'bottom'
        })
    }

    // Error notification
    const error = (title: string) => {
        showToast({
            icon: 'error',
            title,
            customClass: { title: 'text-white' }
        })
    }

    const confirm = (callback: () => void) => {
        confirmToast(callback)
    }

    // Fire method for custom alerts
    const fire = (options: SweetAlertOptions) => {
        // @ts-ignore
        return Swal.fire(options)
    }

    // Show loading method
    const showLoading = () => {
        // @ts-ignore
        Swal.showLoading()
    }

    // Provide the functions globally in the app
    return {
        provide: {
            sweetalert: {
                success,
                validation,
                error,
                confirm,
                fire,
                showLoading,
            }
        }
    }
})
