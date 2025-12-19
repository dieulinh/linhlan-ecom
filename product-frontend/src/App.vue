<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { useCartStore } from './stores/cartStore'

const { cartCount } = useCartStore()
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
        <span v-if="cartCount > 0" class="badge">{{ cartCount }}</span>
      </nav>
    </header>

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

.badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 20px;
  padding: 2px 8px;
  margin-left: 8px;
  border-radius: 999px;
  background: #2563eb;
  color: #fff;
  font-size: 12px;
  font-weight: 700;
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