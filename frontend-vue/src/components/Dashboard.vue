<template>
  <span>
    <h4 class="d-flex justify-content-between align-items-center">Clinical Dashboard
      <button class="btn btn-primary" v-b-modal.filter-modal><i class="cil-filter btn-icon mr-1"></i>Filter</button>
    </h4>
    <AppKpi />
    <AppNetwork />
    <AppGroup />
    <AppGroupDetails />
    <b-modal id="filter-modal" title="BootstrapVue">
      <p class="my-4">Filter options will go here</p>
    </b-modal>
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