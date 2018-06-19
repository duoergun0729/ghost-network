import os

import tensorflow.contrib.slim.nets as nets

from config import config as FLAGS
from networks.lib.lib_resnet_v2_101_fix import resnet_v2_101

_CHECKPOINT_NAME = 'resnet_v2_101.ckpt'
checkpoint_path = os.path.join(
    FLAGS.checkpoint_path,
    _CHECKPOINT_NAME
)

arg_scope = nets.resnet_v2.resnet_arg_scope(weight_decay=0.0)
func = resnet_v2_101
