#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
remote_process controls the individual functions to create an automatic workflow for downloading and performing computation on remote sensing data.

Requires Python3

Author(s): Ayush Prasad, Istem Fer
"""
from . merge_files import nc_merge, csv_merge
from . get_remote_data import get_remote_data
from . process_remote_data import process_remote_data
from . gee_utils import get_sitename
import os


def rp_control(
    geofile,
    outdir,
    start,
    end,
    source,
    collection,
    siteid=None,
    scale=None,
    projection=None,
    qc=None,
    algorithm=None,
    input_file=None,
    credfile=None,
    out_get_data=None,
    out_process_data=None,
    stage_get_data=None,
    stage_process_data=None,
    raw_merge=None,
    pro_merge=None,
    existing_raw_file_path=None,
    existing_pro_file_path=None,
):

    """
    Controls get_remote_data() and process_remote_data() to download and process remote sensing data.

    Parameters
    ----------
    geofile (str) -- path to the file containing the name and coordinates of ROI, currently tested with geojson. 
    
    outdir (str) -- path to the directory where the output file is stored. If specified directory does not exists, it is created.
  
    start (str) -- starting date of the data request in the form YYYY-MM-DD
    
    end (str) -- ending date area of the data request in the form YYYY-MM-DD

    source (str) -- source from where data is to be downloaded, e.g. "gee" or "appeears" 

    collection (str) -- dataset or product name as it is provided on the source, e.g. "COPERNICUS/S2_SR" for gee or "SPL3SMP_E.003" for appeears
    
    siteid(str) -- short form of the siteid , None by default

    scale (int) -- pixel resolution, None by default, recommended to use 10 for Sentinel 2 , None by default

    projection (str) -- type of projection. Only required for appeears polygon AOI type. None by default. 

    qc (float) -- quality control parameter, only required for gee queries, None by default

    algorithm (str) -- algorithm used for processing data in process_data(), currently only SNAP is implemented to estimate LAI from Sentinel-2 bands, None by default

    credfile (str) -- path to JSON file containing Earthdata username and password, only required for AppEEARS, None by default

    out_get_data (str) -- the type of output variable requested from get_data module , None by default
    
    out_process_data (str) -- the type of output variable requested from process_data module, None by default

    stage_get_data (str) -- stage for get_data module, None by default
    
    stage_process_data (str) -- stage for process_data_module, None by default
    
    raw_merge (str) -- if raw file has to be merged, None by default
    
    pro_merge (str) -- if pro file has to be merged, None by default
    
    existing_raw_file_path (str) -- path to existing raw file , None by default
    
    existing_pro_file_path (str) -- path to existing pro file path, None by default
  
    Returns
    -------
    dictionary containing raw_id, raw_path, pro_id, pro_path

    """

    aoi_name = get_sitename(geofile)
    get_datareturn_path = 78

    if stage_get_data:
        get_datareturn_path = get_remote_data(
            geofile,
            outdir,
            start,
            end,
            source,
            collection,
            siteid,
            scale,
            projection,
            qc,
            credfile,
            raw_merge,
            existing_raw_file_path,
        )
        get_datareturn_name = os.path.split(get_datareturn_path)

    if stage_process_data:
        if input_file is None:
            input_file = get_datareturn_path
        process_datareturn_path = process_remote_data(
            aoi_name,
            out_get_data,
            out_process_data,
            outdir,
            algorithm,
            input_file,
            siteid,
            pro_merge,
            existing_pro_file_path,
        )
        process_datareturn_name = os.path.split(process_datareturn_path)

    output = {
        "raw_data_name": None,
        "raw_data_path": None,
        "process_data_name": None,
        "process_data_path": None,
    }

    if stage_get_data:
        output["raw_data_name"] = get_datareturn_name[1]
        output["raw_data_path"] = get_datareturn_path

    if stage_process_data:
        output["process_data_name"] = process_datareturn_name[1]
        output["process_data_path"] = process_datareturn_path

    return output