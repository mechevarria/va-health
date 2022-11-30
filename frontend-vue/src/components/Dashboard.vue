<template>
  <span>
    <AppKpi />
    <AppNetwork />
    <li>Groups</li>
    <li>Demographics</li>
    <router-view></router-view>
  </span>
</template>

<script>
import AppKpi from './Kpi.vue'
import AppNetwork from './Network.vue'

export default {
  name: 'AppDashboard',
  components: {
    AppKpi,
    AppNetwork
  }
}
</script>