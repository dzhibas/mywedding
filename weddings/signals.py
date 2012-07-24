def invitation_created(sender, instance, *args, **kwargs):
    if instance.invite_code == '':
        instance.invite_code = 'GENERATED'

    return
