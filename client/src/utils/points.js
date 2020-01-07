// helper method mixin idea adapted from:
// https://forum.vuejs.org/t/how-to-use-helper-functions-for-imported-modules-in-vuejs-vue-template/6266/5

export default {
  methods: {
    formatCoordinate(coordinate) {
      /*
       * Format a coordinate to include 6 fixed decimal points.
       * parameters:
       *  - coordinate: a coordinate float value
       * returns:
       *   - a coordinate value with 6 fixed decimal points
       */

      return Number(coordinate).toFixed(6)
    },

    pointToLatLng(point) {
      /*
       * Convert a point object to a Leaflet latLng.
       * parameters:
       *   - point: a point object with a latitude and longitude
       * returns:
       *   - Leaflet latLng converted from the point object
       */

      return L.latLng(point.latitude, point.longitude)
    },

    pointToCoordinates(point) {
      /*
       * Convert a point object to a coordinate string with degrees.
       * parameters:
       *   - point: a point object
       * returns:
       *   - a coordinate string (xx.xxxxxx° x, yy.yyyyyyy °y)
       */

      let coordinateString = ''

      if (point.latitude >= 0) {
        coordinateString += this.formatCoordinate(point.latitude) + '° N'
      } else {
        coordinateString += this.formatCoordinate(0 - point.latitude) + '° S'
      }

      coordinateString += ', '

      if (point.longitude >= 0) {
        coordinateString += this.formatCoordinate(point.longitude) + '° E'
      } else {
        coordinateString += this.formatCoordinate(0 - point.longitude) + '° W'
      }

      return coordinateString
    },

    getShortDescription(description, max_length=77) {
      /*
       * Get a shortened point description if the length is greater than the maximum defined
       * parameters:
       *   - description: the point description string
       *   - max_length: maximum length of the description string (default: 77)
       * returns:
       *   - the description shortened to max_length characters if longer than it,
       *     otherwise the full description
       */

      if (description.length >= max_length) {
        return description.slice(0, max_length) + '...'
      } else {
        return description
      }
    }
  }
}
