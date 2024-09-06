<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useMigrainestore } from '../stores/predictedMigStore.js'

const migrainestore = useMigrainestore()

let start = new Date()
start.setDate(start.getDate() - 5)
let end = new Date()

end.setDate(end.getDate() + 16)
let dates = ref(getDatesBetween(start, end))

function getDatesBetween(startDate, endDate) {
  let dates = []
  let currentDate = new Date(startDate)
  while (currentDate <= endDate) {
    dates.push(new Date(currentDate))
    currentDate.setDate(currentDate.getDate() + 1)
  }
  return dates
}


function lul() {
  axios.get(`https://geocoding-api.open-meteo.com/v1/search?name=${migrainestore.city}&count=1&language=en&format=json`)
    .then(res => {
      let respons = res.data.results[0]
      migrainestore.city = respons.name
      migrainestore.lat = respons.latitude
      migrainestore.long = respons.longitude
    })
}


</script>
<template>
  <v-row>
    <v-col justify="space-around">
      <v-row justify="space-around">
        <v-text-field label="City" placeholder="Berlin" @change="lul" v-model="migrainestore.city"></v-text-field>
        <v-text-field label="Latitude" placeholder="0" v-model="migrainestore.lat"></v-text-field>
        <v-text-field label="Longtude" placeholder="0" v-model="migrainestore.long"></v-text-field>
      </v-row>
    </v-col>

  </v-row>

</template>

<style scoped>

</style>
