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
    [types.SUBMIT_PASSWORD_RECOVERY] (state) {
      state.loading = true
    },

    [types.RECEIVE_PASSWORD_RECOVERY_SUCCESS] (state) {
      state.loading = false
      state.error = null
      state.success = true
    },

    [types.RECEIVE_PASSWORD_RECOVERY_FAILURE] (state, error) {
      state.loading = false
      state.success = false

      if (error)
        state.error = error
      else
        state.error = 'Unknown error'
    }
  },
  actions: {
    submit ({ commit }, passwordRecovery) {
      commit(types.SUBMIT_PASSWORD_RECOVERY)
      api
        .post('/password-recoveries', passwordRecovery)
        .then((res) => {
          if (res.status === 204) {
            commit(types.RECEIVE_PASSWORD_RECOVERY_SUCCESS)
          } else {
            var error = null
            if (res.data.errors)
              error = res.data.errors
            commit(types.RECEIVE_PASSWORD_RECOVERY_FAILURE, error)
          }
        })
        .catch((err) => {
          console.error(err)
          commit(types.RECEIVE_PASSWORD_RECOVERY_FAILURE)
        })
    }
  }
}
