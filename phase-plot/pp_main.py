from pp_config_loader import *
from pp_manager import *
from pp_drawer import *

pp_config_loader = PPConfigLoader('config.json')
pp_config_loader.description()

pp_drawer = PPDrawer()

for pp_config in pp_config_loader.config:
    pp_single_manager = PPManager(pp_config)
    pp_single_manager.description()
    pp_single_manager.generate_image()

    pp_drawer.make_phase_plot(pp_single_manager)