<script setup>
import { useDate } from 'vuetify'
import { useMigrainestore } from '../stores/predictedMigStore.js'
import { ref } from 'vue'
import axios from 'axios'

const colors = ['blue', 'indigo', 'deep-purple', 'cyan', 'green', 'orange', 'grey darken-1']
const events = ref([])
const mig = useMigrainestore()

function generateTitle(value) {
  return (value.loss < -5 ?
    `Starke Abnahme des Luftdrucks` : `Abnahme des Luftdrucks`) + `\n Startzeitpunkt: ${new Date(value.maxima.date)} \n Endzeitpunkt: ${new Date(value.minima.date)} \n Druckabnahme: ${value.loss}  `
}

mig.$subscribe((mutation, state) => {

  axios.get(`http://localhost:5000/data?lat=${state.lat}&long=${state.long}&start_date=${state.start.toISOString()}&end_date=${state.end.toISOString()}`,
    { transformResponse: (data) => JSON.parse(data) })
    .then(res => {
      console.log(res.data)
      let a = res.data.filter(value => value.loss < -2.0).map(value => {
        return {
          'title': generateTitle(value),
          'start': new Date(value.maxima.date),
          'end': new Date(value.minima.date),
          'color': value.loss < -5 ? 'red' : 'yellow',
          'allDay': false
        }
      })
      console.log(a)
      events.value = a
    })

})

const type = ref('month')
const types = ['month', 'week', 'day']
const calendar = ref(null)

function updateRange(event) {
  let viewStart = calendar.value.daysInMonth
  mig.start = viewStart[0].date
  mig.end = viewStart.at(-1).date
}
</script>
<template>
  <v-row>
    <v-col>
      <v-sheet height="600">
        <v-select
          v-model="type"
          :items="types"
          class="ma-2"
          label="View Mode"
          variant="outlined"
          dense
          hide-details
        ></v-select>
        <v-calendar
          ref="calendar"
          :events="events"
          :view-mode="type"
          color="primary"
          type="month"
          @update:modelValue="updateRange"
        ></v-calendar>
      </v-sheet>
    </v-col>
  </v-row>
</template>

<style scoped>

</style>
