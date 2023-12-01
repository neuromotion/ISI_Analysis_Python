import pandas as pd
from pathlib import Path
import json
from isicpy.utils import makeFilterCoeffsSOS, getThresholdCrossings
from scipy import signal
import numpy as np
from sklearn.preprocessing import StandardScaler

# clinc_sample_rate = 36931.8
filterOpts = {
    'high': {
        'Wn': 1000.,
        'N': 2,
        'btype': 'high',
        'ftype': 'butter'
    },
}

folder_path = Path(r"/users/rdarie/data/rdarie/Neural Recordings/raw/20231109-Phoenix")
# file_name_list = ["MB_1699558933_985097", "MB_1699560317_650555"]
file_name_list = ["MB_1699558933_985097", "MB_1699560317_650555"]
iti_lookup = {
    "MB_1699558933_985097": 3,
    "MB_1699560317_650555": 0.5,
}

folder_path = Path("/users/rdarie/data/rdarie/Neural Recordings/raw/202311221100-Phoenix")
file_name_list = [
    'MB_1700670158_174163_f.mat', 'MB_1700671071_947699_f.mat', 'MB_1700671568_714180_f.mat',
    'MB_1700672329_741498_f.mat', 'MB_1700672668_26337_f.mat', 'MB_1700673350_780580_f.mat'
    ]
iti_lookup = {
    fn: 1. for fn in file_name_list
}

for file_name in file_name_list:
    clinc_df = pd.read_parquet(folder_path / (file_name + '_f_clinc.parquet'))
    clinc_sample_rate = (float(np.median(np.diff(clinc_df.index))) * 1e-9) ** -1

    high_pass_filter = False
    if high_pass_filter:
        filterCoeffs = makeFilterCoeffsSOS(filterOpts.copy(), clinc_sample_rate)
        clinc_df = pd.DataFrame(
            signal.sosfiltfilt(filterCoeffs, clinc_df, axis=0),
            index=clinc_df.index, columns=clinc_df.columns)

    get_derivative = True
    if get_derivative:
        clinc_df = clinc_df.diff().fillna(method='bfill')

    scaler = StandardScaler()
    scaler.fit(clinc_df)
    clinc_df = pd.DataFrame(
        scaler.transform(clinc_df),
        index=clinc_df.index, columns=clinc_df.columns)

    artifact_signal = (clinc_df ** 2).mean(axis='columns').to_frame(name='average_zscore')
    artifact_signal.to_parquet(folder_path / (file_name + '_average_zscore.parquet'))

    signal_thresh = 8.
    temp = pd.Series(artifact_signal['average_zscore'].to_numpy())
    cross_index, cross_mask = getThresholdCrossings(
        temp, thresh=signal_thresh, fs=clinc_sample_rate, iti=iti_lookup[file_name], absVal=False, keep_max=False)
    align_timestamps = artifact_signal.index[cross_mask].copy()
    file_path = folder_path / 'stim_info.json'
    with open(file_path, 'r') as f:
        stim_info_json = json.load(f)

    def assign_stim_metadata(t, stim_dict_list=None):
        for row in stim_dict_list:
            if (t > row['start_time']) & (t < row['end_time']):
                return row
        return None

    meta_dict = {}
    for ts in align_timestamps:
        ts_sec = ts.total_seconds()
        meta_dict[ts] = assign_stim_metadata(ts_sec, stim_info_json[file_name])

    # pd.concat([artifact_signal.loc[align_timestamps], artifact_signal.shift(1).loc[align_timestamps]], axis='columns')

    stim_info = pd.DataFrame(meta_dict).T
    stim_info.to_parquet(folder_path / (file_name + '_stim_info.parquet'))
