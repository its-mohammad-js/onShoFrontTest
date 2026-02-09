<template>
    <div class="container my-5">
      <!-- Header -->
      <div class="d-flex align-items-center justify-content-between mb-4">
        <a class="fw-bold text-dark">
            <i class="fa fa-arrow-right ms-1"></i>
          بازگشت
         
        </a>
      </div>
  
      <!-- Orders Section -->
      <div class="card shadow-sm">
        <div class="card-header bg-danger py-3 text-white text-center fw-bold fs-4">
          سفارشات
        </div>
        <div class="card-body px-5">
          <table class="table table-borderless align-middle">
            <tbody>
              <tr>
                <td class="text-end d-flex align-items-center justify-content-start gap-3">
                  <img
                    src="https://via.placeholder.com/120"
                    class="img-fluid rounded"
                    alt="Course Thumbnail"
                  />
                 <div>
                    <p>
                    <span class="fw-bold">برگزارکننده:</span> <span class="text-danger1">های وب</span>
                  </p>
                  <p class="text-secondary-emphasis fs-5">
                    دوره آموزشی HTML, CSS
                  </p>
                 </div>
                </td>
              </tr>
              <tr>
                <td class="text-end d-flex align-items-center justify-content-start gap-3">
                  <img
                    src="https://via.placeholder.com/120"
                    class="img-fluid rounded"
                    alt="Course Thumbnail"
                  />
                 <div>
                    <p>
                    <span class="fw-bold">برگزارکننده:</span> <span class="text-danger1">های وب</span>
                  </p>
                  <p class="text-secondary-emphasis fs-5">
                    دوره آموزشی HTML, CSS
                  </p>
                 </div>
                </td>
              </tr>
            </tbody>
          </table>
  
          <!-- Static Details -->
          <div class="my-4">
            <p class="d-flex align-items-center justify-content-between py-4 border-bottom border-top">
              <span class="fw-bold text-muted">تاریخ خرید:</span> 
              <span class="fw-bold">۱۷ دی ۱۴۰۳</span>
            </p>
            <p class="d-flex align-items-center justify-content-between py-4 border-bottom">
              <span class="fw-bold text-muted">مبلغ کل:</span>
              <span class="text-danger1 fw-bold">۴,۵۰۰,۰۰۰ تومان</span>
            </p>
          </div>
  
          <!-- Discount Section -->
          <div class="d-flex justify-content-end align-items-center gap-3 my-4">
      <label for="discountCode">کد تخفیف خود را وارد کنید:</label>
      <input
        type="text"
        id="discountCode"
        class="form-control rounded-3 max-w-300-px py-3"
        placeholder="کد تخفیف خود را وارد کنید"

      />
    </div>
  
          <!-- Payment Button -->
          <div class="text-center">
            <button class="btn btn-danger w-25 py-3">
              پرداخت
            </button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <style scoped>
 .bg-danger {
  background-color: rgba(193, 18, 31, 1) !important;
}
  </style>
  