import trafaret as t

registration_validator = t.Dict({
    t.Key('email') >> 'email': t.String(
        r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'
    ),
    t.Key('password') >> 'password': t.String(min_length=8),
    t.Key('first_name') >> 'first_name': t.String(),
    t.Key('last_name') >> 'last_name': t.String
})

login_validator = t.Dict({
    t.Key('email') >> 'email': t.String(),
    t.Key('password') >> 'password': t.String()
})

goal_validator = t.Dict({
        t.Key('goal') >> 'goal': t.String(allow_blank=True)
    })


trainer_info_validator = t.Dict({
    t.Key('price') >> 'price': t.Or(t.Int(), t.String(allow_blank=True)),
    t.Key('description') >> 'description': t.String(allow_blank=True)
})