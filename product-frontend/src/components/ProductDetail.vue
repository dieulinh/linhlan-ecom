<script setup>
const props = defineProps({
  product: {
    type: Object,
    default: null,
  },
  loading: {
    type: Boolean,
    default: false,
  },
  error: {
    type: String,
    default: '',
  },
})

const emit = defineEmits(['back', 'buy', 'add'])

const handleBuy = () => {
  if (props.product) emit('buy', props.product)
}

const handleAdd = () => {
  if (props.product) emit('add', props.product)
}
</script>

<template>
  <section class="detail">
    <button class="link-btn" type="button" @click="emit('back')">← Back to products</button>

    <div v-if="loading" class="status">Loading product…</div>
    <div v-else-if="error" class="status error">{{ error }}</div>
    <div v-else-if="!product" class="status">No product found.</div>
    <div v-else class="layout">
      <div class="hero" :style="{ backgroundImage: `url(${product.image_url})` }"></div>
      <div class="info">
        <p class="eyebrow">Product</p>
        <h1>{{ product.name }}</h1>
        <p class="price">${{ product.price.toFixed(2) }}</p>
        <p class="muted">Handle: {{ product.handle }}</p>
        <p class="muted">Stock: {{ product.stock }}</p>
        <button class="btn primary" type="button" @click="handleAdd">Add to cart</button>
        <button class="btn primary" type="button" @click="handleBuy">Buy now</button>
      </div>
    </div>

    <div v-if="product?.recommendations?.length" class="recommend">
      <h3>Recommended for you</h3>
      <div class="rec-grid">
        <article v-for="rec in product.recommendations" :key="rec.id" class="rec-card">
          <div class="thumb" :style="{ backgroundImage: `url(${rec.image_url})` }"></div>
          <div>
            <p class="name">{{ rec.name }}</p>
            <p class="muted">${{ rec.price.toFixed(2) }}</p>
          </div>
        </article>
      </div>
    </div>
  </section>
</template>

<style scoped>
.detail {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.layout {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 18px;
  align-items: center;
}

.hero {
  width: 100%;
  padding-top: 70%;
  border-radius: 16px;
  background-size: cover;
  background-position: center;
  border: 1px solid #e2e8f0;
  box-shadow: 0 12px 30px rgba(15, 23, 42, 0.08);
}

.info h1 {
  margin: 0;
}

.price {
  font-size: 24px;
  font-weight: 800;
  margin: 6px 0;
}

.btn.primary {
  border: 1px solid transparent;
  border-radius: 10px;
  padding: 12px 14px;
  background: #2563eb;
  color: #fff;
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 10px 24px rgba(37, 99, 235, 0.25);
}

.recommend {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.rec-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 12px;
}

.rec-card {
  display: grid;
  grid-template-columns: 64px 1fr;
  gap: 10px;
  align-items: center;
  padding: 10px;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  background: #fff;
}

.thumb {
  width: 64px;
  height: 64px;
  border-radius: 10px;
  background-size: cover;
  background-position: center;
  border: 1px solid #e2e8f0;
}

.name {
  margin: 0;
  font-weight: 700;
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
</style>
