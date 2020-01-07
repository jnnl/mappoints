<template>
  <div class="points">
    <div class="row">

      <div class="col-sm-12 col-md-4 points-container">
        <div class="d-flex justify-content-between align-items-center mt-3">
          <h4 class="mb-0">Points</h4>
        </div>
        <div class="points-controls mb-3">
          <div class="points-buttons">
            <b-button :to="{ name: 'Point', params: { pointMode: 'create', id: 'create' }}" size="sm" variant="primary" class="mr-1">
              <span class="fas fa-plus mr-1"></span>
              Add
            </b-button>
            <b-button v-b-toggle.controls-collapse
                      size="sm" variant="primary">
              <span class="fas fa-filter mr-1"></span>
              Filter/Sort
            </b-button>
          </div>
          <b-collapse id="controls-collapse" class="mt-2" visible>
            <b-card>
              <div class="font-weight-bold mb-1">Filter</div>
              <div class="mb-2">
                <b-input-group size="sm" prepend="Point" class="mb-2">
                  <b-form-input v-model="filterFields.point" placeholder="Enter point name"/>
                  <b-input-group-append>
                    <b-button size="sm" @click="filterFields.point = ''">Clear</b-button>
                  </b-input-group-append>
                </b-input-group>
                <b-input-group size="sm" prepend="Creator" class="mb-2">
                  <b-form-input v-model="filterFields.creator" placeholder="Enter creator name"/>
                  <b-input-group-append>
                    <b-button size="sm" @click="filterFields.creator = ''">Clear</b-button>
                  </b-input-group-append>
                </b-input-group>
              </div>
              <div class="font-weight-bold mb-1">Sort</div>
              <b-row>
                <b-col cols="7" class="pr-2">
                  <b-input-group size="sm" prepend="Sort by">
                    <b-form-select v-model="sortFieldSel" :options="sortFields" size="sm"/>
                  </b-input-group>
                </b-col>
                <b-col cols="5" class="pl-0">
                  <b-input-group size="sm" prepend="Direction">
                    <b-form-select v-model="sortDirectionSel" :options="sortDirections" size="sm"/>
                  </b-input-group>
                </b-col>
              </b-row>
            </b-card>
          </b-collapse>
        </div>
        <div class="list-group">
          <div v-for="(point, index) in paginatedPoints"
               :key="index"
               @click="selectPoint(point)"
               href="#"
               class="point-item list-group-item list-group-item-action
                      flex-column align-items-start"
               >
            <div class="point-item-header d-flex w-100 justify-content-between">
              <h5 class="mb-1 point-name">
                <router-link :to="{ name: 'Point', params: { pointMode: isOwner(point) ? 'edit' : 'view', pointObject: point, id: point.id }}">
                  {{ point.name }}
                </router-link>
              </h5>
              <small class="text-muted">
                <router-link :to="{ name: 'Users', query: { user: point.creator.username }}">
                  @{{ point.creator.username }}
                </router-link> · {{ point.created | dateFilter }}
              </small>
            </div>
            <div class="point-item-footer d-flex justify-content-between">
              <small class="point-item-coordinates">
                <span v-if="point.description" class="point-item-arrow collapsed mr-1" data-toggle="collapse" :data-target="'#collapse-' + index"></span>
                {{ pointToCoordinates(point) }}
              </small>
              <small>
                <router-link title="Comment point" :to="{ name: 'Point', params: { pointMode: isOwner(point) ? 'edit' : 'view', pointObject: point, id: point.id }}">
                  <span class="far fa-comment"></span>
                  {{ point.comments._items.length }}
                </router-link>
                <template v-if="point.creator.id === currentUser.id">
                 ·
                <span title="Delete point" class="btn-link point-delete-button" @click.stop="deletePoint(point)" href="#"><span class="far fa-trash-alt"></span></span>
                </template>
              </small>
            </div>
            <div v-if="point.description" :id="'collapse-' + index" class="point-item-description collapse my-2">
              {{ getShortDescription(point.description, 140) }}
            </div>
          </div>
        </div>
        <div class="d-flex justify-content-between">
          <b-pagination class="point-pagination" v-model="currentPage" :total-rows="filteredPoints.length" :per-page="pageSize"/>
        </div>
      </div>

      <div class="col-sm-12 col-md-8 map-container" id="map">
        <l-map :zoom="zoom" :center="center" :options="mapOptions"
               style="position: relative; height: 100%; width: 100%; z-index: 0;" ref="map">
           <l-tile-layer
           :url="mapUrl"
           :attribution="mapAttribution"
           />
           <l-marker-cluster :options="clusterOptions" ref="markerCluster">
             <l-marker v-for="(point, index) in filteredPoints"
                       :key="index" :lat-lng="pointToLatLng(point)"
                       :options="point" ref="marker">
                 <l-popup>
                   <div>
                     <b>
                       <router-link :to="{ name: 'Point', params: { pointMode: isOwner(point) ? 'edit' : 'view', pointObject: point, id: point.id } }">{{ point.name }}</router-link></b>
                     <br/>
                     {{ pointToCoordinates(point) }}
                   </div>
                 </l-popup>
               </l-marker>
             </l-marker-cluster>
           </l-map>
      </div>

    </div>

  </div>
</template>

<script>
import { mapState } from 'vuex'
import { dateFilter } from '@/utils/filters'
import { LMap, LTileLayer, LMarker, LPopup } from 'vue2-leaflet';
import points from '@/utils/points'
import Vue2LeafletMarkerCluster from 'vue2-leaflet-markercluster'

export default {
  // The points view displaying the points in the system.
  name: 'Points',
  components: {
    LMap,
    LTileLayer,
    LMarker,
    LPopup,
  },
  props: {
    user: {
      default: '',
      type: String
    }
  },
  mixins: [points],
  mounted() {
    // Send a request to get the points from the API.
    this.$store.dispatch('getPoints', '?expand=creator')
  },
  data () {
    return {
      currentPage: 1,
      pageSize: 10,
      filterFields: {
        point: '',
        creator: this.user,
      },
      sortFields: [
        { value: 'created', text: 'Date' },
        { value: 'name', text: 'Point name' },
        { value: 'creator.username', text: 'Creator name' }
      ],
      sortDirections: [ 
        { value: 'asc', text: 'Ascending' },
        { value: 'desc', text: 'Descending' }
      ],
      zoom: 2,
      center: L.latLng(0, 0),
      mapOptions: { zoomSnap: 0.1 },
      clusterOptions: { maxClusterRadius: 15 },
    };
  },
  computed: {
    ...mapState([
      'currentUser',
      'users',
      'points',
      'mapUrl',
      'mapAttribution'
    ]),
    sortFieldSel: {
      get() {
        /*
         * Get the point sort field (created/name/creator) from the Vuex store.
         * returns:
         *   - the sort field value saved in the Vuex store
         */
        return this.$store.state.sortFieldSel
      },
      set(value) {
        /*
         * Commit the selected point sort field (created/name/creator) to the Vuex store.
         * parameters:
         *   - the value of the sort field ('created', 'name' or 'creator.username')
         */
        this.$store.commit('updateSortFieldSel', value)
      }
    },
    sortDirectionSel: {
      get() {
        /*
         * Get the point sort direction (ascending/descending) from the Vuex store.
         * returns:
         *   - the sort direction value saved in the Vuex store
         */
        return this.$store.state.sortDirectionSel
      },
      set(value) {
        /*
         * Commit the selected point sort direction (ascending/descending) to the Vuex store.
         * parameters:
         *   - the value of the sort direction ('asc' or 'desc')
         */
        this.$store.commit('updateSortDirectionSel', value)
      }
    },
    filteredPoints() {
      /*
       * Get the points that match the values given in the filter fields
       * returns:
       *   - a subset of points that match specified filter input fields
       */
      let processedPoints = this.points
      if (this.filterFields.point.length) {
        processedPoints = processedPoints.filter(this.filterByPointName)
      }
      if (this.filterFields.creator.length) {
        processedPoints = processedPoints.filter(this.filterByCreatorName)
      }
      return _.orderBy(processedPoints, this.sortFieldSel, this.sortDirectionSel)
    },
    paginatedPoints() {
      /*
       * Get a paginated slice of the point list determined by the current page and its size.
       * returns:
       *   - a paginated subset of the point list corresponding to current page values
       */
      const pageStart = (this.currentPage - 1) * this.pageSize
      const pageEnd = pageStart + this.pageSize
      return this.filteredPoints.slice(pageStart, pageEnd)
    }
  },
  methods: {
    deletePoint(point) {
      /*
       * Send a DELETE request to delete a point.
       * parameters:
       *   - point: the point object to delete
       */
      this.$store.dispatch('deletePoint', point)
    },
    isOwner(point) {
      /*
       * Check if the current user is the owner of the given point.
       * parameters:
       *   - point: the point object to check the ownership of
       * returns:
       *   - boolean indicating if the current user is the owner of the point
       */
      return point.creator.id == this.currentUser.id
    },
    filterByPointName(point) {
      /*
       * Check if the point name matches the point name filter input field's content.
       * parameters:
       *   - point: the point object to check the name of
       * returns:
       *   - boolean indicating if the point's name matches the point name filter field
       */
      let name = point.name.toLowerCase()
      return name.toLowerCase().includes(this.filterFields.point.toLowerCase())
    },
    filterByCreatorName(point) {
      /*
       * Check if the point's creator name matches the creator name filter input field's content.
       * parameters:
       *   - point: the point object to check the creator's name of
       * returns:
       *   - boolean indicating if the point creator's name matches the creator name filter field
       */
      let name = point.creator.username.toLowerCase()
      let creatorName = this.filterFields.creator.toLowerCase()

      if (this.filterFields.creator.indexOf('@') === 0) {
        return name === creatorName.substring(1)
      } else {
        return name.includes(creatorName)
      }
    },
    selectPoint(point) {
      /*
       * Select a point and open its popup in the map.
       * parameters:
       *   - point: point to show in the map with its popup
       */
      for (let marker of this.$refs.marker) {
        if (point.id === marker.options.id) {
          if (!this.$refs.map.mapObject.hasLayer(marker.mapObject)) {
            this.$refs.markerCluster.mapObject.zoomToShowLayer(marker.mapObject, () => {
              marker.mapObject.openPopup()
            })
          } else {
            marker.mapObject.openPopup()
          }
        }
      }
    },
  }
}
</script>

<style>
.points-container {
  overflow-y: auto;
  max-height: calc(100vh - 60px);
}
.points-buttons {
  position: absolute;
  top: 15px;
  right: 15px;
}
.map-container {
  min-height: 800px;
  width: 100%;
  height: calc(100vh - 60px);
}
.point-name {
  overflow-wrap: anywhere;
}
.point-item-arrow {
  cursor: pointer;
}
.point-item-arrow:after {
  content: "▲";
}
.point-item-arrow.collapsed:after {
  content: "▼";
}
.point-delete-button {
  cursor: pointer;
}
.point-item-description {
  border-top: 1px solid #dddddd;
  padding-top: 1em;
}
.point-pagination {
  margin: 1em auto;
}
.leaflet-popup-close-button {
  display: none;
}
</style>
