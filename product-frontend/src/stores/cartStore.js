import { computed, reactive } from 'vue'

// Minimal global cart store using Vue reactivity (no Vuex)
const state = reactive({
  items: new Map(), // id -> { qty, price }
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

const addToCart = (product) => {
  if (!product || typeof product.id === 'undefined') return
  const current = state.items.get(product.id) || { qty: 0, price: product.price || 0 }
  state.items.set(product.id, {
    qty: current.qty + 1,
    price: product.price ?? current.price ?? 0,
  })
}

export const useCartStore = () => ({
  state,
  cartCount,
  cartTotal,
  addToCart,
})
