import Vue from 'vue'
import VeeValidate from 'vee-validate'

import store from './store'
import router from './router'

Vue.use(VeeValidate);

new Vue({
  el: '#app',
  store,
  router
});
