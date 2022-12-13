import Vue from 'vue'
import VueRouter from 'vue-router'
import AppHome from './components/Home.vue'
import AppForm from './components/Form.vue'
import AppTable from './components/Table.vue'
import AppDetail from './components/Detail.vue'
import AppDashboard from './components/Dashboard.vue'
import AppCompare from './components/Compare.vue'

Vue.use(VueRouter)

const routes = [{
    path: '/home',
    component: AppHome,
    name: 'home'
}, {
    path: '/home/form',
    component: AppForm,
    name: 'form'
}, {
    path: '/home/table',
    component: AppTable,
    name: 'table'
}, {
    path: '/home/table/:id',
    component: AppDetail
}, {
    path: '/home/dashboard',
    component: AppDashboard,
    name: 'dashboard'
}, {
    path: '/home/compare',
    component: AppCompare,
    name: 'compare'
}, {
    path: '*',
    redirect: '/home'
}]

const router = new VueRouter({
    mode: 'history',
    routes: routes,
    linkActiveClass: 'c-sidebar-nav-link-primary'
})

export default router