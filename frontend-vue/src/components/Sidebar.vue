<template>
  <div class="c-sidebar c-sidebar-dark c-sidebar-fixed"
    :class="{ 'c-sidebar-minimized': isSidebarMin, 'c-sidebar-show': isSidebarShown }" id="sidebar">
    <div class="c-sidebar-brand d-md-down-none">
      <router-link to="/">
        <img class="c-sidebar-brand-full" src="../assets/symphony-ai-logo-white.svg" alt="SAI logo" width="150" />
        <img class="c-sidebar-brand-minimized" src="../assets/symphony-ai-icon-white.svg" width="30" alt="SAI Logo" />
      </router-link>
    </div>
    <ul class="c-sidebar-nav" @mouseenter="mouseEnter" @mouseleave="mouseLeave">
      <li class="c-sidebar-nav-item">
        <router-link class="c-sidebar-nav-link" to="/home/dashboard" @click.native="closeOnMobile">
          <i class="c-sidebar-nav-icon cil-speedometer"></i> Dashboard
        </router-link>
      </li>
      <li class="c-sidebar-nav-item">
        <router-link class="c-sidebar-nav-link" to="/home/compare" @click.native="closeOnMobile">
          <i class="c-sidebar-nav-icon cil-blur-linear"></i> Group Compare
        </router-link>
      </li>
      <li class="c-sidebar-nav-item">
        <router-link class="c-sidebar-nav-link" to="/home/patient" @click.native="closeOnMobile">
          <i class="c-sidebar-nav-icon cil-address-book"></i> Patient
        </router-link>
      </li>
    </ul>
    <button class="c-sidebar-minimizer c-class-toggler" type="button" aria-label="toggle sidebar min" @click="toggleMin"></button>
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  name: 'AppSidebar',
  data() {
    return {
      isMouseEnter: false
    }
  },
  computed: mapState(['isSidebarMin', 'isSidebarShown']),
  methods: {
    toggleMin() {
      this.$store.commit('toggleSidebarMin')
    },
    mouseEnter() {
      if (this.isSidebarMin) {
        this.$store.commit('sidebarMax')
        this.isMouseEnter = true
      }
    },
    mouseLeave() {
      if (this.isMouseEnter) {
        this.$store.commit('sidebarMin')
        this.isMouseEnter = false
      }
    },
    closeOnMobile() {
      // iPad was not getting caught by the isMobile component
      if (this.$isMobile() || navigator.userAgent.includes('iPad')) {
        this.$store.commit('sidebarHide')
      }
    }
  },
  created() {
    if (this.$isMobile() && this.isSidebarShown) {
      this.$store.commit('sidebarHide')
    }
  }
}
</script>