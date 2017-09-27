<template>
  <div>
    <div class="row">
      <div class="columns medium-8">
        <h3 class="contrast">Edit Profile</h3>
        <phila-alert :error="editError">{{ editError }}</phila-alert>
        <user-form v-if="!editSuccess" :onSave="save"></user-form>
      </div>
    </div>
    <div class="row">
      <div class="columns medium-8">
        <h3 class="contrast">Change Password</h3>
        <phila-alert :error="changePasswordError">{{ changePasswordError }}</phila-alert>
        <change-password-form v-if="!changePasswordSuccess" :onChangePassword="changePassword"></change-password-form>
      </div>
    </div>
  </div>
</template>

<script>
  import { mapState, mapActions } from 'vuex'

  import PhilaAlert from '../components/phila/PhilaAlert.vue'
  import UserForm from '../components/UserForm.vue'
  import ChangePasswordForm from '../components/ChangePasswordForm.vue'

  export default {
    components: {
      PhilaAlert,
      UserForm,
      ChangePasswordForm
    },
    computed: mapState('user', {
      editError: state => state.editError,
      editSuccess: state => state.editSuccess,
      changePasswordError: state => state.changePasswordError,
      changePasswordSuccess: state => state.changePasswordSuccess
    }),
    methods: mapActions('user', [
      'save',
      'changePassword'
    ])
  }
</script>

<style lang="css">
  .row {
    margin-top: 1rem;
    margin-bottom: 1rem;
  }
</style>