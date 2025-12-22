<script setup>
const props = defineProps({
  order: {
    type: Object,
    default: null,
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
  <section class="order-detail">
    <div class="header">
      <div>
        <p class="eyebrow">Order</p>
        <h2 v-if="order">#{{ order.id }}</h2>
        <h2 v-else>Order</h2>
        <p class="muted" v-if="order">Placed {{ formatDate(order.created_at) }}</p>
      </div>
      <div class="total" v-if="order">${{ formatCurrency(order.total) }}</div>
    </div>

    <div v-if="loading" class="status">Loading order…</div>
    <div v-else-if="error" class="status error">{{ error }}</div>
    <div v-else-if="!order" class="status">No order to display.</div>
    <div v-else>
      <div class="items">
        <article v-for="item in order.items" :key="item.id" class="item-row">
          <div class="thumb" :style="{ backgroundImage: `url(${item.product.image_url})` }"></div>
          <div class="meta">
            <p class="name">{{ item.product.name }}</p>
            <p class="muted">Qty {{ item.quantity }}</p>
          </div>
          <div class="line">${{ formatCurrency(item.line_total) }}</div>
        </article>
      </div>

      <div class="summary">
        <div class="row">
          <span>Subtotal</span>
          <strong>${{ formatCurrency(order.total) }}</strong>
        </div>
        <div class="row muted">
          <span>Tax & shipping</span>
          <span>Calculated at payment</span>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.order-detail {
  display: flex;
  flex-direction: column;
  gap: 14px;
  padding: 16px;
  border: 1px solid #e2e8f0;
  border-radius: 14px;
  background: #fff;
  box-shadow: 0 12px 28px rgba(15, 23, 42, 0.05);
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.eyebrow {
  text-transform: uppercase;
  letter-spacing: 1px;
  font-size: 12px;
  font-weight: 700;
  color: #2563eb;
  margin: 0;
}

.muted {
  color: #64748b;
  margin: 2px 0 0;
  font-size: 13px;
}

.total {
  font-weight: 800;
  font-size: 20px;
  color: #0f172a;
}

.items {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.item-row {
  display: grid;
  grid-template-columns: 56px 1fr auto;
  gap: 12px;
  align-items: center;
  padding: 10px;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  background: #f8fafc;
}

.thumb {
  width: 56px;
  height: 56px;
  border-radius: 10px;
  background-size: cover;
  background-position: center;
  border: 1px solid #e2e8f0;
}

.meta .name {
  margin: 0;
  font-weight: 700;
}

.line {
  font-weight: 700;
  color: #0f172a;
}

.summary {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 12px;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  background: #f8fafc;
}

.summary .row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
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
