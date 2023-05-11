# DONALD-VAMBN

This is a modified version of VAMBN from [GitHub](https://github.com/elg34/VAMBN). Its purpose is applying the method to the [DONALD](https://www.ernaehrungsepidemiologie.uni-bonn.de/forschung/donald-1) study data.

For educational and testing purposes, a small dummy data file is also included: `data/fruit-data.csv`

This repo includes modified scripts for both the fruit and the DONALD data.

There are also scripts for plotting and other useful evaluations of the data available: `evaluation_scripts/`



## Setup Notes

Last used with:
- tensorflow 1.14.0
- Keras 2.3.1 (only required for LSTM branches)


## Usage Notes

To start, a suitable data file is required. The fruit data CSV is included, but the private DONALD data can not be part of this repository. To generate the usable DONALD data CSV from a DONALD SAS file, use `donald_loader.py`

To run the pipeline, execute the following files, where ??? is your dataset (`fruit` or `donald`).

- `clean_format_???.R`
  - Defines variable groups and standalone variables
- `impute_aux_???.R`
  - Reformats data and finds missingness
- `HI-VAE/1_???_HIVAE_training.py` (make sure to set sample_size)
  - Trains a HI-VAE for every module (16 visits * 4 variable groups = 64 modules for DONALD)
  - Reconstructs participants from the original participant encodings (real participants, RPs)
- `bnet_???.R`
  - Learns the BNet structure and parameters
  - Draws virtual participant codes from the BNet
  - For DONALD, it is suggested to use `make_bl_wl_donald.py` instead of the equivalent R script. To do this, run `bnet_donald.R` until `data_names.csv` is written, stop it and run the BL/WL script, then rerun the BNet script.
  - If the Tabu search produces errors, it is suggested to also try switching from `tabu` to the `hc` algorithm (for both "Final bayesian network" and "Bootstrapped network")
- `HI-VAE/2_???_HIVAE_VP_decoding_and_counterfactuals.py` (set sample_size)
  - Reconstructs drawn encodings (virtual participants, VPs)

To reformat the RPs or VPs into the original DONALD format, use `donald_writer.py`
