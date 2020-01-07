import Vue from "vue"
import moment from "moment"

Vue.filter("dateFilter", date => {
  // Convert and return a DD.MM.YYYY HH:mm date representation from UTC
  if (date) {
    return moment(String(date)).format("DD.MM.YYYY HH:mm")
  }
})
