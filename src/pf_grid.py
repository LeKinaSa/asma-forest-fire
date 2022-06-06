import numpy as np
from mesa.batchrunner import BatchRunner

from ForestFire import ForestFire
from treecells.DrosselSchwabl import DrosselSchwabl

def main():
    param_set = dict(
        height=[50],
        width=[50],
        density=[0.5],
        TreeCell=[DrosselSchwabl],
        protection=[0],
        p=np.linspace(0, 1, 11)[1:],
        f=np.linspace(0, 1, 11)[1:]
    )

    # At the end of each model run, calculate the fraction of trees which are Burned Out
    model_reporter = {
        "BurntFine": lambda m: (ForestFire.count_type(m, "Burned Out") / ForestFire.count_type(m, "Fine"))
    }

    # Create the batch runner
    param_run = BatchRunner(ForestFire, param_set, iterations=1, model_reporters=model_reporter)
    param_run.run_all()
    df = param_run.get_model_vars_dataframe()
    d = df.to_dict()

    for p in range(10):
        if p != 0:
            print("===========")
        for f in range(10):
            index = p*10 + f
            print(f"p={round(d['p'][index], 1)} f={round(d['f'][index], 1)} b={round(d['BurntFine'][index], 2)}")
            

if __name__ == "__main__":
    main()