#!/bin/bash
GitRepoRoot="git://github.com/rdarie/"

RepoList=(\
"seaborn" \
"python-neo" \
"tridesclous" \
"ephyviewer" \
"elephant" \
"pyglmnet" \
"analysis-tools" \
"rcsanalysis" \
"peakutils" \
"umap" \
"kCSD-python" \
"scaleogram" \
"pywt" \
"scikit-lego" \
"statsmodels"
)
source ./load_ccv_modules.sh
echo "Please wait for conda to install the environment..."
conda env create -f environment.yml -v -v

echo "Please check if installation was successful"
read FILLER
chmod +x $HOME/anaconda/isi_analysis/bin/*
conda activate isi_analysis
cd ..

export PYTHONPATH="/users/rdarie/anaconda/isi_analysis/lib/python3.9/site-packages"
#
pip install pyqt5==5.10.1 --target="/users/rdarie/anaconda/isi_analysis/lib/python3.9/site-packages" --upgrade
# jupyter requires the qt console, installing after the fact to ensure the proper version
conda install jupyter --freeze-installed
conda install pyqtgraph=0.10.0 --freeze-installed
pip install vg==1.6.1 --target="/users/rdarie/anaconda/isi_analysis/lib/python3.9/site-packages" --no-deps
conda install -c conda-forge pyerfa --freeze-installed
conda install -c conda-forge astropy --freeze-installed
# pip install importlib-resources --target="/users/rdarie/anaconda/isi_analysis/lib/python3.9/site-packages" --no-deps

pip install git+git://github.com/G-Node/nixpy@v1.5.0b3 --target="/users/rdarie/anaconda/isi_analysis/lib/python3.9/site-packages" --no-deps
pip install git+git://github.com/hector-sab/ttictoc@v0.4.1 --target="/users/rdarie/anaconda/isi_analysis/lib/python3.9/site-packages" --no-deps
pip install git+git://github.com/raphaelvallat/pingouin@v0.5.0 --target="/users/rdarie/anaconda/isi_analysis/lib/python3.9/site-packages" --no-deps
pip install git+git://github.com/melizalab/libtfr --target="/users/rdarie/anaconda/isi_analysis/lib/python3.9/site-packages" --no-deps
#
# WIP
# MATLABROOT="/gpfs/runtime/opt/matlab/R2021a"
# cd "$MATLABROOT/extern/engines/python"


for i in ${RepoList[*]}; do
    echo $GitRepoRoot$i".git"
    git clone $GitRepoRoot$i".git"
    cd $i
    # git checkout tags/ndav0.3
    python setup.py develop --install-dir="/users/rdarie/anaconda/isi_analysis/lib/python3.9/site-packages" --no-deps
    cd ..
done
#
cd Data-Analysis
python setup.py develop --install-dir="/users/rdarie/anaconda/isi_analysis/lib/python3.9/site-packages" --no-deps
