def user_in_groups(user, group_names):
    if not user or not user.is_authenticated:
        return False
    return user.groups.filter(name__in=group_names).exists()
