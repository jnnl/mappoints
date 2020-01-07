<template>
  <div class="col-4 mx-auto text-center">
    <h2 class="mt-5 mb-4">Register</h2>
    <b-form @submit="registerUser">
      <b-form-group id="name-group" label="Username" label-for="name-input" :invalid-feedback="invalidUsernameFeedback" class="text-left">
        <b-form-input id="name-input" placeholder="Enter username" type="text" :state="validUsername" v-model="username" required/>
      </b-form-group>
      <b-form-group id="location-group" label="Location (optional)" label-for="location-input" :invalid-feedback="invalidLocationFeedback" class="text-left">
        <b-form-input id="location-input" placeholder="Enter location" type="text" :state="validLocation" v-model="location"/>
      </b-form-group>
      <b-form-group id="pw-group" label="Password" label-for="pw-input" :invalid-feedback="invalidPasswordFeedback" class="text-left">
        <b-form-input id="pw-input" placeholder="Enter password" type="password" :state="validPassword" v-model="password" required/>
        <b-form-input id="pw-confirm-input" placeholder="Enter password again" type="password" :state="validPassword" v-model="passwordConfirm" class="mt-2" required/>
      </b-form-group>
      <b-form-group>
        <b-button class="mt-3 px-5" type="submit" variant="primary" :disabled="waiting">Register</b-button>
      </b-form-group>
      <b-spinner v-if="waiting" variant="primary" label="Waiting"></b-spinner>
    </b-form>
    <router-link :to="{ name: 'Login' }">
      I already have an account
    </router-link>
  </div>
</template>

<script>
export default {
  // The new user registration view.
  name: 'Register',
  data() {
    return {
      username: '',
      location: '',
      password: '',
      passwordConfirm: '',
      waiting: false
    }
  },
	computed: {
		validUsername() {
      /*
       * Check if the username is valid.
       * returns:
       *   - boolean indicating if the username is valid or not
       */
			return this.username.length >= 4 && /^[a-zåäö0-9_]+$/i.test(this.username)
		},
		validLocation() {
      /*
       * Check if the location string is valid.
       * returns:
       *   - boolean indicating if the location is valid or not
       */
			return this.location.length <= 100
		},
		validPassword() {
      /*
       * Check if the password string is valid.
       * returns:
       *   - boolean indicating if the password is valid or not
       */
			return this.password.length >= 8 && this.password === this.passwordConfirm
		},
		invalidUsernameFeedback() {
      /*
       * Determine and show error message when the username field is invalid.
       * returns:
       *   - error string indicating how the username is invalid
       */
			if (this.username.length < 4) {
				return 'Username must be at least 4 characters long.'
			} else if (!/^[a-zA-Z0-9_]+$/.test(this.username)) {
				return 'Username may only contain alphabets, numbers and numberscores'
			} else {
				return ''
			}
		},
		invalidLocationFeedback() {
      /*
       * Determine and show error message when the location field is invalid.
       * returns:
       *   - error string indicating how the location is invalid
       */
			if (this.location.length > 100) {
				return 'Location can be at most 100 characters long.'
			} else {
				return ''
			}
		},
		invalidPasswordFeedback() {
      /*
       * Determine and show error message when the password field is invalid.
       * returns:
       *   - error string indicating how the password is invalid
       */
			if (this.password.length < 8) {
				return 'Password must be at least 8 characters long.'
			} else if (this.password !== this.passwordConfirm) {
				return 'Passwords don\'t match.'
			} else {
				return ''
			}
		},
	},
  methods: {
    registerUser() {
      // Send the user details to register to the API and return to the login page
      // when the register button is pressed.
      let registerData = {
        username: this.username,
        location: this.location,
        password: this.password,
      }
      this.waiting = true
      this.$store.dispatch('register', registerData).then((status) => {
        this.waiting = false
        if (status === true) {
          this.$router.push('/login')
        }
      })
    }
  }
}
</script>
