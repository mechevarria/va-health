<template>
  <div id="app" class="c-app">
    <AppSidebar />
    <div class="c-wrapper">
      <AppHeader />
      <main class="c-main">
        <div class="container-fluid">
          <router-view></router-view>
        </div>
      </main>
      <AppFooter />
    </div>
    <div
      :class="{'c-sidebar-backdrop c-fade c-show': this.$store.state.isSidebarShown && $isMobile()}"
      @click="doHide()"
    ></div>
  </div>
</template>

<script>
import AppHeader from './components/Header.vue'
import AppFooter from './components/Footer.vue'
import AppSidebar from './components/Sidebar.vue'

export default {
  name: 'App',
  components: {
    AppHeader,
    AppFooter,
    AppSidebar
  },
  methods: {
    doHide() {
      this.$store.commit('sidebarHide')
    }
  }
}
</script>

<style lang="scss">
//Just in case we want to change up theme colors
$theme-colors: (
  primary: #671aa0,
  info: #1EACFC,
  danger: #fa089e,
  warn: #FFB600,
  success: #00bb9c
);

@import '~perfect-scrollbar/css/perfect-scrollbar.css';
@import '~@coreui/coreui/scss/coreui';
@import '~@coreui/icons/css/all.min.css';
@import '~bootstrap-vue/dist/bootstrap-vue.css';
</style>
