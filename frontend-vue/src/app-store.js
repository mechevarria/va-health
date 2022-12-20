import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const store = new Vuex.Store({
    state: {
        isSidebarMin: false,
        isSidebarShown: true,
        messages: [],
        groupId: 0,
        filterId: 0,
        colors: {
            first: '#ea39b8',
            second: '#ffc107',
            third: '#1ba2f6'
        },
        colorOptions: [{
            value: 'A1Clast_period2_to_4_change',
            text: 'Change in A1C'
        }, {
            value: 'visits_count_permonth_period2_to_4_change',
            text: 'Change in Engagement'
        }, {
            value: 'Is_increase_A1Clast_period2_to_4_change',
            text: 'Predicted A1C Increase'
        }, {
            value: 'Is_decrease_visits_count_permonth_period2_to_4_change',
            text: 'Predicted Change in Engagement'
        }],
        filters: [{
            name: 'Race',
            label: 'Race',
            categorical: true,
            value: 'American Indian or Alaska Native',
            valueOptions: [{
                value: 'American Indian or Alaska Native', text: 'American Indian/Alaska Native'
            }, {
                value: 'Asian', text: 'Asian'
            }, {
                value: 'Black or African American', text: 'African American'
            }, {
                value: 'Native Hawaiian or Pacific Islander', text: 'Native Hawaiian/Pacific Islander'
            }, {
                value: 'White', text: 'White'
            }, {
                value: 'Unknown', text: 'Asian'
            }],
            boolOptions: [{
                value: true, text: 'Yes'
            }, {
                value: false, text: 'No'
            }],
            is_equal: true,
            enabled: false
        }, {
            name: 'Ethnicity',
            label: 'Ethnicity',
            categorical: true,
            value: 'HISPANIC OR LATINO',
            valueOptions: [{
                value: 'HISPANIC OR LATINO', text: 'Hispanic or Latino'
            }, {
                value: 'NOT HISPANIC OR LATINO', text: 'NOT Hispanic or Latino'
            }, {
                value: 'Unknown', text: 'Unknown'
            }],
            boolOptions: [{
                value: true, text: 'Yes'
            }, {
                value: false, text: 'No'
            }],
            is_equal: true,
            enabled: false
        }, {
            name: 'MaritalStatus',
            label: 'Marital Status',
            categorical: true,
            value: 'SINGLE',
            valueOptions: [{
                value: 'DIVORCED', text: 'Divorced'
            }, {
                value: 'MARRIED', text: 'Married'
            },{
                value: 'NEVER MARRIED', text: 'Never Married'
            },{
                value: 'SEPERATED', text: 'Seperated'
            },{
                value: 'SINGLE', text: 'Single'
            }, {
                value: 'UNKNOWN', text: 'Unknown'
            }, {
                value: 'WIDOW/WIDOWER', text: 'Widow/Widower'
            },{
                value: 'WIDOWED', text: 'Widowed'
            },{
                value: '"Missing"', text: 'Missing'
            }],
            boolOptions: [{
                value: true, text: 'Yes'
            }, {
                value: false, text: 'No'
            }],
            is_equal: true,
            enabled: false
        }, {
            name: 'Rurality',
            label: 'Rurality',
            categorical: true,
            value: 'Urban',
            valueOptions: [{
                value: 'CityTown', text: 'City Town'
            }, {
                value: 'SmallTownRural', text: 'Small Town Rural'
            }, {
                value: 'Urban', text: 'Urban'
            }],
            boolOptions: [{
                value: true, text: 'Yes'
            }, {
                value: false, text: 'No'
            }],
            is_equal: true,
            enabled: false
        }, {
            name: 'AgeAtIndexDate',
            label: 'Age',
            categorical: false,
            min: 25,
            inputMin: 20,
            max: 90,
            inputMax: 120,
            enabled: false
        }, {
            name: 'A1C_last_period4_2021-03-01_2022-03-01',
            label: 'A1C',
            categorical: false,
            min: 5,
            inputMin: 4,
            max: 15,
            inputMax: 22,
            enabled: false
        }, {
            label: 'Vaccination Status',
            name: 'TotalSeriesCount',
            categorical: false,
            min: 0,
            inputMin: 0,
            max: 3,
            inputMax: 3,
            enabled: false
        },{
            name: 'Hospitalization60d',
            label: 'Hospitalizations',
            categorical: true,
            value: '0',
            valueOptions: [{
                value: '0', text: 'False'
            }, {
                value: '1', text: 'True'
            }],
            is_equal: true,
            enabled: false
        },{
            label: 'In-Person Visit %',
            name: 'visits_count_proportion_Presumed In Person_period4_2021-03-01_2022-03-01',
            categorical: false,
            min: 0,
            inputMin: 0,
            max: 100,
            inputMax: 100,
            enabled: false,
            percentage: true
        }]
    },
    mutations: {
        toggleSidebarMin(state) {
            state.isSidebarMin = !state.isSidebarMin
        },
        sidebarMin(state) {
            state.isSidebarMin = true
        },
        sidebarMax(state) {
            state.isSidebarMin = false
        },
        toggleSidebarShown(state) {
            state.isSidebarShown = !state.isSidebarShown
        },
        sidebarHide(state) {
            state.isSidebarShown = false
        },
        sidebarShow(state) {
            state.isSidebarShown = true
        },
        addMessage(state, msg) {
            state.messages.push(msg)
        },
        clearMessages(state) {
            state.messages = []
        },
        setGroup(state, id) {
            state.groupId = id
        },
        clearGroup(state) {
            state.groupId = 0
        },
        setFilterId(state, id) {
            state.filterId = id
        },
        setFilters(state, filters) {
            state.filters = filters
        },
        clearFilter(state) {
            state.filterId = 0
        }
    }
})

export default store