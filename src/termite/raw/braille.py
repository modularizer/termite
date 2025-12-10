def braille(dots, show=False):
    """
    dots: iterable of integers 1..8
    returns the Unicode Braille character

    14
    25
    36
    78
    """
    value = 0
    for d in dots:
        value |= 1 << (d - 1)
    s = chr(0x2800 + value)
    if show:
        print(s)
    return s



if __name__ == "__main__":
    braille([1], show=True)         # ⠁
    braille([1,2,3], show=True)     # ⠇
    braille([1,4,7], show=True)     # ⡉
    braille([2,5,8], show=True)     # ⢒
    braille([3,6,7], show=True)     # ⡥
    braille([1,2,3,4,5], show=True) # ⠟
    braille([1,2,3,4,5,6,7,8], show=True) # ⣿
