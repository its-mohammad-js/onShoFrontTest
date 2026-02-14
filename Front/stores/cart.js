import { defineStore } from "pinia";
import { useCookie } from "#app";

export const useCartStore = defineStore("cart", {
  state: () => ({
    cartItems: [],
    discount: 0,
  }),
  getters: {
    totalPrice: (state) =>
      state.cartItems.reduce((sum, item) => sum + (item.price || 0), 0),
    finalPrice: (state) => state.totalPrice - state.discount,
  },
  actions: {
    loadCart() {
      try {
        const cartCookie = useCookie("cart");

        if (cartCookie.value) {
          this.cartItems = JSON.parse(JSON.stringify(cartCookie.value));
        } else {
          this.cartItems = [];
        }
      } catch (error) {
        this.cartItems = [];
      }
    },

    saveCart() {
      try {
        const cartCookie = useCookie("cart", { maxAge: 60 * 60 * 24 * 7 });
        cartCookie.value = JSON.stringify(this.cartItems);
      } catch (error) {}
    },

    addToCart(item) {
      const existingItem = this.cartItems.find((i) => i.id === item.id);
      if (!existingItem) {
        this.cartItems.push(item);
        this.saveCart();
      } else {
      }
    },

    removeFromCart(index) {
      this.cartItems.splice(index, 1);
      this.saveCart();
    },

    applyDiscount(code) {
      const validDiscounts = {
        OFF10: 10,
        OFF20: 20,
        OFF50: 50,
      };

      if (validDiscounts[code]) {
        const discountPercentage = validDiscounts[code];
        this.discount = (this.totalPrice * discountPercentage) / 100;
        return {
          success: true,
          message: `تخفیف ${discountPercentage}% اعمال شد.`,
        };
      } else {
        return { success: false, message: "کد تخفیف معتبر نیست!" };
      }
    },
  },
});
