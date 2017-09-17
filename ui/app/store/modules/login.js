import api from '../../api'
import * as types from '../mutationTypes'

export default {
  namespaced: true,
  state: {
    loading: false,
    error: null,
    success: false
  },
  mutations: {
    [types.SUBMIT_LOGIN] (state) {
      state.loading = true
    },

    [types.RECEIVE_LOGIN_SUCCESS] (state) {
      state.loading = false
      state.error = null
      state.success = true

      // TODO: check for redirect in query param
      // TODO: verify redirect host is a registered app?
      // TODO: ^ should the above just be cominbined into a server route?
    },

    [types.RECEIVE_LOGIN_FAILURE] (state, error) {
      state.loading = false
      state.success = false

      if (error && error.status) {
        if (error.status == 401)
          state.error = 'Incorrect email or password'
        else
          state.error = error.message || 'Unknown error'
      } else
        state.error = 'Unknown error'
    }
  },
  actions: {
    submitLogin ({ commit }, login) {
      commit(types.SUBMIT_LOGIN)
      api
        .post('/session', login)
        .then((res) => {
          if (res.status === 201) {
            commit(types.RECEIVE_LOGIN_SUCCESS)
          } else {
            var error = null
            if (res.data.errors)
              error = res.data.errors[0]
            commit(types.RECEIVE_LOGIN_FAILURE, {
              status: res.status,
              message: error
            })
          }
        })
        .catch((err) => {
          console.error(err)
          commit(types.RECEIVE_LOGIN_FAILURE)
        })
    }
  }
}
