import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

import LoginContainer from './containers/LoginContainer.vue'

const routes = [
  { path: '/login', component: LoginContainer }
]

const router = new VueRouter({
  mode: 'history',
  routes
})

export default router
