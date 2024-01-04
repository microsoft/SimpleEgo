"""Download and prepare the SynthEgo dataset.

MANO and AMASS parts from MPII licenses prohibit redistribution, so this script downloads from the
official source and splices in the correct data.
"""
import subprocess
import sys
import json
from typing import Optional
from pathlib import Path
from getpass import getpass
from zipfile import ZipFile
import tarfile

import numpy as np

MANO_N_J = 15
SMPL_H_N_J = 22
LEFT_HAND = SMPL_H_N_J
RIGHT_HAND = SMPL_H_N_J + MANO_N_J

MANO_FILENAME = "manoposesv10"
MOSH_FILENAME = "MoSh"
POSELIM_FILENAME = "PosePrior"
SYNTHEGO_DIRNAME = "SynthEgo"


def _download_mpii_file(
    username: str, password: str, domain: str, file: str, out_path: Path
) -> None:
    out_path.parent.mkdir(exist_ok=True, parents=True)
    url = f"https://download.is.tue.mpg.de/download.php?domain={domain}&resume=1&sfile={file}"
    try:
        subprocess.check_call(
            [
                "wget",
                "--post-data",
                f"username={username}&password={password}",
                url,
                "-O",
                out_path.as_posix(),
                "--no-check-certificate",
                "--continue",
            ]
        )
    except subprocess.CalledProcessError:
        print("Download failed, check your login details")
        if out_path.exists():
            out_path.unlink()
        exit(1)


def get_mano(out_dir: Path) -> None:
    """Download MANO data."""
    print("Downloading MANO...")
    username = input("Username: ")
    password = getpass("Password: ")
    _download_mpii_file(
        username,
        password,
        "mano",
        f"{MANO_FILENAME}.zip",
        out_dir / f"{MANO_FILENAME}.zip",
    )


def get_amass(out_dir: Path) -> None:
    """Download AMASS data."""
    print("Downloading AMASS...")
    username = input("Username: ")
    password = getpass("Password: ")
    _download_mpii_file(
        username,
        password,
        "amass",
        f"amass_per_dataset/smplh/gender_specific/mosh_results/{MOSH_FILENAME}.tar.bz2",
        out_dir / f"{MOSH_FILENAME}.tar.bz2",
    )
    _download_mpii_file(
        username,
        password,
        "amass",
        f"amass_per_dataset/smplh/gender_specific/mosh_results/{POSELIM_FILENAME}.tar.bz2",
        out_dir / f"{POSELIM_FILENAME}.tar.bz2",
    )


def extract(data_path: Path, out_path: Optional[Path] = None) -> None:
    """Extract the data from the given path."""
    print(f"Extracting {data_path.name}...")
    if data_path.suffix == ".zip":
        out_path = out_path or data_path.parent / data_path.stem
        with ZipFile(data_path) as f:
            f.extractall(out_path)
    elif data_path.suffix == ".bz2":
        out_path = out_path or data_path.parent / data_path.name.replace(".tar.bz2", "")
        with tarfile.open(data_path, "r:bz2") as f:
            f.extractall(out_path)
    else:
        raise ValueError(f"Unknown file type {data_path.suffix}")


def download_synthego(out_dir: Path) -> None:
    """Download the SynthEgo dataset."""
    out_dir.mkdir(exist_ok=True, parents=True)
    for part in range(1, 11):
        out_path = out_dir / f"synth_ego_{part:02d}.zip"
        print(f"Downloading SynthEgo part {part}...")
        url = f"https://facesyntheticspubwedata.blob.core.windows.net/3dv-2024/synth_ego_{part:02d}.zip"
        try:
            subprocess.check_call(
                [
                    "wget",
                    url,
                    "-O",
                    str(out_path),
                    "--no-check-certificate",
                    "--continue",
                ]
            )
        except subprocess.CalledProcessError:
            print("Download failed")
            if out_path.exists():
                out_path.unlink()
            exit(1)


def main() -> None:
    """Download and process the dataset."""
    assert len(sys.argv) == 2, "Usage: python process_pose_gt.py <output_dir>"
    data_dir = Path(sys.argv[1])
    # download data from MPII sources
    get_amass(data_dir)
    get_mano(data_dir)
    # extract the data
    for path in list(data_dir.glob("*.zip")) + list(data_dir.glob("*.bz2")):
        extract(path)
        path.unlink()
    # download the SynthEgo dataset
    zip_dir = data_dir / f"{SYNTHEGO_DIRNAME}_zip"
    download_synthego(zip_dir)
    # extract the SynthEgo dataset
    for path in list(zip_dir.glob("*.zip")):
        extract(path, data_dir / SYNTHEGO_DIRNAME)
        path.unlink()
    zip_dir.rmdir()
    # load MANO dataset
    mano_left = np.load(
        data_dir
        / f"{MANO_FILENAME}/mano_poses_v1_0/handsOnly_REGISTRATIONS_r_lm___POSES___L.npy"
    )
    mano_right = np.load(
        data_dir
        / f"{MANO_FILENAME}/mano_poses_v1_0/handsOnly_REGISTRATIONS_r_lm___POSES___R.npy"
    )
    # fill in the data
    for metadata_fn in (data_dir / SYNTHEGO_DIRNAME).glob("*.json"):
        with open(metadata_fn, "r") as f:
            metadata = json.load(f)
            if isinstance(metadata["pose"][1], str):
                # body pose comes from AMASS
                seq_name: str = metadata["pose"][1]
                frame = int(seq_name.split("_")[-2])
                mirrored = seq_name.split("_")[-1] == 1
                assert not mirrored
                seq_path = Path("/".join(seq_name.split("/")[1:])).with_suffix(".npz")
                if seq_name.startswith("MoSh_MPI_MoSh"):
                    seq_data = np.load(data_dir / MOSH_FILENAME / seq_path)
                elif seq_name.startswith("MoSh_MPI_PoseLimits"):
                    seq_data = np.load(data_dir / POSELIM_FILENAME / seq_path)
                else:
                    raise RuntimeError(f"Unknown sequence name {seq_name}")
                # we resampled to ~30 fps so have to adjust the frame number
                frame_step = int(np.floor(seq_data["mocap_framerate"] / 30))
                seq = seq_data["poses"][::frame_step]
                # exclude root joint
                metadata["pose"][1:SMPL_H_N_J] = (
                    seq[frame].reshape((-1, 3))[1:SMPL_H_N_J].tolist()
                )
            if isinstance(metadata["pose"][LEFT_HAND], str):
                # left hand comes from MANO
                idx = int(metadata["pose"][LEFT_HAND].split("_")[1])
                metadata["pose"][LEFT_HAND:RIGHT_HAND] = (
                    mano_left[idx].reshape((MANO_N_J, 3)).tolist()
                )
            if isinstance(metadata["pose"][RIGHT_HAND], str):
                # right hand comes from MANO
                idx = int(metadata["pose"][RIGHT_HAND].split("_")[1])
                metadata["pose"][RIGHT_HAND:] = (
                    mano_right[idx].reshape((MANO_N_J, 3)).tolist()
                )
        with open(metadata_fn, "w") as f:
            json.dump(metadata, f, indent=4)


if __name__ == "__main__":
    main()
