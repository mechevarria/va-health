<template>
  <span>
    <div class="container">
      <div class="card">
        <div class="card-body">
          <h4 class="card-title">Welcome to the Clinical Health Application</h4>
          <p class="card-text">To get started, please go to the <a href="home/dashboard" title="App Dashboard">dashboard</a> to begin exploring data</p>
          <img src="../assets/va-logo.png" height="80" alt="Veterans Administration Logo" />
        </div>
      </div>
    </div>
    <router-view></router-view>
  </span>
</template>

<script>
export default {
  name: 'AppHome',
  data() {
  }
}
</script>