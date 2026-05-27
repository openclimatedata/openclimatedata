from ._ceds import CEDS
from ._gcb_fossil import GCB_Fossil_Emissions
from ._global_carbon_budget import Global_Carbon_Budget
from ._primap_hist import PRIMAPHIST

__all__ = [
    "PRIMAPHIST",
    "CEDS",
    "Global_Carbon_Budget",
    "GCB_Fossil_Emissions",
]

import importlib.metadata as _metadata

__version__ = _metadata.version("openclimatedata")
