import importlib
module = 'core.event.init_ap_scheduler'
kwargs = {}
module_pag = importlib.import_module(module[0:module.rindex(".")])
print(module_pag,"module_pag",module[module.rindex(".") + 1:])
a = getattr(module_pag, module[module.rindex(".") + 1:])(**kwargs)