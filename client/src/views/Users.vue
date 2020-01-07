<template>
  <div class="row">
    <div class="users col-6 mt-3">
      <h4>Users</h4>
      <div class="user-search my-3">
        <b-input-group>
          <b-form-input v-model="filter" placeholder="Enter name" />
            <b-input-group-append>
              <b-button :disabled="!filter" @click="filter = ''">Clear</b-button>
            </b-input-group-append>
          </b-input-group>
      </div>
      <b-table hover show-empty
       :items="items"
       :fields="fields"
       :current-page="currentPage"
       :per-page="perPage"
       :filter="filter"
       @filtered="onFiltered"
       class="user-table">
        <template slot="actions" slot-scope="row">
          <b-button :to="{ name: 'Points', query: { user: '@' + row.item.username } }" size="sm" variant="primary" class="mr-2" :disabled="row.item.points.length == 0">
            Show points
          </b-button>
        </template>
      </b-table>
    </div>
  </div>
</template>

<script>
import { mapState } from "vuex"

export default {
  // The users view displaying all users in the system.
  name: "Users",
  props: {
    user: {
      default: null,
      type: String
    }
  },
  data() {
    return {
      fields: [
        {
          key: "username",
          sortable: true,
          sortDirection: 'desc',
        },
        {
          key: "location",
          label: "Location",
          sortable: true,
          sortDirection: 'desc',
        },
        {
          key: "points._items.length",
          label: "Points",
          sortable: true,
          sortDirection: 'desc',
        },
        {
          key: "comments._items.length",
          label: "Comments",
          sortable: true,
          sortDirection: 'desc',
        },
        {
          key: "stars._items.length",
          label: "Stars",
          sortable: true,
          sortDirection: 'desc',
        },
        {
          key: "actions",
          class: 'actions',
        }
      ],
      currentPage: 1,
      perPage: 10,
      filter: this.user,
      totalRows: null,
    }
  },
  mounted() {
    // Send a request to get the users from the API.
    this.$store.dispatch('getUsers')
  },
  computed: {
    ...mapState([
      "users"
    ]),
    items () {
      /*
       * Get the users that match the filter input field's value.
       * returns:
       *   - list of users matched by the filter field
       */
      if (this.filter) {
        if (this.filter.indexOf('@') === 0) {
          return this.users.filter(user => user.username == this.filter.substring(1))
        } else {
          return this.users.filter(user => user.username.includes(this.filter))
        }
      } else {
        return this.users
      }
    }
  },
  methods: {
    onFiltered(filteredItems) {
      // Set total rows and current page number when the users table is filtered.
      this.totalRows = filteredItems.length
      this.currentPage = 1
    }
  }
}
</script>
<style>
.actions {
  width: 200px;
  max-width: 200px;
}
</style>
