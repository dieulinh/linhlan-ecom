import { createRouter, createWebHistory } from 'vue-router'
import ProductsPage from './views/ProductsPage.vue'
import OrdersPage from './views/OrdersPage.vue'
import ProductDetailPage from './views/ProductDetailPage.vue'

const routes = [
  { path: '/', name: 'products', component: ProductsPage },
  { path: '/orders', name: 'orders', component: OrdersPage },
  { path: '/product/:id', name: 'product-detail', component: ProductDetailPage, props: true },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
