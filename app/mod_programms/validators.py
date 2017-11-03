import trafaret as t

add_programm = t.Dict({
    t.Key('name') >> 'name': t.String(),
    t.Key('exercises') >> 'exercises': t.List(t.Int(gt=0))
})

edit_programm_name = t.Dict({
    t.Key('id') >> 'id': t.Int(gt=0),
    t.Key('name') >> 'name': t.String()
})

add_exercise = t.Dict({
    t.Key('id') >> 'id': t.Int(gt=0),
    t.Key('new_exercise') >> 'new_exercise': t.Int(gt=0)
})

change_exercise = t.Dict({
    t.Key('id') >> 'id': t.Int(gt=0),
    t.Key('old_exercise') >> 'old_exercise': t.Int(gt=0),
    t.Key('new_exercise') >> 'new_exercise': t.Int(gt=0),
})

delete_exercise = t.Dict({
    t.Key('id') >> 'id': t.Int(gt=0),
    t.Key('exercise_id') >> 'exercise_id': t.Int(gt=0),
})
