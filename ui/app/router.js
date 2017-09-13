import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

import LoginContainer from './containers/LoginContainer.vue'
import RegistrationContainer from './containers/RegistrationContainer.vue'
import PasswordRecoveryContainer from './containers/PasswordRecoveryContainer.vue'

const routes = [
  { path: '/login', component: LoginContainer, meta: { title: 'Login' } },
  { path: '/registration', component: RegistrationContainer, meta: { title: 'Registration' } },
  { path: '/password-recovery', component: PasswordRecoveryContainer, meta: { title: 'Password Recovery' } }
]

const router = new VueRouter({
  mode: 'history',
  routes
})

router.beforeEach((to, from, next) => {
  document.title = to.meta.title + ' - City of Philadelphia'
  next()
})

export default router
