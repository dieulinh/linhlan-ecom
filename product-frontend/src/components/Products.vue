<script setup>
import { computed } from 'vue'

const props = defineProps({
  items: {
    type: Array,
    default: () => [],
  },
})

const emit = defineEmits(['add', 'instant-checkout', 'view'])

const hasResults = computed(() => props.items && props.items.length > 0)

const handleAdd = (item) => {
  emit('add', item)
}
const handleInstantCheckout = (item) => {
  // For simplicity, just add to cart for now
  emit('instant-checkout', item)
}
const handleView = (item) => {
  emit('view', item)
}
</script>

<template>
  <section class="products">
    <header class="section-head">
      <div>
        <p class="eyebrow">Catalog</p>
        <h2>Products</h2>
      </div>
      <p class="muted">{{ props.items.length }} items</p>
    </header>

    <div v-if="hasResults" class="grid">
      <article v-for="item in props.items" :key="item.id" class="card" @click="handleView(item)">
        <div class="image" :style="{ backgroundImage: `url(${item.image_url})` }">
          <span class="pill">{{ item.category || 'General' }}</span>
        </div>
        <div class="content">
          <div class="title-row">
            <h3>{{ item.name }}</h3>
            <span class="price">${{ item.price.toFixed(2) }}</span>
          </div>
          <p class="muted">{{ item.description || 'No description provided.' }}</p>
          <div class="meta">
            <span class="rating">★ {{ item.rating ?? '—' }}</span>
            <div class="actions">
              <button class="add ghost" type="button" @click="handleAdd(item)">Add to cart</button>
              <button class="add" type="button" @click="handleInstantCheckout(item)">Buy now</button>
            </div>
          </div>
        </div>
      </article>
    </div>

    <div v-else class="empty">
      <p>No products match your filters. Try clearing search or choosing another category.</p>
    </div>
  </section>
</template>

<style scoped>
.products {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.section-head {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 10px;
}

.section-head h2 {
  margin: 2px 0 0;
  font-size: 22px;
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
  margin: 0;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 16px;
}

.card {
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 14px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  box-shadow: 0 10px 28px rgba(15, 23, 42, 0.06);
  transition: transform 120ms ease, box-shadow 160ms ease;
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 16px 34px rgba(15, 23, 42, 0.12);
}

.image {
  position: relative;
  padding-top: 62%;
  background-size: cover;
  background-position: center;
}

.pill {
  position: absolute;
  top: 12px;
  left: 12px;
  padding: 6px 10px;
  border-radius: 999px;
  background: rgba(15, 23, 42, 0.78);
  color: #fff;
  font-size: 12px;
  font-weight: 600;
}

.content {
  padding: 14px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  flex: 1;
}

.title-row {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  gap: 10px;
}

h3 {
  margin: 0;
  font-size: 16px;
}

.price {
  font-weight: 700;
  color: #0f172a;
}

.meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: auto;
}

.rating {
  font-weight: 700;
  color: #f59e0b;
}

.actions {
  display: flex;
  gap: 8px;
}

.add {
  border: 1px solid #2563eb;
  background: #2563eb;
  color: #fff;
  border-radius: 10px;
  padding: 8px 12px;
  font-weight: 600;
  cursor: pointer;
  transition: background 120ms ease, transform 120ms ease;
}

.add.ghost {
  background: #fff;
  color: #2563eb;
}

.add:hover {
  background: #1d4ed8;
  transform: translateY(-1px);
}

.empty {
  padding: 24px;
  text-align: center;
  border: 1px dashed #cbd5e1;
  border-radius: 12px;
  color: #475569;
  background: #fff;
}
</style>