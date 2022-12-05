<template>
  <span>
    <h4 class="d-flex justify-content-between align-items-center">Clinical Dashboard <button class="btn btn-primary"><i class="cil-filter btn-icon mr-1"></i>Filter</button></h4>
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