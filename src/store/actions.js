import * as types from './mutation-types'
import axios from 'axios'

export const userInit = ({ commit, dispatch }) => {
  axios.get('/get_user')
  .then(response => {
    commit(types.USER_INIT, response.data)
    dispatch('categoriesFetch')
    dispatch('exercisesFetch')
  })
  .catch(error => {
    console.log(error)
  })
}

export const userLogout = ({ commit }) => {
  commit(types.USER_LOGOUT)
}

export const categoriesFetch = ({ commit }) => {
  axios.get('/training/categories')
  .then(response => {
    commit(types.CATEGORIES_FETCH_SUCCESS, response.data.categories)
  })
}

export const exercisesFetch = ({ commit }) => {
  axios.get('/training/exercises')
  .then(response => {
    commit(types.EXERCISES_FETCH_SUCCESS, response.data.exercises);
  })
}
