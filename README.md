![alt text](docs/img/dataset_samples.jpg)

# The SynthEgo dataset

The SynthEgo dataset was introduced in our paper [**SimpleEgo: Predicting probabilistic body pose from egocentric cameras**](https://microsoft.github.io/SimpleEgo/).

The dataset contains:
- 60,000 stereo pair synthetic RGB images from a head mounted camera at 1280x720 pixel resolution.
- SMPL-H pose and identity parameters for each stereo pair.
- 3D joint locations in world and camera space for each image.
- 2D joint locations in image space for each image.
- Camera parameters for each image.

## Downloading the dataset

You can download the dataset in parts from the folling links:
- [Part 1]()
- [Part 2]()
- [Part 3]()
- [Part 4]()
- [Part 5]()
- [Part 6]()
- [Part 7]()
- [Part 7]()
- [Part 9]()
- [Part 10]()

## Dataset layout

Once extracted, the dataset contains files for each sample of the form:
- `metadata_0000000_0000.json`
- `img_L_0000000_0000.png`
- `img_R_0000000_0000.png`

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

If you use the SynthEgo Dataset your research, please cite the following [paper](TODO):

```
@inproceedings{cuevas2024simpleego,
TODO
}
```
