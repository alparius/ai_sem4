"""
TODO
    Build a system that approximate the quality of a concrete mixture based on the used ingredients.
    The training data will be taken from: http://archive.ics.uci.edu/ml/datasets/Concrete+Slump+Test.


TODO
    Input variables (7) (component kg in one M^3 concrete):
        Cement
        Slag
        Fly ash
        Water
        SP
        Coarse Aggr.
        Fine Aggr.
    Output variables (3):
        SLUMP (cm)
        FLOW (cm)
        28-day Compressive Strength (Mpa)
"""


from my_gpalgorithm import GPAlgorithm

if __name__ == '__main__':
    algorithmGP = GPAlgorithm()
    algorithmGP.run()
