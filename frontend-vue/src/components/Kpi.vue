<template>
  <span>
    <div class="card-deck">
      <div
        class="card mb-4 mt-2 text-white"
        v-for="(kpi, index) in data"
        :key="index"
        :class="getStyle(index)"
      >
        <div class="card-body">
          {{ kpi.name }}  <i class="spinner-border spinner-border-sm float-right" v-if="isBusy"></i>
          <h4>{{ kpi.value }}</h4>
        </div>
      </div>
    </div>
  </span>
</template>

<script>
import { mapState } from 'vuex'
import axios from 'axios'
import msgMixin from '../mixins/msg-mixin'

export default {
  name: 'AppKpi',
  computed: mapState(['filterId']),
  mixins: [msgMixin],
  data() {
    return {
      data: [],
      isBusy: false
    }
  },
  methods: {
    setPlaceholder() {
      this.data = []
      for (let i = 0; i < 5; i++) {
        this.data.push({
          name: '--',
          value: '--'
        })
      }
    },
    getKpi() {
      this.setPlaceholder()
      this.isBusy = true
      let url = '/api/kpi'
      if (this.filterId > 0) {
        url = url + `/${this.filterId}`
      }
      axios
        .get(url)
        .then((res) => {
          this.data = res.data
        })
        .catch((err) => {
          console.error(err)
          this.errorMsg(err.message)
        })
        .finally(() => {
          this.isBusy = false
        })
    },
    getStyle(index) {
      let style = 'bg-danger'
      switch (index) {
        case 0:
          style = 'bg-secondary'
          break
        case 1:
          style = 'bg-primary'
          break
        case 2:
          style = 'bg-warning'
          break
        case 3:
          style = 'bg-success'
          break
        case 4:
          style = 'bg-info'
          break
      }
      return style
    }
  },
  watch: {
    filterId() {
      this.getKpi()
    }
  },
  created() {
    this.getKpi()
  }
}
</script>
