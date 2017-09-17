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
    [types.SUBMIT_REGISTRATION] (state) {
      state.loading = true
    },

    [types.RECEIVE_REGISTRATION_SUCCESS] (state) {
      state.loading = false
      state.error = null
      state.success = true
    },

    [types.RECEIVE_REGISTRATION_FAILURE] (state, error) {
      state.loading = false
      state.success = false

      if (error)
        state.error = error
      else
        state.error = 'Unknown error processing your registration'
    }
  },
  actions: {
    submitRegistration ({ commit }, registration) {
      commit(types.SUBMIT_REGISTRATION)
      api
        .post('/registrations', registration)
        .then((res) => {
          if (res.status === 204) {
            commit(types.RECEIVE_REGISTRATION_SUCCESS)
          } else {
            var error = null
            if (res.data && res.data.errors)
              error = res.data.errors
            commit(types.RECEIVE_REGISTRATION_FAILURE, error)
          }
        })
        .catch((err) => {
          console.error(err)
          commit(types.RECEIVE_REGISTRATION_FAILURE)
        })
    }
  }
}
