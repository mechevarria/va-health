<template>
  <span>
    <h4>Clinical Dashboard</h4>
    <li>KPI</li>
    <li>Graph</li>
    <li>Groups</li>
    <li>Demographics</li>
    <router-view></router-view>
  </span>
</template>

<script>
import msgMixin from '../mixins/msg-mixin'

export default {
  name: 'AppDashboard',
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