const getters = {
    currentUser: state => state.user,
    categories: state => state.categories,
    exercises: state => state.exercises,
    exercisesByCategoryId: (state, getters) => id => {
      return getters.exercises.filter(exercise => exercise.category.id === id)
    }
};

export default getters
