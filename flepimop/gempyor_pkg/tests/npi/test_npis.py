import gempyor
import numpy as np
import pandas as pd
import datetime
import pytest

from gempyor.utils import config

import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import glob, os, sys, shutil
from pathlib import Path

# import seaborn as sns
import pyarrow.parquet as pq
import pyarrow as pa
from gempyor import file_paths, outcomes

config_path_prefix = ""

os.chdir(os.path.dirname(__file__))


def test_full_npis_read_write():
    os.chdir(os.path.dirname(__file__))

    inference_simulator = gempyor.InferenceSimulator(
        config_path=f"{config_path_prefix}config_npi.yml",
        run_id=105,
        prefix="",
        first_sim_index=1,
        outcome_scenario="med",
        npi_scenario="inference",
        stoch_traj_flag=False,
        out_run_id=105,
    )
    # inference_simulator.one_simulation(sim_id2write=1,load_ID=False)

    # outcomes.onerun_delayframe_outcomes(
    #    sim_id2write=1, s=inference_simulator.s, load_ID=False, sim_id2load=1
    # )

    npi_outcomes = outcomes.build_npi_Outcomes(inference_simulator.s, load_ID=False, sim_id2load=None, config=config)
    # npi_seir = seir.build_npi_SEIR(
    #    inference_simulator.s, load_ID=False, sim_id2load=None, config=config
    # )

    inference_simulator.s.write_simID(ftype="hnpi", sim_id=1, df=npi_outcomes.getReductionDF())

    hnpi_read = pq.read_table(f"{config_path_prefix}model_output/hnpi/000000001.105.hnpi.parquet").to_pandas()
    hnpi_read["reduction"] = np.random.random(len(hnpi_read)) * 2 - 1
    out_hnpi = pa.Table.from_pandas(hnpi_read, preserve_index=False)
    pa.parquet.write_table(out_hnpi, file_paths.create_file_name(105, "", 1, "hnpi", "parquet"))
    import random

    random.seed(10)

    inference_simulator = gempyor.InferenceSimulator(
        config_path=f"{config_path_prefix}config_npi.yml",
        run_id=105,
        prefix="",
        first_sim_index=1,
        outcome_scenario="med",
        npi_scenario="inference",
        stoch_traj_flag=False,
        out_run_id=106,
    )
    # shutil.move('model_output/seir/000000001.105.seir.parquet', 'model_output/seir/000000001.106.seir.parquet')

    # outcomes.onerun_delayframe_outcomes(
    #    sim_id2write=1, s=inference_simulator.s, load_ID=True, sim_id2load=1
    # )

    npi_outcomes = outcomes.build_npi_Outcomes(inference_simulator.s, load_ID=True, sim_id2load=1, config=config)
    inference_simulator.s.write_simID(ftype="hnpi", sim_id=1, df=npi_outcomes.getReductionDF())

    hnpi_read = pq.read_table(f"{config_path_prefix}model_output/hnpi/000000001.105.hnpi.parquet").to_pandas()
    hnpi_wrote = pq.read_table(f"{config_path_prefix}model_output/hnpi/000000001.106.hnpi.parquet").to_pandas()
    assert (hnpi_read == hnpi_wrote).all().all()

    # runs with the new, random NPI
    inference_simulator = gempyor.InferenceSimulator(
        config_path=f"{config_path_prefix}config_npi.yml",
        run_id=106,
        prefix="",
        first_sim_index=1,
        outcome_scenario="med",
        stoch_traj_flag=False,
        out_run_id=107,
    )
    # shutil.move('model_output/seir/000000001.106.seir.parquet', 'model_output/seir/000000001.107.seir.parquet')

    # outcomes.onerun_delayframe_outcomes(
    #    sim_id2write=1, s=inference_simulator.s, load_ID=True, sim_id2load=1
    # )

    npi_outcomes = outcomes.build_npi_Outcomes(inference_simulator.s, load_ID=True, sim_id2load=1, config=config)
    inference_simulator.s.write_simID(ftype="hnpi", sim_id=1, df=npi_outcomes.getReductionDF())

    hnpi_read = pq.read_table(f"{config_path_prefix}model_output/hnpi/000000001.106.hnpi.parquet").to_pandas()
    hnpi_wrote = pq.read_table(f"{config_path_prefix}model_output/hnpi/000000001.107.hnpi.parquet").to_pandas()
    assert (hnpi_read == hnpi_wrote).all().all()


def test_spatial_groups_isolation():
    inference_simulator = gempyor.InferenceSimulator(
        config_path=f"{config_path_prefix}config_test_spatial_group_npi.yml",
        run_id=105,
        prefix="",
        first_sim_index=1,
        outcome_scenario="med",
        npi_scenario="inference",
        stoch_traj_flag=False,
        out_run_id=105,
    )