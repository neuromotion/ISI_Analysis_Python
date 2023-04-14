import palettable

emg_montages = {
    'lower': {
        0: 'LVL',
        1: 'LMH',
        2: 'LTA',
        3: 'LMG',
        4: 'LSOL',
        5: 'L Forearm',
        6: 'RLVL',
        7: 'RMH',
        8: 'RTA',
        9: 'RMG',
        10: 'RSOL',
        11: 'R Forearm',
        12: 'NA',  # not connected
        13: 'NA',  # not connected
        14: 'NA',  # not connected
        15: 'Sync'
    },
    'lower_v2': {
        0: 'LVL',
        1: 'NA',  # not connected
        2: 'LTA',
        3: 'LMG',
        4: 'LSOL',
        5: 'L Forearm',
        6: 'RLVL',
        7: 'RMH',
        8: 'RTA',
        9: 'RMG',
        10: 'RSOL',
        11: 'R Forearm',
        12: 'LMH',
        13: 'NA',  # not connected
        14: 'NA',  # not connected
        15: 'Sync'
    },
    'upper': {
        0: 'L Upper Chest',
        1: 'L Lower Chest',
        2: 'L Side',
        3: 'L Biceps',
        4: 'C Forearm',
        5: 'LTA',
        6: 'R Upper Chest',
        7: 'R L Upper chest',
        8: 'R side',
        9: 'R Biceps',
        10: 'R Forearm',
        11: 'R TA',
        12: 'NA',  # not connected
        13: 'NA',  # not connected
        14: 'NA',  # not connected
        15: 'Sync'
    }
}
paired_emg_labels = ['LVL', 'RLVL', 'LMH', 'RMH', 'LTA', 'RTA', 'LMG', 'RMG', 'LSOL', 'RSOL', 'L Forearm', 'R Forearm']
emg_palette = palettable.colorbrewer.qualitative.Paired_12.mpl_colors
emg_hue_map = {
    nm: c for nm, c in zip(paired_emg_labels, emg_palette)
}



muscle_names = {
    'LVL': 'vastus',
    'LMH': 'hamstring',
    'LTA': 'tib. ant.',
    'LMG': 'gastrocnemius',
    'LSOL': 'soleus',
    'L Forearm': 'forearm',
    'RLVL': 'vastus',
    'RMH': 'hamstring',
    'RTA': 'tib. ant.',
    'RMG': 'gastrocnemius',
    'RSOL': 'soleus',
    'R Forearm': 'forearm'
}
kinematics_offsets = {
    'Day11_AM': {
        1: 0.,
        2: 0.,
        3: 0.,
        4: 0.,
    },
    'Day12_PM': {
        3: 1.6,
        4: 0.7
    },
    'Day8_AM': {
        4: 0.9
    }
}
video_info = {
    'Day8_AM': {
        4: {
            'paths': ['/users/rdarie/Desktop/Data Partition Neural Recordings/raw/ISI-C-003/6_Video/Day08_AM_Cam2_GH010042.mp4'],
            'start_timestamps': ['23:56:38:02'],
            'rollovers': [True]
        }
    },
    'Day11_AM': {
        1: {
            'paths': ['/users/rdarie/Desktop/Data Partition Neural Recordings/raw/ISI-C-003/6_Video/Day11_AM_Cam1_GH010630_NDF.mp4'],
            'start_timestamps': ['23:05:24:14'],
            'rollovers': [False]
        },
        2: {
            'paths': ['/users/rdarie/Desktop/Data Partition Neural Recordings/raw/ISI-C-003/6_Video/Day11_AM_Cam1_GH010630_NDF.mp4'],
            'start_timestamps': ['23:05:24:14'],
            'rollovers': [False]
        },
        4: {
            'paths': ['/users/rdarie/Desktop/Data Partition Neural Recordings/raw/ISI-C-003/6_Video/Day11_AM_Cam1_GH010630_NDF.mp4'],
            'start_timestamps': ['23:05:24:14'],
            'rollovers': [False]
        }
    },
    'Day12_PM': {
        4: {
            'paths': [
                '/users/rdarie/Desktop/Data Partition Neural Recordings/raw/ISI-C-003/6_Video/Day12_PM_Cam1.mp4',
                '/users/rdarie/Desktop/Data Partition Neural Recordings/raw/ISI-C-003/6_Video/Day12_PM_Cam2_GH010047_Masked.mp4',
                '/users/rdarie/Desktop/Data Partition Neural Recordings/raw/ISI-C-003/6_Video/Day12_PM_Cam3.mp4',
                ],
            'start_timestamps': ['02:36:10:16', '02:17:20:02', '02:17:47:27',],
            'rollovers': [False, False, False],
            # '/users/rdarie/Desktop/Data Partition Neural Recordings/raw/ISI-C-003/6_Video/Day12_PM_Cam2_2.mp4', '04:02:37:05'
        }
    }
}
