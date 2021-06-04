import os
import numpy as np
import utils.pickle_utils as pickle_utils




CONFIG = {
    "DROP_FRAME_AFTER_STEP": 2,
    "THRESHOLD": 0.1,
    "FACES": {
        "VECTORS": np.array(list(feature_vectors.values())),
        "NAMES": list(feature_vectors.keys())
    }
}
