from isicpy.third_party.pymatreader import hdf5todict
from isicpy.utils import makeFilterCoeffsSOS
from pathlib import Path
import h5py
import pandas as pd
import ephyviewer
import numpy as np
from scipy import signal

# clinc_sample_rate = 36931.8
clinc_sample_rate = 36931.71326217823

emg_sample_rate = 500
dsi_trigs_sample_rate = 1000

filterOpts = {
    'low': {
        'Wn': 100.,
        'N': 2,
        'btype': 'low',
        'ftype': 'butter'
    }
}
filterCoeffs = makeFilterCoeffsSOS(filterOpts.copy(), emg_sample_rate)
def visualize_dataset():
    app = ephyviewer.mkQApp()
    win = ephyviewer.MainViewer(debug=False)

    # folder_path = Path(r"/users/rdarie/data/rdarie/Neural Recordings/raw/20231109-Phoenix")
    # file_name = "MB_1699558933_985097"
    # file_name = "MB_1699560317_650555"
    # file_name = 'MB_1699560792_657674'

    # emg_block_name = "Block0002"
    # emg_block_name = "Block0001"

    folder_path = Path("/users/rdarie/data/rdarie/Neural Recordings/raw/202311221100-Phoenix")
    file_name_list = [
        'MB_1700670158_174163', 'MB_1700671071_947699', 'MB_1700671568_714180',
        'MB_1700672329_741498', 'MB_1700672668_26337', 'MB_1700673350_780580'
        ]
    file_name = 'MB_1700673350_780580'
    emg_block_name = "Block0005"

    file_timestamp_parts = file_name.split('_')
    file_start_time = pd.Timestamp(float('.'.join(file_timestamp_parts[1:3])), unit='s', tz='EST')

    clinc_df = pd.read_parquet(folder_path / (file_name + '_clinc.parquet'))
    clinc_df.index = clinc_df.index + file_start_time
    clinc_trigs = pd.read_parquet(folder_path / (file_name + '_clinc_trigs.parquet'))
    clinc_trigs.index = clinc_trigs.index + file_start_time

    emg_df = pd.read_parquet(folder_path / f"{emg_block_name}_emg.parquet")
    dsi_trigs = pd.read_parquet(folder_path / f"{emg_block_name}_dsi_trigs.parquet")

    dsi_coarse_offset = 115
    dsi_fine_offset = 0.6465
    t_zero = file_start_time
    t_start_dsi = (emg_df.index[0] - t_zero).total_seconds() + dsi_coarse_offset + dsi_fine_offset

    t_start_clinc = (file_start_time - t_zero).total_seconds()

    apply_emg_filters = True
    if apply_emg_filters:
        emg_signals_source = ephyviewer.InMemoryAnalogSignalSource(
            signal.sosfiltfilt(filterCoeffs, emg_df.to_numpy() ** 2, axis=0),
            emg_sample_rate, t_start_dsi, channel_names=emg_df.columns)
    else:
        emg_signals_source = ephyviewer.InMemoryAnalogSignalSource(
            emg_df.to_numpy(),
            emg_sample_rate, t_start_dsi, channel_names=emg_df.columns)

    emg_signals_view = ephyviewer.TraceViewer(source=emg_signals_source, name='emg')
    emg_signals_view.params_controller.on_automatic_color(cmap_name='Set3')

    dsi_trigs_source = ephyviewer.InMemoryAnalogSignalSource(
        dsi_trigs.to_numpy(), dsi_trigs_sample_rate, t_start_dsi, channel_names=dsi_trigs.columns)
    trig_view = ephyviewer.TraceViewer(source=dsi_trigs_source, name='emg_trig')
    trig_view.params_controller.on_automatic_color(cmap_name='Set3')

    clinc_source = ephyviewer.InMemoryAnalogSignalSource(
        clinc_df.to_numpy(), clinc_sample_rate, t_start_clinc, channel_names=clinc_df.columns)
    clinc_view = ephyviewer.TraceViewer(source=clinc_source, name='clinc')
    clinc_view.params_controller.on_automatic_color(cmap_name='Set3')

    clinc_trig_source = ephyviewer.InMemoryAnalogSignalSource(
        clinc_trigs.to_numpy(), clinc_sample_rate, t_start_clinc, channel_names=clinc_trigs.columns)
    clinc_trig_view = ephyviewer.TraceViewer(source=clinc_trig_source, name='clinc_trigs')
    clinc_trig_view.params_controller.on_automatic_color(cmap_name='Set3')

    win.add_view(emg_signals_view)
    win.add_view(clinc_view, split_with='emg', orientation='vertical')
    win.add_view(trig_view, tabify_with='emg')
    win.add_view(clinc_trig_view, tabify_with='clinc')

    win.show()
    app.exec_()


if __name__ == '__main__':
    visualize_dataset()
