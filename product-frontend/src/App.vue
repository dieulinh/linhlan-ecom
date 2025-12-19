<script setup>
import { ref } from 'vue'
import { RouterLink, RouterView } from 'vue-router'
import { useCartStore } from './stores/cartStore'

const cart = useCartStore()
const { cartCount, cartTotal, cartItems } = cart
const showCart = ref(false)

const toggleCart = () => {
  showCart.value = !showCart.value
}
const closeCart = () => {
  showCart.value = false
}
</script>

<template>
  <div class="page">
    <header class="topbar">
      <div class="brand">LinhLan Shop</div>
      <nav class="nav">
        <RouterLink class="link-btn" to="/">Products</RouterLink>
        <RouterLink class="link-btn" to="/orders">
          Orders
        </RouterLink>
        <button class="cart-chip" type="button" @click="toggleCart">
          <span class="cart-icon" aria-hidden="true">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="9" cy="21" r="1.4" />
              <circle cx="19" cy="21" r="1.4" />
              <path d="M3 4h2l1.4 9.2A1.2 1.2 0 0 0 7.6 14h9.6a1.2 1.2 0 0 0 1.2-1l1-6.5H5.2" />
            </svg>
          </span>
          <span class="cart-label">Cart</span>
          <span class="cart-count-pill" :class="{ empty: cartCount === 0 }">{{ cartCount }}</span>
        </button>
      </nav>
    </header>

    <div v-if="showCart" class="cart-overlay" @click.self="closeCart">
      <div class="cart-panel">
        <header class="cart-head">
          <div>
            <p class="eyebrow">Cart</p>
            <h3>{{ cartCount }} items · ${{ cartTotal?.toFixed(2) }}</h3>
          </div>
          <button class="close" type="button" @click="closeCart">×</button>
        </header>
        <div v-if="cartItems.length" class="cart-list">
          <article v-for="item in cartItems" :key="item.id" class="cart-row">
            <div class="thumb" :style="{ backgroundImage: item.image_url ? `url(${item.image_url})` : '' }"></div>
            <div class="cart-meta">
              <p class="name">{{ item.name }}</p>
              <p class="muted">${{ item.price.toFixed(2) }}</p>
            </div>
            <div class="qty-controls">
              <button class="qty-btn" type="button" @click="cart.decrement(item.id)" :disabled="item.qty === 1">−</button>
              <span class="qty">{{ item.qty }}</span>
              <button class="qty-btn" type="button" @click="cart.increment(item.id)">＋</button>
            </div>
            <div class="line">${{ item.lineTotal.toFixed(2) }}</div>
            <button class="delete-btn" type="button" @click="cart.removeItem(item.id)" aria-label="Remove">
              ×
            </button>
          </article>
        </div>
        <div v-else class="status">Your cart is empty.</div>

        <footer class="cart-footer">
          <div class="cart-summary">
            <span>Total</span>
            <strong>${{ cartTotal?.toFixed(2) }}</strong>
          </div>
          <RouterLink class="checkout-btn" to="/orders" @click="closeCart">Checkout</RouterLink>
        </footer>
      </div>
    </div>

    <main>
      <RouterView />
    </main>
  </div>
</template>
         


<style scoped>
.page {
  min-height: 100vh;
  background: radial-gradient(circle at 20% 20%, #f5f8ff, #f7fbff 30%, #fdfdfd 60%);
  color: #0f172a;
}

.topbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 32px;
  position: sticky;
  top: 0;
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(8px);
  border-bottom: 1px solid #e2e8f0;
  z-index: 10;
}

.brand {
  font-size: 20px;
  font-weight: 700;
  letter-spacing: 0.4px;
}

.cart {
  display: flex;
  gap: 12px;
  align-items: baseline;
  font-weight: 600;
}

.cart-count {
  color: #0f172a;
}

.cart-total {
  color: #2563eb;
}

main {
  max-width: 1080px;
  margin: 0 auto;
  padding: 32px 24px 64px;
  display: flex;
  flex-direction: column;
  gap: 28px;
}

.hero {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 18px;
  background: linear-gradient(135deg, #e9efff, #f8fbff 50%, #ffffff);
  border: 1px solid #e2e8f0;
  border-radius: 18px;
  padding: 28px;
  box-shadow: 0 18px 40px rgba(15, 23, 42, 0.06);
}

.eyebrow {
  text-transform: uppercase;
  letter-spacing: 1px;
  font-size: 12px;
  font-weight: 700;
  color: #2563eb;
  margin: 0 0 8px;
}

h1 {
  margin: 0 0 8px;
  font-size: 32px;
  line-height: 1.15;
}

.lede {
  margin: 0 0 16px;
  color: #475569;
  max-width: 54ch;
}

.actions {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.btn {
  border: 1px solid transparent;
  border-radius: 10px;
  padding: 10px 14px;
  font-weight: 600;
  cursor: pointer;
  padding: 12px 14px;
  border-radius: 10px;
  border: 1px solid #e2e8f0;
  background: #fff;
  color: #0f172a;
}

.status.error {
  border-color: #fca5a5;
  background: #fef2f2;
  color: #b91c1c;
}

.status.success {
  border-color: #bbf7d0;
  background: #ecfdf3;
  color: #166534;
}

.link-btn {
  border: 1px solid #e2e8f0;
  background: #fff;
  color: #2563eb;
  border-radius: 10px;
  padding: 8px 12px;
  font-weight: 600;
  cursor: pointer;
  transition: background 120ms ease, transform 120ms ease, box-shadow 120ms ease;
}

.link-btn:hover {
  background: #f8fafc;
  transform: translateY(-1px);
  box-shadow: 0 8px 18px rgba(15, 23, 42, 0.08);
}

.nav {
  display: flex;
  gap: 10px;
}

.cart-chip {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  border-radius: 999px;
  border: 1px solid #e2e8f0;
  background: #fff;
  color: #0f172a;
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 8px 18px rgba(15, 23, 42, 0.08);
  transition: transform 120ms ease, box-shadow 120ms ease;
}

.cart-chip:hover {
  transform: translateY(-1px);
  box-shadow: 0 12px 22px rgba(15, 23, 42, 0.12);
}

.cart-icon {
  width: 18px;
  height: 18px;
  color: #2563eb;
  display: inline-flex;
}

.cart-label {
  font-size: 14px;
  font-weight: 700;
}

.cart-count-pill {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 22px;
  padding: 4px 8px;
  border-radius: 999px;
  background: #2563eb;
  color: #fff;
  font-size: 12px;
  font-weight: 800;
  line-height: 1;
}

.cart-count-pill.empty {
  background: #e2e8f0;
  color: #475569;
}

.link-btn {
  border: 1px solid #e2e8f0;
  background: #fff;
  color: #2563eb;
  border-radius: 10px;
  padding: 8px 12px;
  font-weight: 600;
  cursor: pointer;
  text-decoration: none;
  transition: background 120ms ease, transform 120ms ease, box-shadow 120ms ease;
}

.link-btn:hover {
  background: #f8fafc;
  transform: translateY(-1px);
  box-shadow: 0 8px 18px rgba(15, 23, 42, 0.08);
}

.link-btn.router-link-active {
  background: #2563eb;
  color: #fff;
  border-color: #2563eb;
  box-shadow: 0 8px 18px rgba(37, 99, 235, 0.2);
}

.cart-overlay {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.35);
  display: flex;
  align-items: flex-start;
  justify-content: flex-end;
  padding: 24px;
  z-index: 40;
}

.cart-panel {
  width: min(420px, 100%);
  background: #fff;
  border-radius: 16px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 22px 50px rgba(15, 23, 42, 0.24);
  padding: 18px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.cart-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
}

.cart-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.cart-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 12px;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  background: #f8fafc;
  gap: 12px;
}

.cart-summary {
  display: flex;
  align-items: baseline;
  gap: 8px;
  font-weight: 700;
}

.checkout-btn {
  border: 1px solid transparent;
  border-radius: 10px;
  padding: 10px 14px;
  background: #2563eb;
  color: #fff;
  font-weight: 700;
  text-decoration: none;
  box-shadow: 0 10px 24px rgba(37, 99, 235, 0.22);
  transition: transform 120ms ease, box-shadow 120ms ease;
}

.checkout-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 14px 28px rgba(37, 99, 235, 0.3);
}

.cart-row {
  display: grid;
  grid-template-columns: 56px 1fr auto auto 36px;
  gap: 10px;
  align-items: center;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 10px;
  background: #fff;
}

.cart-row .thumb {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  background-size: cover;
  background-position: center;
  border: 1px solid #e2e8f0;
}

.cart-meta .name {
  margin: 0;
  font-weight: 700;
}

.qty {
  font-weight: 700;
  color: #0f172a;
}

.qty-controls {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  padding: 4px 6px;
}

.qty-btn {
  width: 28px;
  height: 28px;
  border-radius: 8px;
  border: 1px solid #dbeafe;
  background: #fff;
  color: #2563eb;
  font-weight: 800;
  cursor: pointer;
  transition: background 120ms ease, transform 120ms ease;
}

.qty-btn:hover:not(:disabled) {
  background: #eff6ff;
  transform: translateY(-1px);
}

.qty-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.line {
  font-weight: 700;
  color: #2563eb;
}

.delete-btn {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  border: 1px solid #fee2e2;
  background: #fff1f2;
  color: #b91c1c;
  font-weight: 800;
  cursor: pointer;
  transition: background 120ms ease, transform 120ms ease;
}

.delete-btn:hover {
  background: #fecdd3;
  transform: translateY(-1px);
}

.checkout-overlay {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.45);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 30;
  padding: 20px;
}

.checkout-panel {
  position: relative;
  background: #fff;
  width: min(420px, 100%);
  border-radius: 16px;
  padding: 22px;
  box-shadow: 0 22px 50px rgba(15, 23, 42, 0.2);
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.checkout-panel .close {
  position: absolute;
  top: 12px;
  right: 12px;
  border: none;
  background: transparent;
  font-size: 20px;
  cursor: pointer;
}

.quantity {
  display: flex;
  align-items: center;
  gap: 10px;
}

.quantity button {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  border: 1px solid #e2e8f0;
  background: #fff;
  cursor: pointer;
}

.quantity span {
  min-width: 32px;
  text-align: center;
  font-weight: 700;
}

.total {
  font-weight: 800;
  font-size: 18px;
}

.btn.wide {
  width: 100%;
  justify-content: center;
  display: inline-flex;
  align-items: center;
  text-align: center;
}

.orders {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.orders-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 14px;
}

.order-card {
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 14px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  box-shadow: 0 12px 30px rgba(15, 23, 42, 0.05);
}

.order-head {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.order-total {
  font-weight: 800;
  color: #0f172a;
}

.items {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.item-row {
  display: grid;
  grid-template-columns: 48px 1fr auto;
  gap: 10px;
  align-items: center;
}

.thumb {
  width: 48px;
  height: 48px;
  border-radius: 10px;
  background-size: cover;
  background-position: center;
  border: 1px solid #e2e8f0;
}

.item-meta .name {
  margin: 0;
  font-weight: 600;
}

.small {
  font-size: 12px;
}

.line {
  font-weight: 700;
  color: #0f172a;
}

@media (max-width: 640px) {
  .topbar {
    flex-direction: column;
    gap: 8px;
    align-items: flex-start;
  }

  main {
    padding: 20px 16px 48px;
  }
}
</style>