<template>
  <div class="container my-5">
    <div class="row">
      <div class="col-12">
        <div class="mb-5">
          <a
            href="#"
            class="text-secondary-emphasis text-decoration-none fw-bold"
          >
            <i class="icon icon-filled-arrow-right ms-2"></i>بازگشت
          </a>
        </div>
      </div>

      <!-- بخش سبد خرید -->
      <div class="col-lg-8">
        <div
          class="p-4 rounded-0 rounded-top bg-danger-subtle d-flex align-items-center justify-content-between flex-wrap"
        >
          <div class="d-flex gap-2 align-items-center">
            <i
              class="icon icon-filled-shopping-cart text-secondary-emphasis fs-4"
            ></i>
            <h4 class="text-secondary-emphasis fs-5 mb-0">سبد خرید شما</h4>
          </div>
          <img src="/images/checkout/1.png" alt="" style="margin-top: -100px" />
        </div>

        <div class="p-4 bg-light border-0 rounded-0 rounded-bottom">
          <div class="table-responsive">
            <table class="table">
              <tbody>
                <tr
                  v-for="(item, index) in cartStore.cartItems"
                  :key="index"
                  class="align-middle bg-white"
                >
                  <td class="bg-white">
                    <img
                      :src="item.image"
                      alt="Course Image"
                      class="rounded w-100-px h-75-px object-fit-cover"
                    />
                  </td>
                  <td class="bg-white">
                    <div class="d-flex flex-column gap-2">
                      <h6 class="small mb-0">
                        <span class="text-muted small">برگزار کننده :</span>
                        <span class="me-2 text-danger1">{{
                          item.provider
                        }}</span>
                      </h6>
                      <h6 class="fw-bold mb-0">{{ item.title }}</h6>
                    </div>
                  </td>
                  <td class="bg-white text-center">
                    <div class="d-flex flex-column gap-2">
                      <span class="text-muted small">قیمت دوره :</span>
                      <span class="fw-bold"
                        >{{ formatPrice(item.price) }} تومان</span
                      >
                    </div>
                  </td>
                  <td class="text-start bg-white">
                    <button
                      class="btn btn-light btn-sm p-0 px-1 border"
                      @click="removeItem(index)"
                    >
                      <i class="icon icon-filled-trash small text-danger1"></i>
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div
          class="d-flex align-items-center bg-light p-3 rounded w-100 mt-3 flex-wrap gap-3"
        >
          <i class="fa-solid fa-gift fs-4 text-dark"></i>
          <span class="text-dark">کد تخفیف خود را وارد کنید:</span>
          <div class="flex-grow-1">
            <input
              type="text"
              v-model="discountCode"
              class="form-control text-end py-3 w-100 w-md-50 rounded-3 shadow-none"
              placeholder="کد تخفیف"
            />
          </div>
          <button class="btn btn-danger py-3" @click="applyDiscountCode">
            اعمال کد
          </button>
        </div>
      </div>

      <!-- بخش پرداخت -->
      <div class="col-lg-4 mt-4 mt-lg-0">
        <div class="p-4 bg-danger-subtle border-0 rounded">
          <div class="p-3 bg-white rounded">
            <div class="d-flex justify-content-between py-2 px-4">
              <span>هزینه دوره‌ها:</span>
              <span>{{ formatPrice(cartStore.totalPrice) }} تومان</span>
            </div>
            <div class="d-flex justify-content-between py-2 px-4 text-danger1">
              <span>سود شما از خرید ویژه:</span>
              <span class="fw-bold"
                >{{ formatPrice(cartStore.discount) }} تومان</span
              >
            </div>
            <hr />
            <div class="d-flex justify-content-between p-3 fw-bold">
              <span>مبلغ قابل پرداخت:</span>
              <span class="fw-bold"
                >{{ formatPrice(cartStore.finalPrice) }} تومان</span
              >
            </div>
          </div>
          <!-- دکمه پرداخت -->
          <button
            class="btn bg-dark-subtle w-100 mt-3 text-white py-2"
            @click="processPayment"
            id="payment-button"
          >
            پرداخت
          </button>
          <!-- متن توضیحی -->
          <div class="text-muted mt-3 d-flex align-items-center gap-2">
            <i class="fa-solid fa-triangle-exclamation text-warning fs-4"></i>
            <p class="text-muted small mb-0">
              پرداخت وجه سفارش به منزله مطالعه و پذیرش قوانین و شرایط استفاده از
              خدمات است.
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useCartStore } from "~/stores/cart";
import { useNuxtApp, useCookie } from "#app";

const cartStore = useCartStore();
const discountCode = ref("");
const { $sweetalert } = useNuxtApp();

const formatPrice = (value) => (value ? value.toLocaleString() : "۰");

onMounted(() => {
  try {
    console.log("🔄 Loading cart on checkout page...");
    cartStore.loadCart(); // خواندن مقدار از کوکی و مقداردهی مجدد

    console.log(
      "📌 مقدار `cartStore.cartItems` بعد از مقداردهی در Checkout:",
      cartStore.cartItems,
    );
    console.log("💰 Total price:", cartStore.totalPrice);
    console.log("💳 Final price:", cartStore.finalPrice);
  } catch (error) {
    console.error("🚨 خطا در مقداردهی سبد خرید:", error);
  }
});

const removeItem = (index) => {
  cartStore.removeFromCart(index);
  location.reload(); // صفحه را رفرش کن
};

const applyDiscountCode = () => {
  const result = cartStore.applyDiscount(discountCode.value);
  if (result.success) {
    $sweetalert.success(result.message);
  } else {
    $sweetalert.error(result.message);
  }
};

const processPayment = async () => {
  console.log("🔄 Payment process started");
  const token = useCookie("token").value;

  console.log("🔑 Token:", token ? "Present" : "Missing");
  console.log("🛒 Cart items:", cartStore.cartItems);

  if (!token) {
    $sweetalert.error("جهت پرداخت لطفاً وارد حساب کاربری خود شوید");
    return;
  }

  if (cartStore.cartItems.length === 0) {
    console.log("❌ Cart is empty!");
    $sweetalert.error("سبد خرید شما خالی است!");
    return;
  }

  console.log("✅ Cart has items, proceeding with payment...");

  try {
    // Show loading
    const loadingAlert = $sweetalert.fire({
      title: "در حال پردازش...",
      text: "لطفاً صبر کنید",
      allowOutsideClick: false,
      showConfirmButton: false,
      didOpen: () => {
        $sweetalert.showLoading();
      },
    });

    // Prepare courses data for API
    const courses = cartStore.cartItems.map((item) => ({
      course_id: item.id,
      quantity: 1,
    }));

    console.log("📦 Courses data:", courses);

    // Create order
    const { $api } = useNuxtApp();
    console.log("🌐 Making API call to /payment/ordersub");

    const response = await $api.post(
      "/payment/ordersub",
      {
        courses: courses,
      },
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      },
    );

    console.log("📡 API Response:", response.data);

    if (response.data.status) {
      // Loading alert will be replaced by new alerts

      // Initialize payment gateway
      console.log("🔄 Initializing payment gateway...");
      const gatewayResponse = await $api.post(
        "/payment/gateway/init",
        {
          order_id: response.data.data.order_id,
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        },
      );

      if (gatewayResponse.data.status) {
        console.log(
          "✅ Payment gateway initialized, redirecting to payment page...",
        );

        // Clear cart
        cartStore.cartItems = [];
        cartStore.saveCart();

        // Check if this is test mode
        if (gatewayResponse.data.data.test_mode) {
          console.log("🧪 Test mode detected, redirecting to callback...");
          // For test mode, redirect directly to callback
          window.location.href = gatewayResponse.data.data.payment_url;
        } else {
          // Redirect to real payment gateway
          window.location.href = gatewayResponse.data.data.payment_url;
        }
      } else {
        $sweetalert.error(
          "خطا در راه‌اندازی درگاه پرداخت: " + gatewayResponse.data.data.error,
        );
      }
    } else {
      $sweetalert.error("خطا در ثبت سفارش");
    }
  } catch (error) {
    console.error("❌ Error processing payment:", error);
    console.error("❌ Error response:", error.response?.data);
    console.error("❌ Error status:", error.response?.status);

    if (error.response?.data?.data?.courses) {
      $sweetalert.error("برخی از دوره‌ها قبلاً خریداری شده‌اند!");
    } else if (error.response?.status === 401) {
      $sweetalert.error("احراز هویت ناموفق. لطفاً دوباره وارد شوید.");
    } else if (error.response?.status === 403) {
      $sweetalert.error("شما مجوز لازم برای این عملیات را ندارید.");
    } else {
      $sweetalert.error("خطا در پردازش پرداخت");
    }
  }
};
</script>

<style scoped>
.bg-danger-subtle {
  background-color: #fbf1f2 !important;
}
.bg-dark-subtle {
  background-color: rgba(43, 45, 66, 1) !important;
}
</style>
