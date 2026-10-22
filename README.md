# practice_seg

Medical image segmentation course material: **TotalSegmentator** (ready-made whole-body segmentation, simplified) + **nnU-Net** (train your own segmentation model with Jupyter Notebook). Environment management uses **Pixi** — no Conda / pip needed.

`practice_nnUNet` 專案已合併進本 repo（該部分的 notebook `pip_2.ipynb` 就在這裡），**不需要另外 clone practice_nnUNet**。

## 檔案內容

| 檔案 | 說明 |
|----|----|
| `步驟第二版.md` | 完整分步教程（Pixi 版），**請依照這份執行** |
| `task1-pip_2.ipynb` | TotalSegmentator 範例 notebook |
| `pip_2.ipynb` | nnU-Net 資料集建立 / 訓練 / 推論 notebook |
| `pixi.toml` / `pixi.lock` | Pixi 環境定義與鎖定檔（已含課程全部相依） |
| `scripts/pptx_info.py` | 簡報資訊處理工具（`pixi run info` / `pixi run extract` 使用） |

## 快速開始（詳細步驟見 `步驟第二版.md`）

1. 安裝 Pixi（只需做一次）
2. `git clone https://github.com/xfuren/practice_seg.git && cd practice_seg`
3. `pixi install`（相依已含 python 3.11、ipykernel、totalsegmentator、torch 2.5.1）
4. 註冊 Jupyter kernel：`pixi run python -m ipykernel install --user --name myenv111 --display-name "Python(myenv111)"`
5. nnU-Net 部分需再 clone 官方 nnUNet 並在 `~/nnUNet` 建立環境：`git clone https://github.com/MIC-DKFZ/nnUNet.git`（見 `步驟第二版.md` 的 practice_nnUNet 章節）
6. 登入 Jupyter（網址請參考課程公告），依序執行 notebook