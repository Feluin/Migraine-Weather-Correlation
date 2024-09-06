import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useMigrainestore = defineStore('migrainedays', () => {
  let daylist = ref([])
  let
    setdays = (newdays) => {
      daylist.value = newdays
    }
  let city = ref('')
  let lat = ref(0.0)
  let long = ref(0.0)
  let start = ref(new Date())
  let end = ref(new Date())
  return { daylist, setdays, city, lat, long, start, end }
})