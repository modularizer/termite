import termite.raw.unicode as r


_unicode_names = [k for k in dir(r) if k.upper() == k and not k.startswith("_")]
dashed_unicode_names = [k.lower().replace("_", "-") for k in _unicode_names]
_unicode_chars = {k.lower().replace("_", "").replace("-", ""): getattr(r, k) for k in _unicode_names}
unicode_names = list(_unicode_chars)

class Unicode:
    def __getattr__(self, item):
        return self[item]

    def __getitem__(self, item):
        return _unicode_chars[item.lower().replace("_", "").replace("-", "").replace(":", "")]

    def __dir__(self):
        return list(_unicode_chars)

    def __iter__(self):
        return iter(_unicode_chars)

    def __contains__(self, item):
        k = item.lower().replace("_", "").replace("-", "").replace(":", "")
        return k in _unicode_chars

    def keys(self):
        return _unicode_chars.keys()

    def values(self):
        return _unicode_chars.values()

    def __repr__(self):
        return "".join(_unicode_chars.values())

    def __str__(self):
        return "".join(_unicode_chars.values())

unicode = Unicode()

