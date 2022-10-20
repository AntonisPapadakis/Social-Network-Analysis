import os

current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
data_dir = os.path.join(parent_dir, "data")
graphs_dir = os.path.join(data_dir, "graphs")
plots_dir = os.path.join(data_dir, "plots")
layouts_dir = os.path.join(data_dir, "full search layouts")
simulated_layouts_dir = os.path.join(data_dir, "simulated annealing layouts")
tables_dir = os.path.join(data_dir, "tables")
