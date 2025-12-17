<script setup>
const props = defineProps({
  orders: {
    type: Array,
    default: () => [],
  },
  loading: {
    type: Boolean,
    default: false,
  },
  error: {
    type: String,
    default: '',
  },
})

const formatCurrency = (cents) => (cents / 100).toFixed(2)
const formatDate = (iso) => (iso ? new Date(iso).toLocaleString() : '')
</script>

<template>
  <section class="orders">
    <header class="section-head">
      <div>
        <p class="eyebrow">Recent</p>
        <h2>Orders</h2>
      </div>
      <p class="muted">{{ orders.length }} total</p>
    </header>

    <div v-if="loading" class="status">Loading orders…</div>
    <div v-else-if="error" class="status error">{{ error }}</div>
    <div v-else-if="orders.length === 0" class="status">No orders yet.</div>
    <div v-else class="orders-grid">
      <article v-for="order in orders" :key="order.id" class="order-card">
        <div class="order-head">
          <div>
            <p class="muted">Order #{{ order.id }}</p>
            <p class="muted small">{{ formatDate(order.created_at) }}</p>
          </div>
          <div class="order-total">${{ formatCurrency(order.total) }}</div>
        </div>
        <div class="items">
          <div v-for="item in order.items" :key="item.id" class="item-row">
            <div class="thumb" :style="{ backgroundImage: `url(${item.product.image_url})` }"></div>
            <div class="item-meta">
              <p class="name">{{ item.product.name }}</p>
              <p class="muted small">Qty {{ item.quantity }}</p>
            </div>
            <div class="line">${{ formatCurrency(item.line_total) }}</div>
          </div>
        </div>
      </article>
    </div>
  </section>
</template>

<style scoped>
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

.status {
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
</style>
