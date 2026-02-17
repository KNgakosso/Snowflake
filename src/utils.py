def verif_alpha(*args, **kwargs):
    for value in args:
        if value < 0 or value > 1:
            raise ValueError("All alphas must be float number between 0 and 1")
    for name, value in kwargs.items():
        if value < 0 or value > 1:
            raise ValueError(f"The parameter {name} must be a float number between 0 and 1")
        
def verif_non_negativity(*args, **kwargs):
    for value in args:
        if value < 0:
            raise ValueError("All alphas must be float number between 0 and 1")
    for name, value in kwargs.items():
        if value < 0:
            raise ValueError(f"The parameter {name} must be a non negative float number")
        
def verif_id(id : tuple[int, int]):
    if id[0] < 0 or id[1] < 0 or id[1] >= 6*id[0]:
        if id != (0,0):
            raise ValueError("The id must be a 2 integers tuple (r, i). \n" \
                             "The first number r must be non negative.\n" \
                             "The second number i must respect the condiftion r <= i < r*6."
                    )

def create_list_ids(nb_rings : int):
    list_ids = [(0,0)]
    for r in range(nb_rings + 1):
        for i in range(6*r):
            list_ids.append((r,i))
    return list_ids

def above(r : int, i : int) -> tuple[int, int]:
    if r == 0:
        raise ValueError
    s, p = divmod(i, r)
    return (r+1, s * (r+1) + p)

def above_right(r : int, i : int) -> tuple[int, int]:
    if r == 0:
        raise ValueError
    s, p = divmod(i, r)
    return (r+1, (s * (r+1) + p+1) % (6*(r+1)))


def above_left(r : int, i : int) -> tuple[int, int]:
    if r == 0:
        raise ValueError
    s, p = divmod(i, r)
    return (r+(p==0), (s * (r+(p==0)) + p-1) % (6*(r+(p==0))))

def below(r : int, i : int) -> tuple[int, int]:
    if r == 0:
        raise ValueError
    elif r == 1:
        return (0, 0)
    s, p = divmod(i, r)
    return (r-1, (s * (r-1) + p) % (6*(r-1)))

def below_right(r : int, i : int) -> tuple[int, int]:
    if r == 0:
        raise ValueError
    s, p = divmod(i, r)
    return (r, (s * r + p+1) % (6*r))

def below_left(r : int, i : int) -> tuple[int, int]:
    if r == 0:
        raise ValueError
    s, p = divmod(i, r)
    return (r-(p!=0), (s * (r-(p!=0)) + p-1) % (6*(r-(p!=0))))
