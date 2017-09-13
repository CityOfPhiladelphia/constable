<template>
  <div
    v-if="success || error || warn"
    role="alert"
    class="alert"
    :class="{'alert-success': success, 'alert-error': error, 'alert-warn': warn}">
    <div
      class="fa"
      :class="{'fa-check': success, 'fa-times': error, 'fa-exclamation': warn}"
      aria-hidden="true"></div>
    <div class="alert-message">
      <slot/> {{ message }}
    </div>
  </div>
</template>

<script>
  export default {
    name: 'phila-alert',

    props: {
      success: {
        default: false
      },
      error: {
        default: false
      },
      warn: {
        default: false
      },
      message: {
        type: String
      }
    }
  }
</script>

<style lang="css">
  .alert {
    padding: 1.25rem;
    margin: .5rem 0;
    width: 100%;
    display: table;
  }

  .alert-message {
    text-align: center;
    vertical-align: middle;
  }

  .alert .fa {
    font-size: 3rem;
    vertical-align: middle;
    width: 6rem;
  }

  .alert div, .alert span {
    display: table-cell;
    text-align: center;
  }

  .alert-success {
    color: #3a833c;
    background-color: #b9f2b1;
  }

  .alert-error {
    color: #cc3000;
    background: #fed0d0;
  }

  .alert-warn {
    background: #ffefa2;
  }
</style>
