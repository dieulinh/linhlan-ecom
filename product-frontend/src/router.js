import { createRouter, createWebHistory } from 'vue-router'
import ProductsPage from './views/ProductsPage.vue'
import OrdersPage from './views/OrdersPage.vue'
import ProductDetailPage from './views/ProductDetailPage.vue'
import OrderConfirmPage from './views/OrderConfirmPage.vue'

const routes = [
  { path: '/', name: 'products', component: ProductsPage },
  { path: '/orders', name: 'orders', component: OrdersPage },
  { path: '/product/:id', name: 'product-detail', component: ProductDetailPage, props: true },
  { path: '/order_confirmed', name: 'order-confirmed', component: OrderConfirmPage },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
