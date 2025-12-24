<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import OrderDetail from '../components/OrderDetail.vue'
import AddressForm from '../components/AddressForm.vue'

const route = useRoute()
const order = ref(null)
const loading = ref(true)
const error = ref('')
const savingAddress = ref(false)
const addressError = ref('')
const hasAddress = computed(() => !!order.value?.shipping_address)
const handleSave = async (address) => {
  addressError.value = ''
  savingAddress.value = true
  try {
    console.log('Saving address for order:', order.value.id, address)
    const res = await fetch(
      `http://localhost:8000/products/orders/${order.value.id}/address/`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify(address),
      },
    )
    if (!res.ok) throw new Error(`Save address request failed: ${res.status}`)
    const data = await res.json()
    console.log('Address saved:', data)
    order.value = {
      ...order.value,
      shipping_address: data.address,
    }
  } catch (err) {
    addressError.value = err?.message || 'Unable to save address.'
  } finally {
    savingAddress.value = false
  }
}

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

    <OrderDetail :order="order"  :loading="loading" :error="error" />
    <section v-if="order && hasAddress" class="address-card">
      <header class="address-head">
        <div>
          <p class="eyebrow">Shipping address</p>
          <h3>Delivery details</h3>
        </div>
      </header>
      <div class="address-body">
        <p class="strong">{{ order.shipping_address.full_name }}</p>
        <p class="muted">{{ order.shipping_address.email }}</p>
        <p class="muted" v-if="order.shipping_address.phone">{{ order.shipping_address.phone }}</p>
        <p>{{ order.shipping_address.line1 }}</p>
        <p v-if="order.shipping_address.line2">{{ order.shipping_address.line2 }}</p>
        <p>{{ order.shipping_address.city }}, {{ order.shipping_address.state }} {{ order.shipping_address.postal_code }}</p>
        <p>{{ order.shipping_address.country }}</p>
      </div>
    </section>

    <address-form
      v-else-if="order"
      @submit="handleSave"
      :key="order.id"
      :initial-address="order.shipping_address"
    />
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

.address-card {
  padding: 16px;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  background: #fff;
  box-shadow: 0 10px 24px rgba(15, 23, 42, 0.05);
}

.address-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.address-body {
  display: flex;
  flex-direction: column;
  gap: 2px;
  color: #0f172a;
}

.strong {
  font-weight: 700;
  margin: 0;
}
</style>
