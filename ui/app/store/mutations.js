import * as types from './mutationTypes'

export default {
  [types.RECEIVE_LOGIN_SUCCESS] (state) {
    state.loading = false
  },

  [types.RECEIVE_LOGIN_FAILURE] (state, error) {
    state.loading = false
    if (error[0]) {
      error = error[0]
      if (error == 'Not Authorized')
        state.login.error = 'Wrong username or password.'
      else if (error == 'Too Many Login Attempts')
        state.login.error = 'Too many failed attempts logging in. Please try again in 15 minutes.'
      else if (error == 'Maximum number of user sessions reached.')
        state.login.error = 'You are logged in from too many browsers.'
      else
        state.login.error = 'Unknown error login error'
    } else {
      state.login.error = 'Username and password required.'
    }
  }
}
