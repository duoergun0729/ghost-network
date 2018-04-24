import inspect

import_from = inspect.getframeinfo(inspect.getouterframes(inspect.currentframe())[1][0])[0]
attack_mode = 0
eval_mode = 0

if 'eval' in import_from:
    eval_mode = 1

import argparse
import os

from easydict import EasyDict as edict

config = edict()
config.random_range = 0.1  # will be change to 0.0 if mode is eval
config.attack_network = "resnet_v2_152" if 'ensemble' not in import_from else 'ensemble'
config.pgd = False
config.FGSM = False
config.restart = False
config.self_ens_num = 1

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument("--random_range", type=float, default=config.random_range)
parser.add_argument("--attack_network", type=str, default=config.attack_network)
parser.add_argument("--pgd", type=bool, default=config.pgd)
parser.add_argument("--FGSM", type=bool, default=config.FGSM)
parser.add_argument("--restart", type=bool, default=config.restart)
parser.add_argument("--self_ens_num", type=int, default=config.self_ens_num)

args = parser.parse_args()
for key, value in args.__dict__.iteritems():
    config[key] = value

config.max_epsilon = 15.0 / 255
config.step_size = 1.0 / 255 if not config.FGSM else config.max_epsilon
config.num_steps = int(min(config.max_epsilon * 255 + 4, 1.25 * config.max_epsilon * 255)) if not config.FGSM else 1
config.report_step = 100

config.attack_networks = ["resnet_v2_152", "resnet_v2_101", "resnet_v2_50"]
config.test_network = ["inception_v3", "inception_v4", "inception_resnet_v2", "resnet_v2_152", "ens3_inception_v3",
                       "ens4_inception_v3", "ens_inception_resnet_v2", "resnet_v2_101", "resnet_v2_50"]
config.test_list_filename = '../data/FlorianProject/resnet_testlist.txt'
config.ground_truth_file = '../data/FlorianProject/valid_gt.csv'
config.test_img_dir = '../data/FlorianProject/test_data/'
config.checkpoint_path = os.path.join(os.path.dirname(__file__), 'data')

if config.pgd:
    config.result_dir = 'result3/PGD_{:s}_{:.3f}'.format(config.attack_network, config.random_range)
elif config.FGSM:
    config.result_dir = 'result3/FGSM_{:s}_{:.3f}'.format(config.attack_network, config.random_range)
else:
    config.result_dir = 'result3/I-FGSM_{:s}_{:.3f}'.format(config.attack_network, config.random_range)

if config.self_ens_num > 1:
    config.result_dir += "_slfens{:d}".format(config.self_ens_num)

if eval_mode == 1:
    config.random_range = 0.0
    config.batch_size = 128 if 'ensemble' not in import_from else 128 / len(config.attack_networks)
else:
    config.batch_size = 32
    if not os.path.exists(config.result_dir):
        os.makedirs(config.result_dir)
    else:
        assert config.restart

print(config)
