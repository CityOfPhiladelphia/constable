<template>
  <component
    class="button full-width"
    :is="href ? 'a' : 'button'"
    :href="href"
    :disabled="disabled"
    @click="onClick">
    <div class="valign">
      <div class="button-label valign-cell"><slot/></div>
    </div>
  </component>
</template>

<script>
  export default {
    name: 'phila-button',

    props: {
      href: {
        type: String
      },
      disabled: {
        type: Boolean,
        default: false
      }
    },

    methods: {
      onClick (e) {
        this.$emit('click', e)
      }
    }
  }
</script>

<style lang="css">
  .button {
    padding: .2rem;
    margin: .5rem 0;
  }
</style>
