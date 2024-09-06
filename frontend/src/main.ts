import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import 'vuetify/styles'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import App from './App.vue'
import router from './router'
import { createVuetify } from 'vuetify'
import { VCalendar } from 'vuetify/labs/VCalendar'
import { VDateInput } from 'vuetify/labs/components'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(createVuetify({

  directives, components: { ...components, VCalendar, VDateInput }
}))

app.mount('#app')
