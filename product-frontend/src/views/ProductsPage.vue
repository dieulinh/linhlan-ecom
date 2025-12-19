<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import Products from '../components/Products.vue'
import { useCartStore } from '../stores/cartStore'

const router = useRouter()
const cart = useCartStore()
const { addToCart, cartTotal } = cart

const products = ref([])
const loading = ref(true)
const error = ref('')

const checkoutVisible = ref(false)
const checkoutItem = ref(null)
const checkoutQty = ref(1)
const checkoutLoading = ref(false)
const checkoutError = ref('')

const search = ref('')
const category = ref('all')
const sort = ref('featured')

const categories = computed(() => ['all', ...new Set(products.value.map((p) => p.category || 'Uncategorized'))])

const filtered = computed(() => {
  const term = search.value.trim().toLowerCase()
  const byCategory = (item) => category.value === 'all' || item.category === category.value
  const bySearch = (item) =>
    !term || item.name.toLowerCase().includes(term) || (item.description || '').toLowerCase().includes(term)

  const sorted = [...products.value]
    .filter((item) => byCategory(item) && bySearch(item))
    .sort((a, b) => {
      if (sort.value === 'price-asc') return a.price - b.price
      if (sort.value === 'price-desc') return b.price - a.price
      if (sort.value === 'rating') return (b.rating || 0) - (a.rating || 0)
      return a.id - b.id
    })

  return sorted
})

const startCheckout = (item) => {
  checkoutItem.value = item
  checkoutQty.value = 1
  checkoutError.value = ''
  checkoutVisible.value = true
}

const closeCheckout = () => {
  checkoutVisible.value = false
}

const incrementQty = () => {
  checkoutQty.value += 1
}

const decrementQty = () => {
  if (checkoutQty.value > 1) checkoutQty.value -= 1
}

const instantCheckout = async () => {
  if (!checkoutItem.value) return
  checkoutError.value = ''
  checkoutLoading.value = true
  try {
    const res = await fetch('http://localhost:8000/products/instant_checkout/', {
      method: 'POST',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ product_id: checkoutItem.value.id, quantity: checkoutQty.value }),
    })
    if (!res.ok) throw new Error(`Checkout failed: ${res.status}`)
    await res.json()
    checkoutVisible.value = false
  } catch (err) {
    checkoutError.value = err?.message || 'Instant checkout failed.'
  } finally {
    checkoutLoading.value = false
  }
}

const loadProducts = async () => {
  loading.value = true
  error.value = ''
  try {
    const res = await fetch('http://localhost:8000/products/list/', {
      headers: { Accept: 'application/json' },
    })
    if (!res.ok) throw new Error(`Request failed with status ${res.status}`)
    const data = await res.json()
    products.value = Array.isArray(data?.results) ? data.results : []
  } catch (err) {
    error.value = err?.message || 'Unable to load products.'
  } finally {
    loading.value = false
  }
}

const viewProduct = (item) => {
  router.push({ name: 'product-detail', params: { id: item.id } })
}

onMounted(loadProducts)
</script>

<template>
  <section class="page-body">
    <header class="hero">
      <div>
        <p class="eyebrow">New arrivals</p>
        <h1>Curated picks for everyday living</h1>
        <p class="lede">
          Explore a handful of products with clean design, quality materials, and prices that make sense.
        </p>
      </div>
      <div class="hero-card">
        <p class="muted">Fast shipping · 30-day returns</p>
        <p class="muted">Secure checkout · Chat support</p>
      </div>
      <div :v-if="cartTotal" class="cart">
        <span class="cart-count">{{ cart.cartCount }} items</span>
        <span class="cart-total">${{cartTotal?.toFixed(2) }}</span>
      </div>
    </header>

    <section class="controls">
      <div class="field">
        <label>Search</label>
        <input v-model="search" type="search" placeholder="Find products" />
      </div>
      <div class="field">
        <label>Category</label>
        <select v-model="category">
          <option v-for="cat in categories" :key="cat" :value="cat">{{ cat }}</option>
        </select>
      </div>
      <div class="field">
        <label>Sort</label>
        <select v-model="sort">
          <option value="featured">Featured</option>
          <option value="price-asc">Price: Low to High</option>
          <option value="price-desc">Price: High to Low</option>
          <option value="rating">Top Rated</option>
        </select>
      </div>
    </section>

    <div v-if="loading" class="status">Loading products…</div>
    <div v-else-if="error" class="status error">{{ error }}</div>
    <Products v-else :items="filtered" @add="addToCart" @instant-checkout="startCheckout" @view="viewProduct" />

    <div v-if="checkoutVisible" class="checkout-overlay">
      <div class="checkout-panel">
        <button class="close" type="button" @click="closeCheckout">×</button>
        <p class="eyebrow">Instant checkout</p>
        <h3>{{ checkoutItem?.name }}</h3>
        <p class="muted">${{ checkoutItem?.price?.toFixed(2) }}</p>

        <div class="quantity">
          <button type="button" @click="decrementQty" :disabled="checkoutQty === 1">−</button>
          <span>{{ checkoutQty }}</span>
          <button type="button" @click="incrementQty">＋</button>
        </div>

        <p class="total">Total ${{ (checkoutItem?.price * checkoutQty)?.toFixed(2) }}</p>

        <button class="btn primary wide" type="button" :disabled="checkoutLoading" @click="instantCheckout">
          {{ checkoutLoading ? 'Processing…' : 'Place order' }}
        </button>

        <div v-if="checkoutError" class="status error">{{ checkoutError }}</div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.page-body {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.hero {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 14px;
  background: linear-gradient(135deg, #e9efff, #f8fbff 50%, #ffffff);
  border: 1px solid #e2e8f0;
  border-radius: 18px;
  padding: 20px;
  box-shadow: 0 18px 40px rgba(15, 23, 42, 0.06);
}

.cart {
  display: flex;
  gap: 10px;
  align-items: baseline;
  font-weight: 700;
  justify-content: flex-end;
}

.controls {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 14px;
  padding: 18px;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  background: #fff;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.field label {
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.6px;
  color: #475569;
}

input,
select {
  padding: 10px 12px;
  border-radius: 10px;
  border: 1px solid #cbd5e1;
  background: #fff;
  font-size: 14px;
  transition: border-color 120ms ease, box-shadow 120ms ease;
}

input:focus,
select:focus {
  outline: none;
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.12);
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

.btn.primary.wide {
  width: 100%;
  justify-content: center;
  display: inline-flex;
  align-items: center;
  text-align: center;
  border: 1px solid transparent;
  border-radius: 10px;
  padding: 12px 14px;
  background: #2563eb;
  color: #fff;
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 10px 24px rgba(37, 99, 235, 0.25);
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
