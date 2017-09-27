import api from '../../api'
import * as types from '../mutationTypes'

export default {
  namespaced: true,
  state: {
    loading: false,
    editError: null,
    editSuccess: false,
    changePasswordError: null,
    changePasswordSuccess: false
  },
  mutations: {
    [types.SAVE_USER] (state) {
      state.loading = true
    },

    [types.SAVE_USER_SUCCESS] (state) {
      state.loading = false
      state.editError = null
      state.editSuccess = true
    },

    [types.SAVE_USER_FAILURE] (state, error) {
      state.loading = false
      state.editSuccess = false

      if (error)
        state.editError = error
      else
        state.editError = 'Unknown error saving'
    },

    [types.CHANGE_PASSWORD] (state) {
      state.loading = true
    },

    [types.CHANGE_PASSWORD_SUCCESS] (state) {
      state.loading = false
      state.changePasswordError = null
      state.changePasswordSuccess = true
    },

    [types.CHANGE_PASSWORD_ERROR] (state, error) {
      state.loading = false
      state.changePasswordSuccess = false

      if (error)
        state.changePasswordError = error
      else
        state.changePasswordError = 'Unknown error saving'
    }
  },
  actions: {
    save ({ commit }, user) {
      commit(types.SAVE_USER)
      api
        .put('/users/' + user.id, user)
        .then((res) => {
          if (res.status === 200) {
            commit(types.SAVE_USER_SUCCESS)
          } else {
            var error = null
            if (res.data && res.data.errors)
              error = res.data.errors
            commit(types.SAVE_USER_FAILURE, error)
          }
        })
        .catch((err) => {
          console.error(err)
          commit(types.SAVE_USER_FAILURE)
        })
    },

    changePassword ({ commit }, passwordChange) {
      commit(types.CHANGE_PASSWORD)
      api
        .put('/change-password', passwordChange)
        .then((res) => {
          if (res.status === 200) {
            commit(types.CHANGE_PASSWORD_SUCCESS)
          } else {
            var error = null
            if (res.data && res.data.errors)
              error = res.data.errors
            commit(types.CHANGE_PASSWORD_ERROR, error)
          }
        })
        .catch((err) => {
          console.error(err)
          commit(types.CHANGE_PASSWORD_ERROR)
        })
    }
  }
}
