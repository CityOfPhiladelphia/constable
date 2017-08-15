import Vue from 'vue'
import Vuex from 'vuex'

import * as actions from './actions'
import * as getters from './getters'
import mutations from './mutations'

Vue.use(Vuex)

const debug = (process.env.NODE_ENV !== 'production')

const store = new Vuex.Store({
  state: {
    loading: false,
    login: {
      error: false
    }
  },
  actions,
  mutations,
  //getters,
  strict: debug
})

export default store
