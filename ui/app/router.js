import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

import LoginContainer from './containers/LoginContainer.vue'
import RegistrationContainer from './containers/RegistrationContainer.vue'

const routes = [
  { path: '/login', component: LoginContainer },
  { path: '/registration', component: RegistrationContainer }
]

const router = new VueRouter({
  mode: 'history',
  routes
})

export default router
