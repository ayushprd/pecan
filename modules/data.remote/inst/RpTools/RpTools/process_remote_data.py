#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
process_remote_data controls functions which perform further computation on the data.
Requires Python3
Author: Ayush Prasad
"""
from RpTools.merge_files import nc_merge
from importlib import import_module
import os
import time

def process_remote_data(aoi_name, out_get_data, out_process_data, outdir, algorithm, input_file, siteid=None, pro_merge=None, existing_pro_file_path=None):
    """
    uses processing functions to perform computation on input data
    
    Parameters
    ----------
    aoi_name (str) -- name to the AOI.
    output (dict) -- dictionary contatining the keys get_data and process_data
    outdir (str) -- path to the directory where the output file is stored. If specified directory does not exists, it is created.
    algorithm (str) -- name of the algorithm used to perform computation.
    inputfile (str) -- path to raw file
    siteid (str) -- shortform of the siteid
    pro_merge (str) -- if the pro file has to be merged
    existing_pro_file_path -- path to existing pro file if pro_merge is TRUE
    
    Returns
    -------
    Absolute path to the output file

    output netCDF is saved in the specified directory.
    """
    

    # get the type of the input data
    input_type = out_get_data
    # locate the input file
    # input_file = os.path.join(outdir, aoi_name, "_", input_type, ".nc")
    # extract the computation which is to be done
    output = out_process_data
    # construct the function name
    func_name = "".join([input_type, "2", output, "_", algorithm])
    # import the module
    module_from_pack = "RpTools" + "." + func_name
    module = import_module(module_from_pack)
    # import the function from the module
    func = getattr(module, func_name)
    # call the function
    process_datareturn_path = func(input_file, outdir, siteid)

    if pro_merge == True and pro_merge != "replace":
        try:
            process_datareturn_path = nc_merge(existing_pro_file_path, process_datareturn_path, outdir)
        except:
            print(existing_pro_file_path)
    return process_datareturn_path