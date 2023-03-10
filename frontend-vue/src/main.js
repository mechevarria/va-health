import Vue from 'vue'
import App from './App.vue'
import {
  NavPlugin,
  DropdownPlugin,
  ToastPlugin,
  TablePlugin,
  PaginationPlugin,
  FormSelectPlugin,
  ModalPlugin,
  ProgressPlugin,
  FormInputPlugin,
  FormSpinbuttonPlugin,
  FormCheckboxPlugin,
  FormRadioPlugin,
  TooltipPlugin
} from 'bootstrap-vue'
import VueMobileDetection from 'vue-mobile-detection'
import 'perfect-scrollbar/dist/perfect-scrollbar'
import '@popperjs/core/dist/esm/popper'
import HighchartsVue from 'highcharts-vue'
import router from './app-router'
import store from './app-store'

Vue.config.productionTip = false

Vue.use(NavPlugin)
Vue.use(DropdownPlugin)
Vue.use(ToastPlugin)
Vue.use(TablePlugin)
Vue.use(PaginationPlugin)
Vue.use(FormSelectPlugin)
Vue.use(ModalPlugin)
Vue.use(ProgressPlugin)
Vue.use(FormInputPlugin)
Vue.use(FormSpinbuttonPlugin)
Vue.use(FormCheckboxPlugin)
Vue.use(FormRadioPlugin)
Vue.use(TooltipPlugin)
Vue.use(VueMobileDetection)
Vue.use(HighchartsVue)

new Vue({
  render: (h) => h(App),
  router,
  store
}).$mount('#app')
