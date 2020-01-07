<template>
  <div class="col-4 mx-auto text-center">
    <h2 class="mt-5 mb-4">Login</h2>
    <b-form @submit="login">
      <b-form-group id="name-group" label="Username" label-for="name-input" class="text-left">
        <b-form-input id="name-input" placeholder="Enter username" type="text" v-model="username" required/>
      </b-form-group>
      <b-form-group id="pw-group" label="Password" label-for="pw-input" class="text-left">
        <b-form-input id="pw-input" placeholder="Enter password" type="password" v-model="password" required/>
      </b-form-group>
      <b-form-group>
        <b-button class="mt-3 px-5" type="submit" variant="primary" :disabled="waiting">Login</b-button>
      </b-form-group>
      <b-spinner v-if="waiting" variant="primary" label="Waiting"></b-spinner>
    </b-form>

    <div class="mt-4">
      <router-link :to="{ name: 'Register' }">
        Create account
      </router-link>
    </div>
  </div>
</template>

<script>
export default {
  // The user login view.
	name: 'Login',
	data() {
		return {
			username: '',
			password: '',
      waiting: false,
		}
	},
	methods: {
		login() {
      // Send the user details to the API for logging in when the login button is pressed.
			let loginData =  {
				username: this.username,
				password: this.password,
			}
      this.waiting = true
			this.$store.dispatch('login', loginData).then(() => {
				this.$router.push('/')
        this.waiting = false
			})
		}
	}
}
</script>

<style scoped>
</style>
