import Vue from 'vue'
import Vuex from 'vuex'

import login from './modules/login'
import registration from './modules/registration'
import passwordRecovery from './modules/passwordRecovery'
import user from './modules/user'

Vue.use(Vuex)

const debug = (process.env.NODE_ENV !== 'production')

const store = new Vuex.Store({
  modules: {
    login,
    registration,
    passwordRecovery,
    user
  },
  strict: debug
})

export default store
