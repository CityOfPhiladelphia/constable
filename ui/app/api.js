import axios from 'axios'

export default axios.create({
  baseURL: 'http://localhost:5000',
  timeout: 10000,
  withCredentials: true,
  validateStatus: function (status) {
    return status >= 200 && status < 500;
  }
});
