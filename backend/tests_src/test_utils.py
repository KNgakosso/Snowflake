import src.utils as utils
import pytest

#TEST VERIF_ALPHA
#################################


@pytest.mark.parametrize("alpha_val", [0., 1e-10, 0.5, 1-1e-10, 1, 1.])
def test_verif_alpha_1_alpha_OK(alpha_val):
    utils.verif_alpha(alpha=alpha_val)

@pytest.mark.parametrize("alpha_val", [-10, -1e-10, 1+1e-1, 201.2])
def test_verif_alpha_1_alpha_ERROR(alpha_val):
    with pytest.raises(ValueError) as e:
        utils.verif_alpha(alpha_1=alpha_val)
    assert str(e.value) == "The parameter alpha_1 must be a float number between 0 and 1"

def test_verif_alpha_2_alphas_OK():
    utils.verif_alpha(alpha_1=0.3, alpha_2=0.99)

def test_verif_alpha_2_alphas_ERROR_on_alpha_1():
    with pytest.raises(ValueError) as e:
        utils.verif_alpha(alpha_1 = 7, alpha_2 = 0.5)
    assert str(e.value) == "The parameter alpha_1 must be a float number between 0 and 1"

def test_verif_alpha_2_alphas_ERROR_on_alpha_2():
    with pytest.raises(ValueError) as e:
        utils.verif_alpha(alpha_1 = 0.1, alpha_2 = 4)
    assert str(e.value) == "The parameter alpha_2 must be a float number between 0 and 1"

def test_verif_alpha_4_alphas_OK():
    utils.verif_alpha(alpha_1=0.3, alpha_2=0.19, alpha_3 = 0.5, alpha_4=1e-1)

def test_verif_alpha_4_alphas_mutliple_ERRORS():
    with pytest.raises(ValueError) as e:
        utils.verif_alpha(alpha_1=0.3, alpha_2=10, alpha_3 = -8, alpha_4=1000)
    assert str(e.value) == "The parameter alpha_2 must be a float number between 0 and 1"

def test_verif_alpha_4_alphas_mutliple_ERRORS_ARGS():
    with pytest.raises(ValueError) as e:
        utils.verif_alpha(0.3, 10, -8, 1000)
    #assert str(e.value) == "The parameter alpha_2 must be a float number between 0 and 1"

# TEST VERIF NON NEGATIVITY
#######################################

@pytest.mark.parametrize("value", [0, 1e-15, 10, 1000])
def test_verif_non_negativity_OK(value):
    utils.verif_non_negativity(param=value)

@pytest.mark.parametrize("value", [-1002.5, -1e-15])
def test_verif_non_negativity_ERROR(value):
    with pytest.raises(ValueError) as e:
        utils.verif_non_negativity(param=value)
    assert str(e.value) == "The parameter param must be a non negative float number"

def test_verif_non_negativity_2_params_OK():
    utils.verif_non_negativity(param_1=0.3, param_2=99)

def test_verif_non_negativity_2_params_ERROR_on_param_1():
    with pytest.raises(ValueError) as e:
        utils.verif_non_negativity(param_1 = -1, param_2 = 45.5)
    assert str(e.value) == "The parameter param_1 must be a non negative float number"

def test_verif_non_negativity_2_param_2_ERROR_on_param_2():
    with pytest.raises(ValueError) as e:
        utils.verif_non_negativity(param_1 = 0.1, param_2 = -4)
    assert str(e.value) == "The parameter param_2 must be a non negative float number"

def test_verif_non_negativity_4_params_OK():
    utils.verif_non_negativity(param_1=30.2, param_2=0.19, param_3 = 50000, param_4=1e-11)

def test_verif_non_negativity_4_params_mutliple_ERRORS():
    with pytest.raises(ValueError) as e:
        utils.verif_non_negativity(param_1=0.3, param_2=-10, param_3 = -8, param_4=-1000)
    assert str(e.value) == "The parameter param_2 must be a non negative float number"


# TEST VERIF_ID
####################################

@pytest.mark.parametrize("id", [(0,0), (1,0), (1,5), (10,0), (15,4), (100, 599)])
def test_verify_id_OK(id):
    utils.verif_id(id)

@pytest.mark.parametrize("id", [(-1,0), (-10, 2), (-100,1990),       #id[0] negative
                                (10,-1), (15,-900), (0, -10),        #id[1] negative
                                (-1,-1), (-6, -100), (-40, -2)       #both negative
])
def test_verify_id_ERROR_negative_values(id):
    with pytest.raises(ValueError) as e: 
        utils.verif_id(id)
    assert str(e.value) == "The id must be a 2 integers tuple (r, i). \n" \
                             "The first number r must be non negative.\n" \
                             "The second number i must respect the condiftion r <= i < r*6."
    
@pytest.mark.parametrize("id", [(0,1), (0, 10),
                                (1, 6), (1, 1500),
                                (10, 60), (10,900)
])
def test_verify_id_ERROR_i_too_high(id):
    with pytest.raises(ValueError) as e: 
        utils.verif_id(id)
    assert str(e.value) == "The id must be a 2 integers tuple (r, i). \n" \
                             "The first number r must be non negative.\n" \
                             "The second number i must respect the condiftion r <= i < r*6."
    


# TEST above
#####################
@pytest.mark.parametrize("r, i, expec_res", [
    (1, 0, (2, 0)),            #arrete 0 -> arrete 0
    (4, 4, (5, 5)),            #arrete 1 -> arrete 1
    (3, 15, (4, 20)),          #arrete 5 -> arrete 5

    (4, 2, (5, 2)),            #interieur 0 -> interieur 0
    (2, 9, (3, 13)),           #interieur 4 -> interieur 4
    (5, 29, (6, 34))           #interieur 5 -> interieur 5
])
def test_above(r, i, expec_res):
    result = utils.above(r, i) 
    assert expec_res == result

def test_above_zero_ERROR():
    with pytest.raises(ValueError) as e:
        utils.above(0, 4)

# TEST above right
#####################
@pytest.mark.parametrize("r, i, expec_res", [
    (1, 0, (2, 1)),            #arrete 0 -> interieur 0
    (5, 10, (6, 13)),          #arrete 2 -> interieur 2
    (2, 8, (3, 13)),           #arrete 5 -> interieur 5


    (2, 1, (3, 2)),            #interieur 0 -> interieur 0
    (4, 14, (5, 18)),          #interieur 3 -> interieur 3
    (3, 17, (4, 23))           #interieur 5 -> interieur 5
])
def test_above_right(r, i, expec_res):
    result = utils.above_right(r, i) 
    assert expec_res == result

def test_above_right_zero_ERROR():
    with pytest.raises(ValueError) as e:
        utils.above_right(0, 4)

# TEST above left
#####################
@pytest.mark.parametrize("r, i, expec_res", [
    (1, 0, (2, 11)),        #arrete 0 -> interieur 5
    (3, 6, (4, 7)),         #arrete 3 -> interieur 2
    (4, 20, (5, 24)),       #arrete 5 -> interieur 4

    (5, 1, (5, 0)),         #interieur 0 -> arrete 0
    (6, 7, (6, 6)),         #interieur 1 -> arrete 1
    (3, 16, (3, 15)),       #interieur 5 -> arrete 5

    (2, 1, (2, 0)),         #interieur 0 -> interieur 0
    (3, 11, (3, 10)),       #interieur 3 -> interieur 3
    (4, 22, (4, 21)),       #interieur 5 -> interieur 5
])
def test_above_left(r, i, expec_res):
    result = utils.above_left(r, i) 
    assert expec_res == result

def test_above_left_zero_ERROR():
    with pytest.raises(ValueError) as e:
        utils.above_left(0, 4)

# TEST below
#####################
@pytest.mark.parametrize("r, i, expec_res", [
    (1, 0, (0, 0)),            #arrete 0 -> center
    (1, 4, (0, 0)),            #arrete 4 -> center
    (1, 5, (0, 0)),            #arrete 5 -> center

    (3, 0, (2, 0)),            #arrete 0 -> arrete 0
    (6, 6, (5, 5)),            #arrete 1 -> arrete 1
    (2, 10, (1, 5)),           #arrete 5 -> arrete 5
    
    (6, 5, (5, 5)),            #interieur 0 -> arrete 1
    (3, 5, (2, 4)),            #interieur 1 -> arrete 2
    (2, 11, (1, 0)),           #interieur 5 -> arrete 0

    (4, 2, (3, 2)),            #interieur 0 -> interieur 0
    (5, 17, (4, 14)),          #interieur 3 -> interieur 3
    (3, 16, (2, 11))           #interieur 5 -> interieur 5
])
def test_below(r, i, expec_res):
    result = utils.below(r, i) 
    assert expec_res == result

def test_below_zero_ERROR():
    with pytest.raises(ValueError) as e:
        utils.below(0, 4)


# TEST below right
#####################
@pytest.mark.parametrize("r, i, expec_res", [
    (1, 0, (1, 1)),         #arrete 0 -> arrete 1
    (1, 1, (1, 2)),         #arrete 1 -> arrete 2
    (1, 5, (1, 0)),         #arrete 5 -> arrete 0

    (5, 10, (5, 11)),       #arrete 2 -> interieur 2
    (4, 0, (4, 1)),         #arrete 0 -> interieur 0
    (6, 24, (6, 25)),       #arrete 5 -> interieur 5

    (4, 1, (4, 2)),         #interieur 0 -> interieur 0
    (3, 16, (3, 17)),       #interieur 5 -> interieur 5
    (3, 13, (3, 14)),       #interieur 4 -> interieur 4

    (2, 1, (2, 2)),         #interieur 0 -> arrete 2
    (6, 29, (6, 30)),       #interieur 4 -> arrete 5
    (4, 23, (4, 0)),        #interieur 5 -> arrete 0
])
def test_below_right(r, i, expec_res):
    result = utils.below_right(r, i) 
    assert expec_res == result

def test_below_right_zero_ERROR():
    with pytest.raises(ValueError) as e:
        utils.below_right(0, 4)


# TEST below left
#####################
@pytest.mark.parametrize("r, i, expec_res", [
    (1, 0, (1, 5)),        #arrete 0 -> arrete 5
    (1, 4, (1, 3)),        #arrete 4 -> arrete 3
    (1, 5, (1, 4)),        #arrete 5 -> arrete 4

    (4, 0, (4, 23)),       #arrete 0 -> interieur 5
    (2, 2, (2, 1)),        #arrete 1 -> interieur 0
    (6, 30, (6, 29)),      #arrete 5 -> interieur 4


    (5, 3, (4, 2)),        #interieur 0 -> interieur 0
    (4, 23, (3, 17)),      #interieur 5 -> interieur 5
    (3, 8, (2, 5)),        #interieur 2 -> interieur 2

    (4, 3, (3, 2)),        #interieur 0 -> arrete 0
    (3, 13, (2, 8)),       #interieur 4 -> arrete 4
    (6, 34, (5, 28)),      #interieur 5 -> arrete 5
])
def test_below_left(r, i, expec_res):
    result = utils.below_left(r, i) 
    assert expec_res == result

def test_below_left_zero_ERROR():
    with pytest.raises(ValueError) as e:
        utils.below_left(0, 4)