import Vue from "vue"
import Vuex from "vuex"
import config from "@/config"
import api from "@/api"

Vue.use(Vuex)

function showSuccessToast(message) {
  Vue.toasted.show(message, { type: 'success' })
}

function showErrorToast(error, message) {
  Vue.toasted.show(`${message} (${error.response.status} ${error.response.statusText})`,
    { type: 'error' })
}

const store = new Vuex.Store({
  state: {
    token: localStorage.getItem('token'),
    currentUser: JSON.parse(localStorage.getItem('user')),
    users: [],
    points: [],
    sortFieldSel: 'name',
    sortDirectionSel: 'asc',
    mapUrl: 'https://{s}.tile.osm.org/{z}/{x}/{y}.png',
    mapAttribution: '&copy; <a href="https://osm.org/copyright">OpenStreetMap</a> contributors',
  },

  getters: {
    isAuthenticated: state => {
      /*
       * Check if the current user is authenticated or not.
       * parameters:
       *   - state: the store state object
       * returns:
       *   - boolean indicating if the user is authenticated or not
       */
      return state.token != null || state.currentUser != null
    }
  },

  mutations: {

    setToken(state, token) {
      /*
       * Save the JWT authentication token to the store and local storage.
       * parameters:
       *   - state: the store state object
       *   - token: the JWT token to save
       */
      state.token = token
      localStorage.setItem('token', token)
    },
    setCurrentUser(state, user) {
      /*
       * Save the current user details to the store and local storage.
       * parameters:
       *   - state: the store state object
       *   - user: the user information to save
       */
      state.currentUser = user
      const userInfo = JSON.stringify(user)
      localStorage.setItem('user', userInfo)
    },
    clearToken(state) {
      /*
       * Clear the JWT token from the store and local storage.
       * parameters:
       *   - state: the store state object
       */
      state.token = null
      localStorage.removeItem('token')
    },
    clearCurrentUser(state) {
      /*
       * Clear the current user details from the store and local storage.
       * parameters:
       *   - state: the store state object
       */
      state.currentUser = null
      localStorage.removeItem('user')
    },
    setUsers(state, users) {
      /*
       * Save the users list retrieved from the API to the store.
       * parameters:
       *   - state: the store state object
       *   - users: list of user objects to store
       */
      state.users = users
    },
    setPoints(state, points) {
      /*
       * Save the point list retrieved from the API to the store.
       * parameters:
       *   - state: the store state object
       *   - points: list of point objects to store
       */
      state.points = points
    },
    addPoint(state, point) {
      /*
       * Save a new point object to the store.
       * parameters:
       *   - state: the store state object
       *   - point: the point object to store
       */
      state.points.push(point)
    },
    updatePoint(state, point) {
      /*
       * Save changes made to a point object to the store.
       * parameters:
       *   - state: the store state object
       *   - point: the point object to modify in the store
       */
      state.points.push(point)
    },
    deletePoint(state, deletedPoint) {
      /*
       * Delete a point object from the store.
       * parameters:
       *   - state: the store state object
       *   - deletedPoint: the point object to delete from the store
       */
      state.points = state.points.filter(point => point.id !== deletedPoint.id)
    },
    updateSortFieldSel(state, sel) {
      /*
       * Update the current sort field selection ('created', 'name' or 'creator') in the store.
       * parameters:
       *   - state: the store state object
       *   - sel: the sort field selection to save to the store
       */
      state.sortFieldSel = sel
    },
    updateSortDirectionSel(state, sel) {
      /*
       * Update the current sort direction selection ('asc' or 'desc') in the store.
       * parameters:
       *   - state: the store state object
       *   - sel: the sort direction selection to save to the store
       */
      state.sortDirectionSel = sel
    },

  },
  actions: {

    login(context, data) {
      /*
       * Send the user credentials to the server to authenticate and login.
       * parameters:
       *   - context: context object for the store
       *   - data: the login request body data to send to the server
       * returns:
       *   - true if the login was successful, false otherwise
       */
      return api().post(config.API_URL + '/api-token-auth/', data)
        .then(response => {
          if (response.status === 200) {
            context.commit('setCurrentUser', response.data.user)
            context.commit('setToken', response.data.token)
            showSuccessToast('Logged in')
            return true
          }
        })
        .catch(error => {
          if (error.response && error.response.status === 400) {
            showErrorToast(error, 'Failed to login - invalid username or password')
          } else {
            Vue.toasted.show(`Failed to login (${error})`, { type: 'error' })
          }
          return false
        })
    },

    logout(context) {
      /*
       * Remove the token and user details from the store and local storage to logout.
       */
      context.commit('clearToken')
      context.commit('clearCurrentUser')
      showSuccessToast('Logged out')
    },

    register(context, data) {
      /*
       * Send new user details to the server to register/create a new user.
       * parameters:
       *   - context: context object for the store
       *   - data: the registration request body data to send to the server
       * returns:
       *   - true if the registration was successful, false otherwise
       */
      return api().post(config.API_URL + '/users/', data)
        .then(response => {
          if (response.status === 201) {
            showSuccessToast(`User \'${response.data.username}\' successfully registered. You may now login.`)
            return true
          }
        })
        .catch(error => {
          if (error.response == null) {
            showErrorToast(error, 'Failed to register user')
          } else {
            if (error.response.status === 400) {
              showErrorToast(error, 'Failed to register user - please enter a valid username and password')
            } else if (error.response.status === 409) {
              showErrorToast(error, 'Failed to register user - user with that username already exists')
            } else {
              showErrorToast(error, 'Failed to register user')
            }
          }

          return false;
        })
    },

    getUsers(context, params='') {
      /*
       * Get the list of users from the server.
       * parameters:
       *   - context: context object for the store
       *   - params: optional query parameters to send
       */
      api().get(config.API_URL + '/users/' + params)
        .then(response => response.data)
        .then(users => {
          context.commit('setUsers', users._items)
        })
        .catch(error => {
          showErrorToast(error, 'Failed to fetch users')
        })
    },

    getPoints(context, params='') {
      /*
       * Get the list of points from the server.
       * parameters:
       *   - context: context object for the store
       *   - params: optional query parameters to send
       */
      api().get(config.API_URL + '/points/' + params)
        .then(response => response.data)
        .then(points => {
          context.commit('setPoints', points._items)
        })
        .catch(error => {
          showErrorToast(error, 'Failed to fetch points')
        })
    },

    getPointDetails(context, point) {
      /*
       * Get the details of a single point from the server.
       * parameters:
       *   - context: context object for the store
       *   - point: point object to get details of (its _url is used for the request)
       * returns:
       *   - the details of the point object if successful, false otherwise
       */
      return api().get(point._url + '?expand=comments.creator')
        .then(response => {
           return response.data
        }).catch(error => {
          showErrorToast(error, 'Failed to get point details')
          return false
        })
    },

    addPoint(context, pointData) {
      /*
       * Send point details to the server to create a new point.
       * parameters:
       *   - context: context object for the store
       *   - pointData: the point request body data to send to the server
       * returns:
       *   - the created point object if the creation was successful, false otherwise
       */
      return api().post(config.API_URL + '/points/', pointData)
        .then(response => {
          let point = response.data
          api().get(point.creator).then(response => {
            point.creator = response.data
          })
          context.commit('addPoint', point)
          showSuccessToast(`Point \'${point.name}\' added successfully`)
          return point
        })
        .catch(error => {
          showErrorToast(error, 'Failed to add point')
          return false
        })
    },

    updatePoint(context, point) {
      /*
       * Send point details to the server to update a point.
       * parameters:
       *   - context: context object for the store
       *   - point: the point object request data to send to the server
       * returns:
       *   - the updated point object if the update was successful, false otherwise
       */
      return api().put(point._url, point)
        .then(response => {
          let point = response.data
          api().get(point.creator).then(creator => {
            point.creator = creator.data
          })
          context.commit('updatePoint', point)
          showSuccessToast(`Point \'${point.name}\' updated successfully`)
          return point
        })
        .catch(error => {
          console.log(error)
          showErrorToast(error, 'Failed to update point')
        })
    },

    deletePoint(context, point) {
      /*
       * Send a request to the server to delete a point.
       * parameters:
       *   - context: context object for the store
       *   - point: the point object to delete (its _url is used for the request)
       */
      api().delete(point._url)
        .then(response => {
          context.commit('deletePoint', point)
        })
        .then(showSuccessToast(`Point \'${point.name}\' deleted successfully`))
        .catch(error => {
          showErrorToast(error, 'Failed to delete point')
        })
    },

    addComment(context, payload) {
      /*
       * Send comment data to the server to create a new comment.
       * parameters:
       *   - context: context object for the store
       *   - payload: object containing the point's comment url and the comment content
       * returns:
       *   - the created comment object if the creation was successful, false otherwise
       */
      return api().post(payload.point.comments._url, payload.commentData)
        .then(response => {
          let comment = response.data
          api().get(comment.creator._url).then(creator => {
            comment.creator = creator.data
          })
          return comment
        })
        .catch(error => {
          console.log(error)
          showErrorToast(error, 'Failed to add comment')
          return false
        })
    },

    deleteComment(context, comment) {
      /*
       * Send a request to the server to delete a comment.
       * parameters:
       *   - context: context object for the store
       *   - comment: the comment object to delete (its _url attribute is used for the request)
       */
      api().delete(comment._url)
        .then(response => {})
        .then(showSuccessToast(`Comment deleted successfully`))
        .catch(error => {
          showErrorToast(error, 'Failed to delete comment')
        })
    },

  },
})

export default store
