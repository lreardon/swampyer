from Tkinter import *
from BehaviorWorld import *

root = Tk()
root.title("BehaviorWorld Setup")

def run_sim():
    print(default_behavior.get())
    sim = BehaviorWorld(topology.get(), int(world_length_box.get()), int(world_width_box.get()), int(cell_size_box.get()), int(canvas_size_box.get()), behaviors[default_behavior.get()], configurations[d_configuration.get()], name.get(), backup.get())

toolbar = Frame(root)
top_pane = Frame(toolbar)
middle_pane = Frame(toolbar)
bottom_pane = Frame(toolbar)

world_length_select = Frame(top_pane)
world_length_label = Label(world_length_select, text="World Length", pady=3)
world_length_label.pack(side=TOP)
world_length = IntVar(value=15)
world_length_box = Entry(world_length_select, textvariable=world_length)
world_length_box.pack(side=BOTTOM)
world_length_select.pack(side=LEFT, padx=2, pady=2)

world_width_select = Frame(top_pane)
world_width_label = Label(world_width_select, text="World Width", pady=3)
world_width_label.pack(side=TOP)
world_width = IntVar(value=15)
world_width_box = Entry(world_width_select, textvariable=world_width)
world_width_box.pack(side=BOTTOM)
world_width_select.pack(side=LEFT, padx=2, pady=2)

cell_size_select = Frame(top_pane)
cell_size_label = Label(cell_size_select, text="Cell Size", pady=3)
cell_size_label.pack(side=TOP)
cell_size = IntVar(value=15)
cell_size_box = Entry(cell_size_select, textvariable=cell_size)
cell_size_box.pack(side=BOTTOM)
cell_size_select.pack(side=LEFT, padx=2, pady=2)

canvas_size_select = Frame(top_pane)
canvas_size_label = Label(canvas_size_select, text="Canvas Size", pady=3)
canvas_size_label.pack(side=TOP)
canvas_size = IntVar(value=600)
canvas_size_box = Entry(canvas_size_select, textvariable=canvas_size)
canvas_size_box.pack(side=BOTTOM)
canvas_size_select.pack(side=LEFT, padx=2, pady=2)

topology_select = Frame(middle_pane)
topology_label = Label(topology_select, text="Topology", pady=3)
topology_label.pack(side=TOP)
topology = StringVar()
topology_options = Frame(topology_select)
Radiobutton(topology_options, text='infinite-plane', variable=topology, value='infinite-plane', indicatoron=0, width=15).pack(anchor=W)
Radiobutton(topology_options, text='infinite-ribbon', variable=topology, value='infinite-ribbon', indicatoron=0, width=15).pack(anchor=W)
Radiobutton(topology_options, text='rectangle', variable=topology, value='rectangle', indicatoron=0, width=15).pack(anchor=W)
Radiobutton(topology_options, text='infinite-cylinder', variable=topology, value='infinite-cylinder', indicatoron=0, width=15).pack(anchor=W)
Radiobutton(topology_options, text='finite-plane', variable=topology, value='finite-plane', indicatoron=0, width=15).pack(anchor=W)
Radiobutton(topology_options, text='torus', variable=topology, value='torus', indicatoron=0, width=15).pack(anchor=W)
topology.set('torus')
topology_options.pack(side=BOTTOM)
topology_select.pack(side=LEFT, anchor=N, padx=2, pady=2)

configuration_select = Frame(middle_pane)
configuration_label = Label(configuration_select, text="Initial Configuration", pady=3)
configuration_label.pack(side=TOP)
configuration_options = Frame(configuration_select)
d_configuration = StringVar()
configurations_dict = {}
for configuration in configurations:
    configurations_dict[configuration] = Radiobutton(configuration_options, text=configuration, variable=d_configuration, value=configuration, indicator=0, width=40)
    configurations_dict[configuration].pack(anchor=W)
configurations_dict['ten_dustmites_random_on_random_shades'].select()
configuration_options.pack(side=BOTTOM)
configuration_select.pack(side=LEFT, anchor=N, padx=2, pady=2)

default_behavior_select = Frame(middle_pane)
default_behavior_label = Label(default_behavior_select, text="Default Behavior", pady=3)
default_behavior_label.pack(side=TOP)
default_behavior_options = Frame(default_behavior_select)
default_behavior = StringVar()
behaviors_dict = {}
for behavior in behaviors:
    behaviors_dict[behavior] = Radiobutton(default_behavior_options, text=behavior, variable=default_behavior, value=behavior, indicatoron=0, width=20)
    behaviors_dict[behavior].pack(anchor=W)
behaviors_dict['eat_dust'].select()
default_behavior_options.pack(side=BOTTOM)
default_behavior_select.pack(side=LEFT, anchor=N, padx=2, pady=2)

name_select = Frame(bottom_pane)
name_label = Label(name_select, text="Model Name", pady=3)
name_label.pack(side=TOP)
name = StringVar(value='test')
name_box = Entry(name_select, textvariable=name)
name_box.pack(side=BOTTOM)
name_select.pack(side=LEFT, padx=2, pady=2)

backup_select = Frame(bottom_pane)
backup_label = Label(backup_select, text="Save this model?", pady=3)
backup_label.pack(side=TOP)
backup_options = Frame(backup_select)
backup = BooleanVar()
backup_dict = {}
backup_dict['yes'] = Radiobutton(backup_options, text='Yes', variable=backup, value=True, indicatoron=0, width=15)
backup_dict['yes'].pack(anchor=W)
backup_dict['no'] = Radiobutton(backup_options, text='No', variable=backup, value=False, indicatoron=0, width=15)
backup_dict['no'].pack(anchor=W)
backup_dict['no'].select()
backup_options.pack(side=BOTTOM)
backup_select.pack(side=LEFT, padx=2, pady=2)

run = Button(bottom_pane, text="Run", width=20, command=run_sim)
run.pack(side=RIGHT, padx=(100,0))

top_pane.pack(side=TOP, anchor=CENTER, pady=5)
middle_pane.pack(side=TOP, anchor=CENTER, pady=5)
bottom_pane.pack(side=TOP, anchor=CENTER, pady=5)
toolbar.pack(side=TOP, fill=X)

root.mainloop()
