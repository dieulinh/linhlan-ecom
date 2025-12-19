import { computed, reactive } from 'vue'

// Minimal global cart store using Vue reactivity (no Vuex)
const state = reactive({
  items: new Map(), // id -> { qty, price, name, image_url }
})

const cartCount = computed(() => {
  let total = 0
  state.items.forEach((entry) => {
    total += entry.qty || 0
  })
  return total
})

const cartTotal = computed(() => {
  let total = 0
  state.items.forEach((entry) => {
    total += (entry.qty || 0) * (entry.price || 0)
  })
  return total
})

const cartItems = computed(() => {
  return Array.from(state.items.entries()).map(([id, entry]) => ({
    id,
    qty: entry.qty || 0,
    price: entry.price || 0,
    name: entry.name || 'Item',
    image_url: entry.image_url || '',
    lineTotal: (entry.qty || 0) * (entry.price || 0),
  }))
})

const addToCart = (product) => {
  if (!product || typeof product.id === 'undefined') return
  const current = state.items.get(product.id) || {
    qty: 0,
    price: product.price || 0,
    name: product.name || 'Item',
    image_url: product.image_url || '',
  }
  state.items.set(product.id, {
    qty: current.qty + 1,
    price: product.price ?? current.price ?? 0,
    name: product.name ?? current.name,
    image_url: product.image_url ?? current.image_url,
  })
}

const setQuantity = (id, quantity) => {
  if (typeof id === 'undefined') return
  const numericQty = Math.max(0, Number(quantity) || 0)
  const existing = state.items.get(id)
  if (!existing) return
  if (numericQty === 0) {
    state.items.delete(id)
    return
  }
  state.items.set(id, { ...existing, qty: numericQty })
}

const increment = (id) => {
  const existing = state.items.get(id)
  if (!existing) return
  setQuantity(id, (existing.qty || 0) + 1)
}

const decrement = (id) => {
  const existing = state.items.get(id)
  if (!existing) return
  setQuantity(id, (existing.qty || 0) - 1)
}

const removeItem = (id) => {
  if (state.items.has(id)) state.items.delete(id)
}

export const useCartStore = () => ({
  state,
  cartCount,
  cartTotal,
  cartItems,
  addToCart,
  setQuantity,
  increment,
  decrement,
  removeItem,
})
