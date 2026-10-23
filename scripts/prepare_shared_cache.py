#!/usr/bin/env python
"""講師一次性準備：全班共享快取（課程伺服器 /home/pipcache）。

開課前執行一次（需已 `pixi install`）：

    cd ~/practice_seg
    pixi run python scripts/prepare_shared_cache.py

準備內容：
  /home/pipcache/nnUNet_raw/Dataset101_MedDDPM
      由 /Public/train/med-ddpm-1 建立（labels 2 -> 1、dataset.json），
      imagesTs 由 /Public/train/med-ddpm-2 複製。
  /home/pipcache/nnUNet_preprocessed
      nnUNetv2_plan_and_preprocess -d 101 的結果（全班相同，可共用）。
  /home/pipcache/.totalsegmentator
      TotalSegmentator 模型權重（total + teeth，已存在則跳過下載）。

準備後三個目錄對 pipcache 群組設為唯讀，學生無法改動。
學生端零操作：
  - 1-totalsegmentator.ipynb 已將 TOTALSEG_HOME_DIR 指向共享目錄。
  - 2-nnunet.ipynb 會自動把準備好的 nnUNet_raw / nnUNet_preprocessed
    symlink 進 ~/practice_seg，對應的建立 / 前處理 cell 偵測到已準備
    完成會自動跳過。nnUNet_results（訓練結果）仍是學生各自本地目錄。
"""

import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
from pathlib import Path

import nibabel as nib
import numpy as np

SHARED = Path("/home/pipcache")
PUBLIC = Path("/Public")

RAW = SHARED / "nnUNet_raw"
PRE = SHARED / "nnUNet_preprocessed"
TSEG = SHARED / ".totalsegmentator"
DATASET = RAW / "Dataset101_MedDDPM"
BIN = Path(sys.prefix) / "bin"


def build_raw():
    images_tr = DATASET / "imagesTr"
    labels_tr = DATASET / "labelsTr"
    images_ts = DATASET / "imagesTs"

    for path in [images_tr, labels_tr, images_ts]:
        path.mkdir(parents=True, exist_ok=True)

    src_images = PUBLIC / "train/med-ddpm-1/image"
    src_masks = PUBLIC / "train/med-ddpm-1/mask"

    assert src_images.is_dir(), f"找不到影像來源資料夾: {src_images}"
    assert src_masks.is_dir(), f"找不到 mask 來源資料夾: {src_masks}"

    def get_nii_files(folder):
        files = list(folder.glob("*.nii.gz"))
        files += list(folder.glob("*.nii"))
        return sorted(files)

    image_files = get_nii_files(src_images)
    mask_files = get_nii_files(src_masks)

    assert len(image_files) == len(mask_files), (
        f"影像數量 {len(image_files)} != mask 數量 {len(mask_files)}"
    )

    def strip_nii_suffix(path):
        name = path.name
        if name.endswith(".nii.gz"):
            return name[:-7]
        elif name.endswith(".nii"):
            return name[:-4]
        return path.stem

    image_map = {strip_nii_suffix(p): p for p in image_files}
    mask_map = {strip_nii_suffix(p): p for p in mask_files}

    case_keys = sorted(set(image_map) & set(mask_map))
    missing_images = sorted(set(mask_map) - set(image_map))
    assert not missing_images, f"找不到 image: {missing_images[:10]}"

    for idx, case_key in enumerate(case_keys):
        case_id = f"seg_{idx:04d}"
        shutil.copy2(image_map[case_key], images_tr / f"{case_id}_0000.nii.gz")
        shutil.copy2(mask_map[case_key], labels_tr / f"{case_id}.nii.gz")
        if (idx + 1) % 100 == 0:
            print(f"  copied {idx + 1}/{len(case_keys)} train cases")

    # labels 2 -> 1
    label_files = sorted(labels_tr.glob("*.nii.gz"))
    converted = 0
    for label_file in label_files:
        img = nib.load(label_file)
        data = np.asarray(img.dataobj)
        if (data == 2).any():
            data = np.rint(data).astype(np.uint8)
            data[data == 2] = 1
            new_img = nib.Nifti1Image(data, img.affine, img.header.copy())
            new_img.set_data_dtype(np.uint8)
            nib.save(new_img, label_file)
            converted += 1
    print(f"  labels 2 -> 1: {converted}/{len(label_files)}")

    dataset_json = {
        "channel_names": {"0": "CT"},
        "labels": {"background": 0, "seg": 1},
        "numTraining": len(list(images_tr.glob("*.nii.gz"))),
        "file_ending": ".nii.gz",
    }
    with open(DATASET / "dataset.json", "w", encoding="utf-8") as f:
        json.dump(dataset_json, f, indent=4, ensure_ascii=False)

    # imagesTs（測試集）
    test_source = PUBLIC / "train/med-ddpm-2/image"
    assert test_source.is_dir(), f"找不到測試資料來源: {test_source}"
    test_files = sorted(test_source.glob("*.nii.gz"))
    for idx, src in enumerate(test_files):
        shutil.copy2(src, images_ts / f"test_{idx:04d}_0000.nii.gz")
        if (idx + 1) % 100 == 0:
            print(f"  copied {idx + 1}/{len(test_files)} test cases")

    print(f"nnUNet_raw 準備完成: {len(case_keys)} train cases, "
          f"{len(test_files)} test cases")


def plan_and_preprocess():
    env = os.environ.copy()
    scratch_results = Path(tempfile.mkdtemp(prefix="nnunet_results_"))
    env["nnUNet_raw"] = str(RAW)
    env["nnUNet_preprocessed"] = str(PRE)
    env["nnUNet_results"] = str(scratch_results)
    env["PYTHONNOUSERSITE"] = "1"
    env.pop("PYTHONPATH", None)

    try:
        exe = BIN / "nnUNetv2_plan_and_preprocess"
        assert exe.exists(), f"找不到 nnU-Net executable:\n{exe}"

        cmd = [str(exe), "-d", "101", "--verify_dataset_integrity"]
        print("執行:", " ".join(cmd))
        subprocess.run(cmd, env=env, check=True)
    finally:
        shutil.rmtree(scratch_results, ignore_errors=True)

    print("nnUNet_preprocessed 準備完成")


def download_totalseg():
    env = os.environ.copy()
    env["TOTALSEG_HOME_DIR"] = str(TSEG)

    exe = BIN / "totalseg_download_weights"
    assert exe.exists(), f"找不到 totalseg_download_weights:\n{exe}"

    for task in ["total", "teeth"]:
        cmd = [str(exe), "-t", task]
        print("執行:", " ".join(cmd))
        subprocess.run(cmd, env=env, check=True)

    print(".totalsegmentator 權重準備完成")


def make_readonly_for_group():
    # 去除 group/other 的寫入權（/home/pipcache 對 pipcache 群組可寫，
    # 不處理的話學生可以刪除 / 改動共享資料集內容）
    for root in [RAW, PRE, TSEG]:
        count = 0
        for dirpath, dirnames, filenames in os.walk(root):
            for name in [dirpath] + dirnames + filenames:
                p = Path(dirpath) / name if name != dirpath else Path(dirpath)
                mode = p.lstat().st_mode
                p.chmod(mode & ~stat.S_IWGRP & ~stat.S_IWOTH)
                count += 1
        print(f"{root}: {count} entries set group/other read-only")


def main():
    assert PUBLIC.is_dir(), "找不到 /Public（請在課程伺服器執行）"
    assert SHARED.is_dir(), f"找不到 {SHARED}（請在課程伺服器執行）"

    print("=" * 70)
    print("1/4 建立共享 nnUNet_raw")
    print("=" * 70)
    build_raw()

    print()
    print("=" * 70)
    print("2/4 plan + preprocessing（共享 nnUNet_preprocessed）")
    print("=" * 70)
    plan_and_preprocess()

    print()
    print("=" * 70)
    print("3/4 TotalSegmentator 權重（total + teeth）")
    print("=" * 70)
    download_totalseg()

    print()
    print("=" * 70)
    print("4/4 對 pipcache 群組設為唯讀")
    print("=" * 70)
    make_readonly_for_group()

    print()
    print("共享快取準備完成：")
    print(" ", RAW)
    print(" ", PRE)
    print(" ", TSEG)


if __name__ == "__main__":
    main()