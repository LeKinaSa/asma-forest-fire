import numpy as np
import seaborn as sns

import matplotlib.pyplot as plt

from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.batchrunner import BatchRunner
from mesa import Agent

from typing import List

from ForestFire import ForestFire

from treecells.Simple import Simple
from treecells.DrosselSchwabl import DrosselSchwabl
from treecells.SingleSpread import SingleSpread

def agent_portrayal(agent):
    state_to_color = {
        "Empty": "white",
        "Fine" : "green",
        "On Fire" : "red",
        "Burned Out" : "black",
        "Protected": "cyan",
    }
    portrayal = {"Shape": "rect",
                 "Color": state_to_color[agent.condition],
                 "Filled": "true",
                 "Layer": 0,
                 "w": 0.9,
                 "h": 0.9
                 }
    return portrayal

def pick_a_model(models : List[Agent]) -> int:
    print("Pick a model:")
    for i, agent in enumerate(models):
        print(f"    [{i}] {agent}")
    choice = int(input(":> "))
    assert 0 <= choice < len(models)
    return choice

def pick_a_grid_size(grid_sizes : List[int]) -> int:
    print("Pick a grid size:")
    for i, size in enumerate(grid_sizes):
        print(f"    [{i}] {size}")
    choice = int(input(":> "))
    assert 0 <= choice < len(grid_sizes)
    return choice

def main():
    models = [Simple, SingleSpread, DrosselSchwabl]
    grid_sizes = [5, 20, 50, 100]

    model_choice = pick_a_model(models)
    grid_choice = pick_a_grid_size(grid_sizes)

    (p, f) = (0.1, 0.1)
    density = float(input("Pick a density: (from 0 to 1):> "))
    assert 0 < density <= 1

    protection = float(input(f"Pick a protection rate: (from 0 to {1-density}):> "))
    assert 0 <= protection <= 1 - density

    if model_choice == 2:
        p = float(input("Pick a regeneration rate: (from 0 to 1):> "))
        f = float(input("Pick a fire ignition rate: (from 0 to 1):> "))
        assert 0 <= p <= 1
        assert 0 <  f <= 1

    visualization = True
    if input("Visualization? [Y|n]:> ") in ("n", "N"):
        visualization = False

    if visualization:
        grid = CanvasGrid(agent_portrayal, grid_sizes[grid_choice], grid_sizes[grid_choice], 900, 900)
        server = ModularServer(ForestFire, [grid], "Forest Fire", {
            "width": grid_sizes[grid_choice],
            "height": grid_sizes[grid_choice],
            "density": density,
            "protection": protection,
            "TreeCell": models[model_choice],
            "p": p,
            "f": f
        })
        server.port = 8521 # The default
        server.launch()
    
    graphs = True
    if input("Graphics? [Y|n]:> ") in ("n", "N"):
        graphs = False
    
    if graphs:
        # fire = ForestFire(grid_sizes[grid_choice], grid_sizes[grid_choice], density, protection, models[model_choice], p, f)
        # fire.run_model()
        # results = fire.dc.get_model_vars_dataframe()
        # sns.lineplot(data=results)
        # plt.show()

        param_set = dict(height=[grid_sizes[grid_choice]],
                        width=[grid_sizes[grid_choice]],
                        density=[density], # Vary density from 0.01 to 1, in 0.01 increments
                        TreeCell=[models[model_choice]],
                        protection=[0],
                        p=np.linspace(0, 1, 11)[1:], f=np.linspace(0, 1, 11)[1:] # 11 11
                        )

        # At the end of each model run, calculate the fraction of trees which are Burned Out
        model_reporter = {"BurntFine": lambda m: (ForestFire.count_type(m, "Burned Out") / 
                                                ForestFire.count_type(m, "Fine"))}

        # Create the batch runner
        param_run = BatchRunner(ForestFire, param_set, iterations=1, model_reporters=model_reporter)
        param_run.run_all()
        df = param_run.get_model_vars_dataframe()
        print(df)
        sns.displot(df, x="p", y="f", hue="BurntFine")
        plt.xlim(0, 1)
        plt.show()
    
    # param_set = dict(height=[grid_sizes[grid_choice]],
    #                 width=[grid_sizes[grid_choice]],
    #                 density=np.linspace(0, 1, 101)[1:], # Vary density from 0.01 to 1, in 0.01 increments
    #                 TreeCell=[models[model_choice]],
    #                 protection=[None],
    #                 p=[p], f=[f]
    #                 )

    # # At the end of each model run, calculate the fraction of trees which are Burned Out
    # model_reporter = {"BurnedOut": lambda m: (ForestFire.count_type(m, "Burned Out") / 
    #                                           m.schedule.get_agent_count()),
    #                   "Fine": lambda m: (ForestFire.count_type(m, "Fine") / 
    #                                           m.schedule.get_agent_count()),
    #                   "OnFire": lambda m: (ForestFire.count_type(m, "On Fire") / 
    #                                           m.schedule.get_agent_count())}
    
    # # Create the batch runner
    # param_run = BatchRunner(ForestFire, param_set, iterations=5, model_reporters=model_reporter)
    # param_run.run_all()
    # df = param_run.get_model_vars_dataframe()
    # plt.scatter(df.protection, df.BurnedOut)
    # plt.xlim(0, 1)
    # plt.show()
    
    # plt.scatter(df.protection, df.Fine)
    # plt.xlim(0, 1)
    # plt.show()

if __name__ == "__main__":
    main()