<script setup>
import { useDate } from 'vuetify'
import { useMigrainestore } from '../stores/predictedMigStore.js'
import { ref } from 'vue'

const colors = ['blue', 'indigo', 'deep-purple', 'cyan', 'green', 'orange', 'grey darken-1']
const events = ref([])
const mig = useMigrainestore()

function generateTitle(value) {
  return (value.loss < -5 ?
    `Starke Abnahme des Luftdrucks` : `Abnahme des Luftdrucks`) + `\n Startzeitpunkt: ${new Date(value.maxima.date)} \n Endzeitpunkt: ${new Date(value.minima.date)} \n Druckabnahme: ${value.loss}  `
}

mig.$subscribe((mutation, state) => {
  console.log(state.daylist)
  let a = state.daylist.filter(value => value.loss < -2.0).map(value => {
    return {
      'title': generateTitle(value),
      'start': new Date(value.maxima.date),
      'end': new Date(value.minima.date),
      'color': value.loss < -5 ? 'red' : 'yellow',
      'allDay': false
    }
  })
  events.value = a
})

const type = ref('month')
const types = ['month', 'week', 'day']
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

        > </v-calendar>
      </v-sheet>
    </v-col>
  </v-row>
</template>

<style scoped>

</style>
