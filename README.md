# practice_seg

Medical image segmentation course material: **TotalSegmentator** (ready-made whole-body segmentation, simplified) + **nnU-Net** (train your own segmentation model with Jupyter Notebook). Environment management uses **Pixi** — no Conda / pip needed.

`practice_nnUNet` 專案已合併進本 repo（該部分的 notebook `2-nnunet.ipynb` 就在這裡），**不需要另外 clone practice_nnUNet**。

## 檔案內容

| 檔案 | 說明 |
|----|----|
| `步驟第二版.md` | 完整分步教程（Pixi 版），**請依照這份執行** |
| `1-totalsegmentator.ipynb` | TotalSegmentator 範例 notebook |
| `2-nnunet.ipynb` | nnU-Net 資料集建立 / 訓練 / 推論 notebook |
| `pixi.toml` / `pixi.lock` | Pixi 環境定義與鎖定檔（單一環境，已含兩部分全部相依） |

## 快速開始（詳細步驟見 `步驟第二版.md`）

1. 安裝 Pixi（只需做一次）
2. `git clone https://github.com/xfuren/practice_seg.git && cd practice_seg`
3. `pixi install`（一次裝好課程兩部分所需的全部相依；全部已宣告在 `pixi.toml`，不需要 `pixi add`，也不需要另外 clone 官方 nnUNet）
4. 註冊 Jupyter kernel（TotalSegmentator 部分與 nnU-Net 部分各一個，指令見 `步驟第二版.md`）
5. 登入 Jupyter（網址請參考課程公告），依序執行 notebook