<script setup>
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import OrderDetail from '../components/OrderDetail.vue'

const route = useRoute()
const order = ref(null)
const loading = ref(true)
const error = ref('')

const loadOrder = async () => {
  loading.value = true
  error.value = ''
  order.value = null

  const orderId = Number(route.query.order_id)
  if (!orderId) {
    error.value = 'Missing order_id in URL.'
    loading.value = false
    return
  }

  try {
    const res = await fetch('http://localhost:8000/products/orders/', {
      headers: { Accept: 'application/json' },
    })
    if (!res.ok) throw new Error(`Orders request failed: ${res.status}`)
    const data = await res.json()
    const target = Array.isArray(data?.results)
      ? data.results.find((o) => Number(o.id) === orderId)
      : null
    if (!target) {
      error.value = 'Order not found.'
    } else {
      order.value = target
    }
  } catch (err) {
    error.value = err?.message || 'Unable to load order.'
  } finally {
    loading.value = false
  }
}

onMounted(loadOrder)
</script>

<template>
  <main class="confirm-page">
    <header class="hero">
      <div>
        <p class="eyebrow">Checkout</p>
        <h1>Order confirmation</h1>
        <p class="muted">Thank you for your purchase. Here are your order details.</p>
      </div>
    </header>

    <OrderDetail :order="order" :loading="loading" :error="error" />
  </main>
</template>

<style scoped>
.confirm-page {
  display: flex;
  flex-direction: column;
  gap: 16px;
  max-width: 880px;
  margin: 0 auto;
  padding: 24px 18px 48px;
}

.hero {
  padding: 18px;
  border-radius: 14px;
  border: 1px solid #e2e8f0;
  background: linear-gradient(135deg, #e9efff, #f8fbff 50%, #ffffff);
  box-shadow: 0 12px 30px rgba(15, 23, 42, 0.06);
}

.eyebrow {
  text-transform: uppercase;
  letter-spacing: 1px;
  font-size: 12px;
  font-weight: 700;
  color: #2563eb;
  margin: 0 0 6px;
}

.muted {
  color: #475569;
  margin: 6px 0 0;
}
</style>
