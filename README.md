# DONALD-VAMBN

This is a modified version of VAMBN from [GitHub](https://github.com/elg34/VAMBN).

It will include a small dummy data file for testing.

It will include modified scripts which work with the dummy data file, and with the DONALD data.



## Setup Notes

Last used with tensorflow 1.15.5

Remember deleting DELETE_PLACEHOLDER files


## Usage Notes

Fruit data CSV is included. To generate DONALD data CSV from SAS file, run `donald_loader.py` after correctly setting its path

To run, execute the following files, where ??? is your dataset.`fruit` is being implemented, `donald` coming soon.

- `clean_format_???.R`
- `impute_aux_???.R`
- `HI-VAE/1_???_HIVAE_training.py` (make sure to set sample_size)
- `bnet_???.R`
- `HI-VAE/2_???_HIVAE_VP_decoding_and_counterfactuals.py` (set sample_size)