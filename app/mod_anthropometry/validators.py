import trafaret as t


add_body_size_validator = t.Dict({
    t.Key('neck', optional=True) >> 'neck': t.Float(gte=0.0),
    t.Key('chest', optional=True) >> 'chest': t.Float(gte=0.0),
    t.Key('waist', optional=True) >> 'waist': t.Float(gte=0.0),
    t.Key('forearm', optional=True) >> 'forearm': t.Float(gte=0.0),
    t.Key('arm', optional=True) >> 'arm': t.Float(gte=0.0),
    t.Key('hip', optional=True) >> 'hip': t.Float(gte=0.0),
    t.Key('shin', optional=True) >> 'shin': t.Float(gte=0.0),
})

edit_body_size_validator = t.Dict({
    t.Key('id') >> 'id': t.Int(gt=0),
    t.Key('neck', optional=True) >> 'neck': t.Float(gte=0.0),
    t.Key('chest', optional=True) >> 'chest': t.Float(gte=0.0),
    t.Key('waist', optional=True) >> 'waist': t.Float(gte=0.0),
    t.Key('forearm', optional=True) >> 'forearm': t.Float(gte=0.0),
    t.Key('arm', optional=True) >> 'arm': t.Float(gte=0.0),
    t.Key('hip', optional=True) >> 'hip': t.Float(gte=0.0),
    t.Key('shin', optional=True) >> 'shin': t.Float(gte=0.0),
})
