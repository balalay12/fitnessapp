import trafaret as t

add_set_validator = t.Dict({
    t.Key('date') >> 'date': t.String(),
    t.Key('exercise') >> 'exercise': t.Int(gt=0),
    t.Key('sets') >> 'sets': t.List(
        t.Mapping(t.String, t.Float(gt=0))
    )
})

edit_set_validator = t.Dict({
    t.Key('id') >> 'id': t.Int(gt=0),
    t.Key('exercise_id') >> 'exercise_id': t.Int(gt=0),
})

planning_validator = t.Dict({
    t.Key('programm_id') >> 'programm_id': t.Int(gt=0),
    t.Key('date') >> 'date': t.String()
})

add_repeat_validator = t.Dict({
    t.Key('id') >> 'id': t.Int(gt=0),
    t.Key('weight') >> 'weight': t.Float(gte=0),
    t.Key('count') >> 'count': t.Float(gte=0),
})