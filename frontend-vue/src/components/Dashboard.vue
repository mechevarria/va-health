<template>
  <span>
    <h4>Clinical Dashboard</h4>
      <AppKpi />
    <li>Graph</li>
    <li>Groups</li>
    <li>Demographics</li>
    <router-view></router-view>
  </span>
</template>

<script>
import AppKpi from './Kpi.vue'
import msgMixin from '../mixins/msg-mixin'

export default {
  name: 'AppDashboard',
  components: {
    AppKpi
  },
  mixins: [msgMixin],
  data() {
    return {
      data: [],
    }
  },
  methods: {
  },
  created() {
  }
}
</script>