<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import Products from './components/Products.vue'

const products = ref([])
const loading = ref(true)
const error = ref('')

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

onMounted(loadProducts)
</script>

<template>
  <div class="page">
    <header class="topbar">
      <div class="brand">LinhLan Shop</div>
      <div class="cart">
        <span class="cart-count">{{ cartCount }} items</span>
        <span class="cart-total">${{ cartTotal.toFixed(2) }}</span>
      </div>
    </header>

    <main>
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
      <Products v-else :items="filtered" @add="addToCart" />
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
  transition: transform 120ms ease, box-shadow 160ms ease, background 160ms ease;
}

.btn.primary {
  background: #2563eb;
  color: #fff;
  box-shadow: 0 10px 24px rgba(37, 99, 235, 0.25);
}

.btn.ghost {
  background: #fff;
  border-color: #e2e8f0;
  color: #0f172a;
}

.btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 12px 26px rgba(15, 23, 42, 0.08);
}

.hero-card {
  align-self: center;
  padding: 18px;
  border: 1px dashed #cbd5e1;
  border-radius: 14px;
  background: #fff;
  color: #475569;
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