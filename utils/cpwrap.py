import configparser
import sys
import os.path

project_root = "."
conf_file = os.path.join(project_root,"config")
default_conf_file = "./default_config"
default_conf = None
conf         = None

def parse_config():
        global default_conf
        global conf
        conf = configparser.ConfigParser()
        conf.read(conf_file)
        default_conf = configparser.ConfigParser()
        default_conf.read(default_conf_file)
        
        if conf == None or (len(conf.sections()) == 0 and len(default_conf.sections()) == 0):
                print("Error: Missing configuration file at '{}'".format(\
                                os.path.abspath(conf_file)))
                raise Exception("Missing configuration file")

def get_keys(like=None):
        ret = conf["all"].keys()
        if like != None:
            ret = list(filter(lambda x:like in x,ret))
            if len(ret) == 0:
                print("No options that contain the string '%s'"%like)
                return ""
        return ret

def change_cfg(key,value):
        global conf
        confs = conf["all"]
        key = str(key)
        if key not in confs:
            return False
        else:
            confs[key] = str(value)
            return True

def CFG(tag):
        global conf
        global default_conf
        
        if conf == None:
                parse_config()
        if len(default_conf.sections()) > 0:
                default_confs = default_conf["all"]
        else:
                default_confs = None
        confs = conf["all"]
        
        if tag in confs:
                return parse_cfg(confs[tag])
        elif default_confs != None and tag in default_confs:
                print("Warning: %s no found in configuration, defaulting to %s" % (str(tag),str(default_conf[tag])),file=sys.stderr)
                return parse_cfg(default_confs[tag])
        else:
                raise Exception("Error: configuration option %s not found in configuration and no default value for it, cannot continue, exit." % str(tag))

def parse_cfg(c):
        if c == None:
                raise Exception("Config key (%s) found but has no value. Cannot continue, exit." % str(c))
        c = c.strip("'")
        c = c.strip('"')
        if c in ["yes","True","Yes","true"]:
                return True
        if c in ["no","False","No","false"]:
                return False
        try:
                return int(c.replace(" ",""))
        except ValueError:
                pass
        try:
                return float(c)
        except ValueError:
                pass
        return c
