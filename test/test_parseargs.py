#!/usr/bin/python3
import operator, types
import sys, getopt
import json
import os
sys.path.append(os.getcwd())
sys.path.append("..")
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../"))
from src.parseargs import parseargs

def print_args(*args, **kwargs):
    print(f"args info: {args} {kwargs}")

def none_args():
    print_args()

def none_default_args(count, name):
    print(f"count = {count} name = {name}")

def had_default_args(count, name, age = 12, state = True, area = "beijing"):
    print_args(count, name, age, state, area)

def had_args_kwargs(count, name, *args, **kwargs):
    print_args(count, name, *args, **kwargs)

def no_use_func_args(name, age, area):
    print(f"no_use_func_args")
    print_args(name, age, area)

def init_args(pargs):
    pargs.append("help", "show arg list.")
    pargs.append("conf", "config file path name. default:bvexchange.toml, find from . and /etc/bvexchange/", True, "toml file", priority = 5)
    pargs.append(none_args, "none args")
    pargs.append(none_default_args, "none default args")
    pargs.append(had_default_args, "had default args")
    pargs.append(had_args_kwargs, "have *args and **kwargs")
    pargs.append(no_use_func_args, "here args name is not funcs arg", True, "fixed_name, fixed_age, fixed_area")
    pargs.append("use_func_args", "here args name is funcs arg", True, "name, age, area", callback = no_use_func_args)

def get_arg_info():
    argc = len(sys.argv) - 1
    argv = sys.argv[1:]
    return (argc, argv)

def test_narmal():
    try:
        argc, argv = get_arg_info()
        print(f"start main argc = {argc} argv = {argv}")
        pargs = parseargs()
        init_args(pargs)
        pargs.show_help(argv)
        opts, err_args = pargs.getopt(argv)
    except getopt.GetoptError as e:
        print(e)
        sys.exit(2)
    except Exception as e:
        print(e)
        sys.exit(2)

    #argument start for --
    if len(err_args) > 0:
        pargs.show_args()

    for opt, arg in opts:
        arg_list = []
        if len(arg) > 0:
            count, arg_list = pargs.split_arg(opt, arg)

            print("opt = {}, arg = {}".format(opt, arg_list))
        if pargs.is_matched(opt, ["conf"]):
            if len(arg_list) != 1:
                pargs.exit_error_opt(opt)
            stmanage.set_conf_env(arg_list[0])
        elif pargs.has_callback(opt):
            pargs.callback(opt, *arg_list)
        else:
            raise Exception(f"not found matched opt: {opt}")


    print("end manage.main")

def append_args(pargs):
    pargs.append("twice_args", "first append.")
    pargs.append("twice_args", "sencond append.")

def test_twice_append_args():
    try:
        argc, argv = get_arg_info()
        print(f"start main argc = {argc} argv = {argv}")
        pargs = parseargs()
        init_args(pargs)
        append_args(pargs)
        pargs.show_help(argv)
        opts, err_args = pargs.getopt(argv)
    except getopt.GetoptError as e:
        print(e)
        sys.exit(2)
    except Exception as e:
        print(e)
        sys.exit(2)

if __name__ == "__main__":
    pa = parseargs(globals())
    pa.test(sys.argv)
