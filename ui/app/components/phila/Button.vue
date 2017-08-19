<template>
  <a class="button full-width" v-on:click="onClick()">
    <div class="valign">
      <div class="button-label valign-cell"><slot /></div>
    </div>
  </a>
</template>

<script>
  export default {
    name: 'phila-button',

    methods: {
      onClick (e) {
        this.$emit('click', e)
      }
    }
  }
</script>
