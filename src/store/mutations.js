import * as types from './mutation-types'

export const mutations = {
    [types.USER_INIT] (state, user_payload) {
      state.user.data = user_payload
      state.user.is_auth = true
    },

    [types.USER_LOGOUT] (state) {
      state.user.data = {}
      state.user.is_auth = false
    },

    [types.CATEGORIES_FETCH_SUCCESS] (state, categories_payload) {
      state.categories = categories_payload
    },

    [types.EXERCISES_FETCH_SUCCESS] (state, exercises_payload) {
      state.exercises = exercises_payload
    }
}
