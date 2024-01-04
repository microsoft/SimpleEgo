![SynthEgo dataset s](docs/img/dataset_samples.jpg)

# The SynthEgo dataset

The SynthEgo dataset was introduced in our paper [**SimpleEgo: Predicting probabilistic body pose from egocentric cameras**](https://microsoft.github.io/SimpleEgo/).

The dataset contains:

- 60,000 stereo pair synthetic RGB images from a head mounted camera at 1280x720 pixel resolution.
- [SMPL-H](https://mano.is.tue.mpg.de/) pose and identity parameters for each stereo pair.
- 3D joint locations in world and camera space for each image.
- 2D joint locations in image space for each image.
- Camera parameters for each image.

## Downloading the dataset

The license terms for the [MANO](https://mano.is.tue.mpg.de/) dataset and parts of the [AMASS](https://amass.is.tue.mpg.de/) dataset prevent redistribution.
As such, we include names and indices for these poses in the dataset we distribute, but not the pose parameters themselves.
**For simplicity, we provide a script to download the MANO, AMASS and SynthEgo datasets and splice in the relevant pose parameters automatically.**
You will need to sign up for MANO and AMASS and provide the relevant credentials when prompted by the script.
The only requirements for the script are numpy and wget, otherwise simply run `python download_dataset.py` from the command line.

You can download the dataset in parts (3GB each) directly from the following links, though *this is not recommended*:

- [Part 1](https://facesyntheticspubwedata.blob.core.windows.net/3dv-2024/synth_ego_01.zip)
- [Part 2](https://facesyntheticspubwedata.blob.core.windows.net/3dv-2024/synth_ego_02.zip)
- [Part 3](https://facesyntheticspubwedata.blob.core.windows.net/3dv-2024/synth_ego_03.zip)
- [Part 4](https://facesyntheticspubwedata.blob.core.windows.net/3dv-2024/synth_ego_04.zip)
- [Part 5](https://facesyntheticspubwedata.blob.core.windows.net/3dv-2024/synth_ego_05.zip)
- [Part 6](https://facesyntheticspubwedata.blob.core.windows.net/3dv-2024/synth_ego_06.zip)
- [Part 7](https://facesyntheticspubwedata.blob.core.windows.net/3dv-2024/synth_ego_07.zip)
- [Part 7](https://facesyntheticspubwedata.blob.core.windows.net/3dv-2024/synth_ego_08.zip)
- [Part 9](https://facesyntheticspubwedata.blob.core.windows.net/3dv-2024/synth_ego_09.zip)
- [Part 10](https://facesyntheticspubwedata.blob.core.windows.net/3dv-2024/synth_ego_10.zip)

## Dataset layout

Once extracted, the dataset contains files for each sample of the form:

- `metadata_0000000_0000.json`
- `img_L_0000000_0000.jpg`
- `img_R_0000000_0000.jpg`

Where the first number indicates the subject index from 0 to 6000, and the second number indicates the frame index from 0 to 10.
The metadata files are structured as follows:

```json
{
  "pose": [ "52x3 array of SMPL-H thetas/pose parameters" ],
  "translation": [ "3 element SMPL-H translation vector" ],
  "identity": [ "10 element SMPL-H neutral beta vector" ],
  "cameras": {
      "camera_L": {
          "world_to_camera": [ "4x4 extrinsic matrix" ],
          "camera_to_image": [ "3x3 intrinsic matrix" ],
          "resolution": [1280, 720]
      },
      "camera_R": { "as for camera_L" },
  },
  "landmarks": {
      "3D_world": [ "54x3 joint locations in world space" ],
      "3D_camera_L": [ "54x3 joint locations in camera space for camera_L" ],
      "2D_camera_L": [ "54x2 joint locations in image space for camera_L" ],
      "3D_camera_R": [ "54x3 joint locations in camera space for camera_R" ],
      "2D_camera_R": [ "54x2 joint locations in image space for camera_R" ],
  }
}
```

## Citation

If you use the SynthEgo Dataset your research, please cite the following paper:

```bibtex
@inproceedings{cuevas2024simpleego,
TODO
}
```
