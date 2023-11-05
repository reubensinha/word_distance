from numpy import sqrt


## TODO Might rewrite this as dataclass 
##      Also might change row variables into a 2D array + 2nd array for offsets
##      this should allow for more dynamic keyboard sizes. + easier to port to other languages.
class keyboard:
    def __init__(self, row1, row2, row3, key_size, key_spacing):
        """Keyboard Layout

        Args:
            row1 (tuple): (offset->int, keys->list)
            row2 (tuple): (offset->int, keys->list)
            row3 (tuple): (offset->int, keys->list)
            key_size (float): side length of key in mm
            key_spacing (float): gap between keys in mm
        """
        self.row1 = row1
        self.row2 = row2
        self.row3 = row3
        self.key_size = key_size
        self.key_spacing = key_spacing

def word_distance(word, keyboard):
    """Return the Distance traveled by a finger to type a word.

    Args:
        word (String): String whose length we will return
        keyboard (_type_): _description_
    """

    word = word.upper()
    dist = 0
    for i in range(len(word)-1):
        dist_i = find_dist(word[i], word[i+1], keyboard)
        if dist_i == -1:
            return -1
        dist += dist_i
    return dist

def find_dist(c1, c2, keyboard):
    """Find Distance between 2 letters on given keyboard

    Args:
        c1 (string of len 1): Letter 1
        c2 (string of len 1): Letter 2
        keyboard (_type_): _description_
    
    Returns:
        dist: distance between 2 keys in mm
         -1 : if invalid string
    """
    y_c1, row_c1 = find_row(c1, keyboard)
    y_c2, row_c2 = find_row(c2, keyboard)

    if (y_c1 == -1 or y_c2 == -1):
        return -1

    gap = keyboard.key_size + keyboard.key_spacing

    y = (y_c1 - y_c2) * gap
    x = (row_c1[0] + row_c1[1].index(c1)*gap) - (row_c2[0] + row_c2[1].index(c2)*gap)

    return sqrt(x**2 + y**2)

def find_row(key, keyboard):
    """Find which row a key is in

    Args:
        key (string of len 1): key to be found
        keyboard (keyboard obj): layout of given keyboard

    Returns:
        row: row tuple selected from keyboard object
        -1 : if key not found
    """
    if key in keyboard.row1[1]:
        row = (1, keyboard.row1)
    elif key in keyboard.row2[1]:
        row = (2, keyboard.row2)
    elif key in keyboard.row3[1]:
        row = (3, keyboard.row3)
    else:
        return (-1, keyboard.row1)
    
    return row


def main(): 
    ## Standard Qwerty Keyboard
    ##
    ## Row 1: (0, ["Q", "W", "E"," "R", "T", "Y", "U", "I", "O", "P"])
    ## Row 2: (0.25 * 19.05, ["A", "S", "D", "F, "G", "H", J, K, L])       Offset: 1/4 key from Row 1
    ## Row 3: (0.75 * 19.05, [Z, X, C, V, B, N, M])             Offset: 1/2 key from Row 2
    ## Key size: 19.05 x 19.05 mm
    ## Key spacing: assume 0 for now
    qwerty = keyboard(
        (0, ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"]),
        (0.25 * 19.05, ["A", "S", "D", "F", "G", "H", "J", "K", "L"]),
        (0.75 * 19.05, ["Z", "X", "C", "V", "B", "N", "M"]),
        19.05,
        0
    )

    WORD = str(input("Enter Word: "))
    print(f"Word is: {WORD}")

    dist = word_distance(WORD, qwerty)
    if dist == -1:
        print("Invalid Word")
    else:
        print(f"Distance traveled: {round(dist, 2)}mm")


main()
    
