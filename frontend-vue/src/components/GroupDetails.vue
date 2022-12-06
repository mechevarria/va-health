<template>
  <span>
    <i class="spinner-border spinner-border-sm mb-1 ml-1" v-if="isBusy"></i>
    <span class="d-flex justify-content-between align-items-center mb-2" v-if="groupId > 0 && !isBusy">
      <h5>Group {{groupId}} Explains:
      </h5>
      <button type="button" class="btn btn-primary" @click="clearGroup()">
        <span class="cil-x-circle icon mr-1"></span>Clear
      </button>
    </span>
    <div class="row row-cols-1 row-cols-md-4">
      <div class="col" v-for="(explain, index) in groupExplains.explains" :key="index">
        <div class="card" v-if="groupId > 0">
          <div class="card-body">
            <li v-for="(value, propertyName, propIndex) in explain" :key="propIndex">
              {{ propertyName }}: {{ value }}
            </li>
          </div>
        </div>
      </div>
    </div>
    <!-- <pre>{{groupExplains}}</pre> -->
    <router-view></router-view>
  </span>
</template>

<script>
import { mapState } from 'vuex'
import axios from 'axios'
import msgMixin from '../mixins/msg-mixin';

export default {
  name: 'AppGroupDetail',
  mixins: [msgMixin],
  computed: mapState(['groupId']),
  data() {
    return {
      isBusy: false,
      groupExplains: {
        explains: []
      }
    }
  },
  watch: {
    groupId(newValue) {
      if (newValue > 0) {
        this.isBusy = true
        const url = `/api/group/${newValue}`
        axios
          .get(url)
          .then((res) => {
            this.groupExplains = res.data
            this.infoMsg(`Group ${newValue} has ${this.groupExplains.explains.length} explains`)
          })
          .catch((err) => {
            console.error(err)
            this.errorMsg(err.message)
          })
          .finally(() => {
            this.isBusy = false
          })
      }
    }
  },
  methods: {
    clearGroup() {
      this.groupExplains.explains = []
      this.$store.commit('clearGroup')
    }
  }
}
</script>