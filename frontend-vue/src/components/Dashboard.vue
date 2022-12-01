<template>
  <span>
    <AppKpi />
    <AppNetwork />
    <AppGroup />
    <AppGroupDetails />
    <router-view></router-view>
  </span>
</template>

<script>
import AppKpi from './Kpi.vue'
import AppNetwork from './Network.vue'
import AppGroup from './Group.vue'
import AppGroupDetails from './GroupDetails.vue'

export default {
  name: 'AppDashboard',
  components: {
    AppKpi,
    AppNetwork,
    AppGroup,
    AppGroupDetails
  }
}
</script>