import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

import LoginContainer from './containers/LoginContainer.vue'
import RegistrationContainer from './containers/RegistrationContainer.vue'

const routes = [
  { path: '/login', component: LoginContainer, meta: { title: 'Login' } },
  { path: '/registration', component: RegistrationContainer, meta: { title: 'Registration' } }
]

const router = new VueRouter({
  mode: 'history',
  routes
})

router.beforeEach((to, from, next) => {
  document.title = to.meta.title
  next()
})

export default router
