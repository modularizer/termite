import termite.raw.emojis as r


_emoji_names = [k for k in dir(r) if k.upper() == k and not k.startswith("_")]
dashed_emoji_names = [k.lower().replace("_", "-") for k in _emoji_names]
_emojis = {k.lower().replace("_", "").replace("-", ""): getattr(r, k) for k in _emoji_names}
emoji_names = list(_emojis)

class Emojis:
    def __getattr__(self, item):
        return self[item]

    def __getitem__(self, item):
        return _emojis[item.lower().replace("_", "").replace("-", "").replace(":", "")]

    def __dir__(self):
        return list(_emojis)

    def __iter__(self):
        return iter(_emojis)

    def __contains__(self, item):
        k = item.lower().replace("_", "").replace("-", "").replace(":", "")
        return k in _emojis

    def keys(self):
        return _emojis.keys()

    def values(self):
        return _emojis.values()

    def __repr__(self):
        return "".join(emojis.values())

    def __str__(self):
        return "".join(emojis.values())

emojis = Emojis()