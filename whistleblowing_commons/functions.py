from .config import _

def seconds_to_minutes(seconds, return_string=True):
    minutes = seconds // 60
    reste = seconds % 60
    if return_string:
        if minutes == 0:
            txt = _(dict(en=f"{reste} seconds", fr=f"{reste} secondes"))
        else:
            txt = _(dict(en=f"{minutes} minutes", fr=f"{minutes} minutes"))
            if reste:
                txt += _(dict(en=f" and {reste} seconds", fr=f" et {reste} secondes"))
        return txt
    else:
        return minutes, reste
