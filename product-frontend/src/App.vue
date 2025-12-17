<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import Products from './components/Products.vue'
import Orders from './components/Orders.vue'

const products = ref([])
const loading = ref(true)
const error = ref('')
const checkoutMessage = ref('')
const checkoutError = ref('')
const checkoutVisible = ref(false)
const checkoutItem = ref(null)
const checkoutQty = ref(1)
const checkoutLoading = ref(false)
const orders = ref([])
const ordersLoading = ref(true)
const ordersError = ref('')
const activePage = ref('products')

const search = ref('')
const category = ref('all')
const sort = ref('featured')
const cart = reactive(new Map())

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

const cartCount = computed(() => {
  let total = 0
  cart.forEach((qty) => {
    total += qty
  })
  return total
})

const cartTotal = computed(() => {
  let total = 0
  cart.forEach((qty, id) => {
    const item = products.value.find((p) => p.id === id)
    if (item) total += qty * item.price
  })
  return total
})

const addToCart = (item) => {
  const current = cart.get(item.id) ?? 0
  cart.set(item.id, current + 1)
}

const goToOrders = () => {
  activePage.value = 'orders'
}

const goToProducts = () => {
  activePage.value = 'products'
}

const startCheckout = (item) => {
  checkoutItem.value = item
  checkoutQty.value = 1
  checkoutMessage.value = ''
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

  checkoutMessage.value = ''
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

    if (!res.ok) {
      throw new Error(`Checkout failed: ${res.status}`)
    }

    const data = await res.json()
    checkoutMessage.value = `Order ${data.order_id} placed for ${checkoutItem.value.name}. Total $${(data.total / 100).toFixed(2)}`
    await loadOrders()
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
      headers: {
        Accept: 'application/json',
      },
    })

    if (!res.ok) {
      throw new Error(`Request failed with status ${res.status}`)
    }

    const data = await res.json()
    products.value = Array.isArray(data?.results) ? data.results : []
  } catch (err) {
    error.value = err?.message || 'Unable to load products.'
  } finally {
    loading.value = false
  }
}

const loadOrders = async () => {
  ordersLoading.value = true
  ordersError.value = ''
  try {
    const res = await fetch('http://localhost:8000/products/orders/', {
      headers: {
        Accept: 'application/json',
      },
    })

    if (!res.ok) {
      throw new Error(`Orders request failed: ${res.status}`)
    }

    const data = await res.json()
    orders.value = Array.isArray(data?.results) ? data.results : []
  } catch (err) {
    ordersError.value = err?.message || 'Unable to load orders.'
  } finally {
    ordersLoading.value = false
  }
}

const formatCurrency = (cents) => (cents / 100).toFixed(2)
const formatDate = (iso) => (iso ? new Date(iso).toLocaleString() : '')

onMounted(async () => {
  await loadProducts()
  await loadOrders()
})
</script>

<template>
  <div class="page">
    <header class="topbar">
      <div class="brand">LinhLan Shop</div>
      <div class="cart">
        <button class="link-btn" type="button" :class="{ active: activePage === 'products' }" @click="goToProducts">Products</button>
        <button class="link-btn" type="button" :class="{ active: activePage === 'orders' }" @click="goToOrders">Orders</button>
        <span class="cart-count">{{ cartCount }} items</span>
        <span class="cart-total">${{ cartTotal.toFixed(2) }}</span>
      </div>
    </header>

    <main>
      <template v-if="activePage === 'products'">
        <section class="hero">
          <div>
            <p class="eyebrow">New arrivals</p>
            <h1>Curated picks for everyday living</h1>
            <p class="lede">
              Explore a handful of products with clean design, quality materials, and prices that make sense.
            </p>
            <div class="actions">
              <button class="btn primary">Shop featured</button>
              <button class="btn ghost">View all</button>
            </div>
          </div>
          <div class="hero-card">
            <p class="muted">Fast shipping · 30-day returns</p>
            <p class="muted">Secure checkout · Chat support</p>
          </div>
        </section>

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
        <Products v-else :items="filtered" @add="addToCart" @instant-checkout="startCheckout" />

        <div v-if="checkoutMessage" class="status success">{{ checkoutMessage }}</div>
        <div v-else-if="checkoutError" class="status error">{{ checkoutError }}</div>
      </template>

      <template v-else-if="activePage === 'orders'">
        <Orders :orders="orders" :loading="ordersLoading" :error="ordersError" />
      </template>

      <div v-if="checkoutVisible" class="checkout-overlay">
        <div class="checkout-panel">
          <button class="close" type="button" @click="closeCheckout">×</button>
          <p class="eyebrow">Instant checkout</p>
          <h3>{{ checkoutItem?.name }}</h3>
          <p class="muted">${{ checkoutItem?.price.toFixed(2) }}</p>

          <div class="quantity">
            <button type="button" @click="decrementQty" :disabled="checkoutQty === 1">−</button>
            <span>{{ checkoutQty }}</span>
            <button type="button" @click="incrementQty">＋</button>
          </div>

          <p class="total">Total ${{ (checkoutItem?.price * checkoutQty).toFixed(2) }}</p>

          <button class="btn primary wide" type="button" :disabled="checkoutLoading" @click="instantCheckout">
            {{ checkoutLoading ? 'Processing…' : 'Place order' }}
          </button>

          <div v-if="checkoutError" class="status error">{{ checkoutError }}</div>
        </div>
      </div>
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

.link-btn.active {
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