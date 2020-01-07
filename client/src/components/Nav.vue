<template>
    <nav id="main-nav" class="navbar navbar-expand-sm navbar-dark bg-dark">
      <router-link class="navbar-brand" :to="{ name: 'Home' }">MapPoints</router-link>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarContent">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div v-if="isAuthenticated" class="collapse navbar-collapse" id="navbarContent">
        <ul class="navbar-nav mr-auto">
          <li class="nav-item">
            <router-link :to="{ name: 'Points' }" class="nav-link"><span class="fas fa-fw fa-map-marker-alt mr-1"></span>
              Points</router-link>
          </li>
          <li class="nav-item">
            <router-link :to="{ name: 'Users' }" class="nav-link"><span class="fas fa-fw fa-user-alt mr-1"></span>
              Users</router-link>
          </li>
        </ul>
        <div v-if="isAuthenticated" class="dropdown show my-2 my-lg-0">
          <a class="dropdown-toggle nav-user-dropdown" href="#" role="button" id="dropdownMenuLink" data-toggle="dropdown">
            <span class="fas fa-fw fa-user-circle mr-2"></span>{{ currentUser.username }}
          </a>
          <div class="dropdown-menu dropdown-menu-right user-menu">
            <router-link class="dropdown-item" :to="{ name: 'Points', query: { user: '@' + currentUser.username } }" href="#/points">My Points</router-link>
            <div class="dropdown-divider"></div>
            <a class="dropdown-item" target="_blank" href="https://gitlab.com/jnnl/pwp-mappoints">About</a>
            <div class="dropdown-divider"></div>
            <a class="dropdown-item" style="cursor: pointer" @click="logout">Log out</a>
          </div>
        </div>
      </div>
    </nav>
</template>

<script>
import { mapState } from "vuex"
export default {
  name: "Nav",
  computed: {
    ...mapState([
      "currentUser"
    ]),
    isAuthenticated() {
      /*
       * Get the current user's authentication status.
       * returns:
       *   - boolean stating if the current user is authenticated or not
       */
      return this.$store.getters.isAuthenticated
    }
  },
  methods: {
    logout() {
      // Log the user out and return to the login page.
      this.$store.dispatch('logout')
      this.$router.push('/login')
    }
  }
}
</script>

<style>
#main-nav {
  margin: 0px -15px;
}

.nav-user-dropdown {
  color: rgba(255, 255, 255, 0.5);
  text-decoration: none;
}

.nav-user-dropdown:hover {
  text-decoration: none;
  color: rgba(255, 255, 255, 0.75);
}

.nav-user-dropdown:focus {
  color: rgba(255, 255, 255, 0.75);
}

@media only screen and (max-width: 575px) {
  .user-menu {
    left: 0 !important;
    right: auto !important;
  }
}
</style>
