def seconds_to_minutes(seconds, return_string=True):
    minutes = seconds // 60
    reste = seconds % 60
    if return_string:
        if minutes == 0:
            txt = f"{reste} seconds"
        else:
            txt = f"{minutes} minutes"
            if reste:
                txt += f" and {reste} seconds"
        return txt
    else:
        return minutes, reste


def clean_number(x):
    return int(x) if isinstance(x, float) and x.is_integer() else x