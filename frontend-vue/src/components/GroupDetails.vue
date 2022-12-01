<template>
  <span>
    <h5>Group {{groupName}} Demographics</h5>
    <router-view></router-view>
  </span>
</template>

<script>

export default {
  name: 'AppGroupDetail',
  data() {
    return {
      groupName: 'S7'
    }
  }
}
</script>