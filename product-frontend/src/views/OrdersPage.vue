<script setup>
import { onMounted, ref } from 'vue'
import Orders from '../components/Orders.vue'

const orders = ref([])
const ordersLoading = ref(true)
const ordersError = ref('')

const loadOrders = async () => {
  ordersLoading.value = true
  ordersError.value = ''
  try {
    const res = await fetch('http://localhost:8000/products/orders/', {
      headers: { Accept: 'application/json' },
    })
    if (!res.ok) throw new Error(`Orders request failed: ${res.status}`)
    const data = await res.json()
    orders.value = Array.isArray(data?.results) ? data.results : []
  } catch (err) {
    ordersError.value = err?.message || 'Unable to load orders.'
  } finally {
    ordersLoading.value = false
  }
}

onMounted(loadOrders)
</script>

<template>
  <Orders :orders="orders" :loading="ordersLoading" :error="ordersError" />
</template>
