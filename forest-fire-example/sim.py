import numpy as np
import seaborn as sns

import matplotlib.pyplot as plt

from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

from ForestFire import ForestFire
from treecells.Simple import Simple

def agent_portrayal(agent):
    state_to_color = {
        "Fine" : "green",
        "On Fire" : "red",
        "Burned Out" : "black"
    }
    portrayal = {"Shape": "rect",
                 "Color": state_to_color[agent.condition],
                 "Filled": "true",
                 "Layer": 0,
                 "w": 0.9,
                 "h": 0.9
                 }
    return portrayal

grid = CanvasGrid(agent_portrayal, 20, 20, 900, 900)
server = ModularServer(ForestFire,
                       [grid],
                       "Forest Fire",
                       {"width": 20, "height": 20, "density": 0.7, "TreeCell": Simple})
server.port = 8521 # The default
server.launch()

# fire = ForestFire(100, 100, 0.6)
# fire.run_model()
# results = fire.dc.get_model_vars_dataframe()
# print(results)
# sns.lineplot(data=results)
# plt.show()

# fire = ForestFire(100, 100, 0.8)
# fire.run_model()
# results = fire.dc.get_model_vars_dataframe()
# sns.lineplot(data=results)
# plt.show()

# param_set = dict(height=[50], # Height and width are constant
#                  width=[50],
#                  # Vary density from 0.01 to 1, in 0.01 increments:
#                  density=np.linspace(0,1,101)[1:])

# # At the end of each model run, calculate the fraction of trees which are Burned Out
# model_reporter = {"BurnedOut": lambda m: (ForestFire.count_type(m, "Burned Out") / 
#                                           m.schedule.get_agent_count()) }

# # Create the batch runner
# param_run = BatchRunner(ForestFire, param_set, model_reporters=model_reporter)
# param_run.run_all()
# df = param_run.get_model_vars_dataframe()
# df.head()
# plt.scatter(df.density, df.BurnedOut)
# plt.xlim(0,1)
# plt.show()

# param_run = BatchRunner(ForestFire, param_set, iterations=5, model_reporters=model_reporter)
# param_run.run_all()
# df = param_run.get_model_vars_dataframe()
# plt.scatter(df.density, df.BurnedOut)
# plt.xlim(0,1)
# plt.show()
