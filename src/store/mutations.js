import * as types from './mutation-types'

export const mutations = {
    [types.USER_INIT] (state, user_payload) {
      state.user.data = user_payload
      state.user.is_auth = true
    },

    [types.USER_LOGOUT] (state) {
      state.user.data = {}
      state.user.is_auth = false
    }
}
