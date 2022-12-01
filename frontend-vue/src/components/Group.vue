<template>
  <span>
    <h5>Groups:</h5>
    <div class="card-deck mb-3">
      <div class="card">
        <div class="card-header">
          <h5 class="d-flex justify-content-between align-items-center">
            S1
            <button type="button" class="btn btn-sm" @click="toggleCard">
              <i v-if="!showCard" class="cil-chevron-bottom btn-icon"></i>
              <i v-if="showCard" class="cil-chevron-top btn-icon"></i>
            </button>
          </h5>
          <span class="bg-light text-dark">
            <span class="font-weight-bold">Patients:</span> 56 | <span class="font-weight-bold">Explainers:</span> 2
          </span>
        </div>
        <div class="card-body" v-if="showCard">
          <div class="card-text">
            Top Explainers:
            <li>53.27% higher concentration of "visit type = virtual"</li>
            <li>Higher values of relative weight = Medium</li>
          </div>
        </div>
      </div>
    </div>
    <router-view></router-view>
  </span>
</template>

<script>

export default {
  name: 'AppGroup',
  data() {
    return {
      showCard: false
    }
  },
  methods: {
    toggleCard() {
      this.showCard = !this.showCard
    }
  }
}
</script>