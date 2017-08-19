<template>
  <div>
    <label for="username">Username</label>
    <span v-show="errors.has('username')" role="alert">{{ errors.first('username') }}</span>
    <input
      type="text"
      id="username"
      name="username"
      v-model="username"
      v-validate="'required'"
      v-on:keyup.enter="validateAndSubmit()"
      v-bind:class="{ 'input-error': errors.has('username') }">

    <label for="password">Password</label>
    <span v-show="errors.has('password')" role="alert">{{ errors.first('password') }}</span>
    <input
      type="password"
      id="password"
      name="password"
      v-model="password"
      v-validate="'required'"
      v-on:keyup.enter="validateAndSubmit()"
      v-bind:class="{ 'input-error': errors.has('password') }">

    <a class="button full-width" v-on:click="validateAndSubmit()">
      <div class="valign">
        <div class="button-label valign-cell">Submit</div>
      </div>
    </a>

    <div class="login-error" v-if="error">
      {{ error }}
    </div>
  </div>
</template>

<script>
  export default {
    props: {
      onSubmit: {
        type: Function,
        required: true
      }
    },
    data () {
      return {
        username: null,
        password: null
      }
    },
    computed: {
      error () {
        return this.$store.state.login.error // TODO: component accessing state. Should this be a prop?
      }
    },
    methods: {
      validateAndSubmit () {
        this.$validator.validateAll()
        .then((valid) => {
          if (valid)
            this.onSubmit({
              username: this.username,
              password: this.password
            })
        })
      }
    }
  }
</script>

<style lang="css">
  .login-error {
    background: #fed0d0;
    padding: 1em;
    margin: .5em 0;
    text-align: center;
  }

  .input-error {
    border: 2px solid #fed0d0;
  }
</style>