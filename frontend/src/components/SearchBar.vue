<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useMigrainestore } from '../stores/predictedMigStore.js'

const migrainestore = useMigrainestore()

let city = ref('')
let lat = ref(0.0)
let long = ref(0.0)
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
  console.log(city.value)
  axios.get(`https://geocoding-api.open-meteo.com/v1/search?name=${city.value}&count=1&language=en&format=json`)
    .then(res => {
      let respons = res.data.results[0]
      city.value = respons.name
      lat.value = respons.latitude
      long.value = respons.longitude
    })
}

function requestMigraine() {
  axios.get(`http://localhost:5000/data?lat=${lat.value}&${long.value}`, { transformResponse: (data) => JSON.parse(data) })
    .then(res => {
      console.log(res.data)
      migrainestore.daylist = res.data
    })
}
</script>
<template>
  <v-row>
    <v-col justify="space-around">
      <v-row justify="space-around">
        <v-text-field label="City" placeholder="Berlin" @change="lul" v-model="city"></v-text-field>
        <v-text-field label="Latitude" placeholder="0" v-model="lat"></v-text-field>
        <v-text-field label="Longtude" placeholder="0" v-model="long"></v-text-field>
      </v-row>


    </v-col>

  </v-row>
  <v-row>
    <v-date-input
      label="Select range"
      show-adjacent-months
      max-width="368"
      multiple="range" v-model="dates"></v-date-input>
    <v-btn text="Search" @click="requestMigraine"></v-btn>
  </v-row>
</template>

<style scoped>

</style>
