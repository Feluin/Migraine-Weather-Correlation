import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useMigrainestore = defineStore('migrainedays', () => {
  let daylist = ref([])
  let
    setdays = (newdays) => {
      daylist.value = newdays
    }
  return { daylist, setdays }
})