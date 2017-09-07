import * as types from './mutation-types'
import axios from 'axios'

export const userInit = ({ commit}) => {
  axios.get('/get_user')
  .then(response => {
    commit(types.USER_INIT, response.data)
  })
  .catch(error => {
    console.log(error)
  })
}

export const userLogout = ({ commit }) => {
  commit(types.USER_LOGOUT)
}
