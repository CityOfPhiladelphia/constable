import axios from 'axios'

import * as types from './mutationTypes'

var api = axios.create({
  baseURL: 'http://localhost:5000',
  timeout: 5000,
  withCredentials: true,
  validateStatus: function (status) {
    return status >= 200 && status < 500;
  }
});

export const submitLogin = ({ commit }, login) => {
  api
  .post('/session', login)
  .then((res) => {
    if (res.status === 201) {
      commit(types.RECEIVE_LOGIN_SUCCESS)
    } else {
      var error = null
      if (res.data.errors)
        error = res.data.errors
      commit(types.RECEIVE_LOGIN_FAILURE, error)
    }
  })
  .catch((err) => console.log(err)) // TODO: global error handler?
}
