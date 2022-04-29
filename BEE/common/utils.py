def remove_non_properties_from_dict(d):
    for k, v in dict(d).items():
        if v is None:
            del d[k]

    return d
