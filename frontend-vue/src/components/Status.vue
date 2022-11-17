<template>
  <span>
    <div class="card-deck">
      <div class="card">
        <div class="card-body">
          <h4 class="card-title">Eureka API Status</h4>
          <div class="card-text">
            <pre>{{data}}</pre>
          </div>
        </div>
      </div>
    </div>
    <router-view></router-view>
  </span>
</template>

<script>
import axios from 'axios'
import msgMixin from '../mixins/msg-mixin'

export default {
  name: 'AppHome',
  mixins: [msgMixin],
  data() {
    return {
      data: [],
      isBusy: false
    }
  },
  methods: {
    getStatus() {
      this.isBusy = true
      const url = '/api/status'
      axios
        .get(url)
        .then((res) => {
          this.data = JSON.stringify(res.data, null, 2)
        })
        .catch((err) => {
          console.error(err)
          this.errorMsg(err.message)
        })
        .finally(() => {
          this.isBusy = false
        })
    }
  },
  created() {
    this.getStatus()
  }
}
</script>