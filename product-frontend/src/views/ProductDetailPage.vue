<script setup>
import { onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import ProductDetail from '../components/ProductDetail.vue'
import { useCartStore } from '../stores/cartStore'
const { addToCart, cartCount, cartTotal } = useCartStore()

const route = useRoute()
const product = ref(null)
const loading = ref(true)
const error = ref('')

const fetchProduct = async (id) => {
  loading.value = true
  error.value = ''
  product.value = null
  try {
    const res = await fetch(`http://localhost:8000/products/${id}/json/`, {
      headers: { Accept: 'application/json' },
    })
    if (!res.ok) throw new Error(`Product request failed: ${res.status}`)
    product.value = await res.json()
  } catch (err) {
    error.value = err?.message || 'Unable to load product.'
  } finally {
    loading.value = false
  }
}

onMounted(() => fetchProduct(route.params.id))
watch(
  () => route.params.id,
  (id) => {
    if (id) fetchProduct(id)
  },
)
</script>

<template>
  <ProductDetail @add="addToCart" :product="product" :loading="loading" :error="error" @back="$router.back()" />
</template>
