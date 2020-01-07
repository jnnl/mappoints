<template>
  <div class="point">
    <div class="row">
      <div class="col point-details">
        <b-form @submit="createPoint">
          <div class="d-flex justify-content-between align-items-center mt-3">
            <template v-if="pointMode === 'create'">
              <h4>Create a Point</h4>
              <b-button size="sm" type="submit" variant="primary" class="mr-1">
                <span class="fas fa-plus mr-1"></span>
                Create Point
              </b-button>
            </template>
            <template v-else>
              <h4 style="word-wrap: anywhere">{{ point.name }}</h4>
              <b-button v-if="pointMode === 'edit'"
                @click="updatePoint" size="sm" type="submit" variant="primary" class="mr-1">
                <span class="fas fa-save mr-1"></span>
                Save Changes
              </b-button>
            </template>
          </div>

          <template v-if="isEditable">
            <b-form-group
              id="point-name"
              label="Name"
              label-for="name-input">
              <b-form-input id="name-input" placeholder="Enter name"
                v-model="point.name" trim required/>
            </b-form-group>

            <b-form-group
              id="point-latitude"
              label="Latitude"
              label-for="latitude-input">
              <b-input-group>
                <b-form-input id="latitude-input" placeholder="Enter latitude"
                  type="number" min="0" max="90" step="0.000001"
                  @input="setLatitude" :value="displayLatitude" trim required/>
                <b-input-group-append>
                  <b-form-select v-model="latitudeSel"
                    @change="swapLatitude" :options="latitudeOptions" />
                </b-input-group-append>
              </b-input-group>
            </b-form-group>

            <b-form-group
              id="point-longitude"
              label="Longitude"
              label-for="longitude-input">
              <b-input-group>
                <b-form-input id="longitude-input" placeholder="Enter longitude"
                  type="number" min="0" max="180" step="0.000001"
                  @input="setLongitude" :value="displayLongitude" trim required/>
                <b-input-group-append>
                  <b-form-select v-model="longitudeSel"
                    @change="swapLongitude" :options="longitudeOptions" />
                </b-input-group-append>
              </b-input-group>
            </b-form-group>

            <b-form-group
              id="point-description"
              label="Description"
              label-for="description-input">
              <b-form-textarea
                id="description-input"
                v-model="point.description"
                placeholder="Enter description"
                rows="5"
                max-rows="10"
              />
            </b-form-group>
          </template>
          <template v-else>
            <b>{{ pointToCoordinates(point) }}</b>
            <div class="mt-3 font-weight-bold">Description:</div>
            <div class="mb-3">{{ point.description }}</div>
          </template>

          <template v-if="pointMode !== 'create'">
            <div class="font-weight-bold mt-3 mb-1">Comments ({{ point.comments._items && point.comments._items.length }}):</div>
            <div class="comments list-group">
              <div class="comment-add mb-2">
								<b-form-textarea
									id="comment-content"
									v-model="commentContent"
									placeholder="Enter message"
									rows="3"
									no-resize
								/>
								<b-button class="float-right mt-1" size="sm" @click="addComment"
                  :disabled="commentContent.length < 1" variant="primary">Add comment</b-button>
              </div>
              <div v-for="(comment, index) of getSortedComments()" :key="index" class="comment p-2 list-group-item">
                <div class="comment-header d-flex justify-content-between">
                  <small class="text-muted">
                    <router-link :to="{ name: 'Users', query: { user: comment.creator && comment.creator.username }}">
                      @{{ comment.creator && comment.creator.username }}
                    </router-link> · {{ comment.created | dateFilter }}
                  </small>
                  <hr />
                  <span v-if="comment.creator && comment.creator.id === currentUser.id" title="Delete comment"
                    class="d-flex btn-link comment-delete-button" @click.stop="deleteComment(comment)" href="#"><span class="far fa-trash-alt"></span></span>
                </div>
                <div class="comment-content">
                  {{ comment.content }}
                </div>
              </div>
            </div>
          </template>
        </b-form>

      </div>

      <div class="col-sm-12 col-md-8 map-container" id="map">
        <l-map :zoom="zoom" :center="center" :options="mapOptions"
               @contextmenu="setPoint($event)"
               style="position: relative; height: 100%; width: 100%; z-index: 0;" ref="map">
           <l-tile-layer
           :url="mapUrl"
           :attribution="mapAttribution"
           />
           <l-marker :lat-lng.sync="latLngPoint"
             :options="point" :draggable="isEditable" ref="marker">
           </l-marker>
        </l-map>
      </div>

    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import { dateFilter } from '@/utils/filters'
import points from '@/utils/points'

export default {
  // The point view displaying a single point.
  name: 'Point',
  props: {
    pointMode: String,
    pointObject: {
      type: Object,
      default: () => ({
        name: '',
        description: '',
        latitude: 0.0,
        longitude: 0.0,
      })
    },
  },
  mixins: [points],
  created() {
    // Handle inconsistent component state and show a warning toast to the user.
    if (this.pointMode !== 'create' && !this.point.id) {
      this.$toasted.show('Point could not be loaded, please don\'t refresh the page.', { type: 'error' })
      this.$router.push('/')
    }
  },
  mounted() {
    if (this.pointMode !== 'create') {
      this.latitudeSel = this.point.latitude >= 0 ? 1 : -1
      this.longitudeSel = this.point.longitude >= 0 ? 1 : -1
      this.displayLatitude = this.point.latitude * this.latitudeSel
      this.displayLongitude = this.point.longitude * this.longitudeSel

      this.$store.dispatch('getPointDetails', this.point).then(p => {
        this.point = p
      })
    }
  },
  data() {
    return {
      displayLatitude: 0.0,
      displayLongitude: 0.0,
      latitudeSel: 1,
      latitudeOptions: [
        { value: 1, text: '° N' },
        { value: -1, text: '° S' },
      ],
      longitudeSel: 1,
      longitudeOptions: [
        { value: 1, text: '° E' },
        { value: -1, text: '° W' },
      ],
      zoom: 2,
      center: L.latLng(0, 0),
      mapOptions: { zoomSnap: 0.1 },
      point: this.pointObject,
      commentContent: '',
    }
  },
  computed: {
    ...mapState([
      'currentUser',
      'mapUrl',
      'mapAttribution'
    ]),
    isEditable() {
      /*
       * Check if the point's information is editable.
       * returns:
       *   - boolean indicating if the information is editable
       */
      return this.pointMode === 'create' || this.pointMode === 'edit'
    },
    latLngPoint: {
      get() {
        /*
         * Get the Leaflet latLng representation of a coordinate pair.
         * returns:
         *   - Leaflet latLng representation of the coordinates
         */
        return L.latLng(this.point.latitude, this.point.longitude)
      },
      set(value) {
        /*
         * Get the latitude and longitude attributes from the argument.
         * parameters:
         *   - value: Leaflet latLng object to read
         */
        const lat = this.formatCoordinate(value.lat)
        const lng = this.formatCoordinate(value.lng)
        this.latitudeSel = lat >= 0 ? 1 : -1
        this.longitudeSel = lng >= 0 ? 1 : -1
        this.point.latitude = lat
        this.point.longitude = lng
        this.displayLatitude = lat * this.latitudeSel
        this.displayLongitude = lng * this.longitudeSel
      }
    },
  },
  methods: {
    getSortedComments() {
      /*
       * Sort the comments by creation date (latest first).
       * returns:
       *  - list of sorted comments
       */
      return _.chain(this.point.comments._items)
              .sortBy('created')
              .reverse()
              .value()
    },
    setPoint(event) {
      /*
       * Set the point when the map is clicked with the right mouse button.
       * parameters:
       *   - event: contextmenu DOM event to handle
       */
      if (!this.isEditable) {
        return
      }
      const lat = this.formatCoordinate(event.latlng.lat)
      const lng = this.formatCoordinate(event.latlng.lng)
      this.latitudeSel = lat >= 0 ? 1 : -1
      this.longitudeSel = lng >= 0 ? 1 : -1
      this.point.latitude = lat
      this.point.longitude = lng
      this.displayLatitude = lat * this.latitudeSel
      this.displayLongitude = lng * this.longitudeSel
    },
    setLatitude(latitude) {
      /*
       * Set the latitude of the point when the latitude input field is modified.
       * parameters:
       *   - latitude: value of the latitude input field
       */
      this.point.latitude = latitude * this.latitudeSel
    },
    setLongitude(longitude) {
      /*
       * Set the longitude of the point when the longitude input field is modified.
       * parameters:
       *   - longitude: value of the longitude input field
       */
      this.point.longitude = longitude * this.longitudeSel
    },
    createPoint() {
      // Send a POST request to create a new point and then return to the Points page.
      this.$store.dispatch('addPoint', this.point).then((point) => {
        this.$router.push('/points')
      })
    },
    updatePoint() {
      // Send a PUT request to update the current point and then return to the Points page.
      this.$store.dispatch('updatePoint', this.point).then((point) => {
        this.$router.push('/points')
      })
    },
    addComment() {
      // Send a POST request to add a comment to the current point.
      let payload = {'point': this.point, 'commentData': { 'content': this.commentContent }}
      this.$store.dispatch('addComment', payload).then((c) => {
        this.point.comments._items.push(c)
        this.commentContent = ''
      })
    },
    deleteComment(comment) {
      /*
       * Send a DELETE request to delete a comment from the current point.
       * parameters:
       *   - comment: the comment object to delete from the point
       */
      this.$store.dispatch('deleteComment', comment).then(() => {
        this.point.comments._items.splice(this.point.comments._items.indexOf(comment), 1)
      })
    },
    swapLatitude() {
      // Swap the north/south position of the point object.
      this.point.latitude *= -1
    },
    swapLongitude() {
      // Swap the east/west position of the point object.
      this.point.longitude *= -1
    }
  }
}
</script>

<style scoped>
.point-details {
  max-height: calc(100vh - 56px);
  overflow-y: auto;
}
.comment-delete-button {
  cursor: pointer;
  font-size: small;
}
.comment-content {
  overflow-wrap: anywhere;
}
</style>
