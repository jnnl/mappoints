<template>
  <div class="home">
    <div class="row">

      <div class="col-sm-12 col-md-4 latest-container">
        <div class="d-flex justify-content-between align-items-center mt-3">
          <h4 class="mb-3">Latest points</h4>
        </div>
        <div class="list-group">
          <div v-for="(point, index) in latestPoints"
             :key="index"
             @click="selectPoint(point, true)"
             href="#"
             class="point-item list-group-item list-group-item-action
             flex-column align-items-start collapsed">
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
            </div>
            <div v-if="point.description" :id="'collapse-' + index" class="point-item-description collapse my-2">
              {{ getShortDescription(point.description, 140) }}
            </div>
          </div>
        </div>
      </div>

      <div class="col-sm-12 col-md-8 map-container" id="map">
        <l-map
           :zoom="zoom"
           :center="center"
           :options="mapOptions"
           style="height: 100%; width: 100%"
           ref="map"
           >
           <l-tile-layer
           :url="mapUrl"
           :attribution="mapAttribution"
           />
             <l-marker-cluster :options="clusterOptions" ref="markerCluster">
               <l-marker v-for="point in latestPoints"
                :key="point.id"
                :lat-lng="pointToLatLng(point)"
                :options="point"
                ref="marker">
                   <l-popup>
                     <div>
                       <b>
                          <router-link :to="{ name: 'Point', params: { pointMode: isOwner(point) ? 'edit' : 'view', pointObject: point, id: point.id } }">{{ point.name }}</router-link>
                       </b>
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
import points from '@/utils/points'
import { LMap, LTileLayer, LMarker, LPopup } from 'vue2-leaflet';

export default {
  // The home view displaying the latest points.
  name: 'Home',
  components: {
    LMap,
    LTileLayer,
    LMarker,
    LPopup,
  },
  mixins: [points],
  mounted() {
    this.$store.dispatch('getPoints', '?expand=creator')
  },
  data () {
    return {
      zoom: 2,
      center: L.latLng(0, 0),
      mapOptions: { zoomSnap: 0.5 },
      clusterOptions: { maxClusterRadius: 15 },
    };
  },
  computed: {
    ...mapState([
      'currentUser',
      'points',
      'mapUrl',
      'mapAttribution',
    ]),
    latestPoints() {
      /*
       * Get the 'maxLatest' latest points (default: 5)
       * returns:
       *   - list of n latest points, sorted by latest first
       */
      const maxLatest = 5;
      return _.chain(this.points)
        .sortBy('created')
        .reverse()
        .take(maxLatest)
        .value()
    },
  },
  methods: {
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
    selectPoint(point) {
      /* Select a point and open its popup in the map.
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
.latest-container {
}
.map-container {
  min-height: 800px;
  width: 100%;
}
.point-name {
  overflow-wrap: anywhere;
}
.point-item-arrow:after {
  content: "▲";
}
.point-item-arrow.collapsed:after {
  content: "▼";
}
.point-item-description {
  border-top: 1px solid #dddddd;
  padding-top: 1em;
}
.leaflet-popup-close-button {
  display: none;
}
</style>
