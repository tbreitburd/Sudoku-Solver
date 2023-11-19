import sys
import configparser as cfg

input_file = sys.argv[1]

config = cfg.ConfigParser()
config.read(input_file)