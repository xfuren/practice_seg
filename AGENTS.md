# AGENTS.md

## 專案性質

`practice_seg` 是醫學影像分割課程教材 repo（TotalSegmentator + nnU-Net）。學生在課程的 Jupyter 伺服器上依 `步驟第二版.md`（繁體中文）逐步操作（伺服器網址與帳號密碼不外流於 repo，請參考課程公告）。環境管理全部使用 **Pixi**；舊版 Conda / pip 流程與相關檔案（`task1-conda.ipynb`、`pip.ipynb`、`conda.ipynb`、`practice_seg.txt`、`nnUNet.txt`、`*-step-2.txt`、`environment*.yml`）已移除，必要時可自 git history 找回。

## 重要檔案

- `步驟第二版.md`：主教程（維護版本）。原始簡報 `步驟第二版.pptx` **不在 repo 中**（已 gitignore，講師本機保留；含舊版截圖與敏感資訊，勿 commit）。`pixi run extract` 會用 pandoc 把本機 pptx 轉到 `步驟第二版_原始.md` 供對照。修改教程時以 md 為準。
- `task1-pip_2.ipynb`：TotalSegmentator 範例（學生實際執行）。
- `pip_2.ipynb`：nnU-Net 資料集 / 訓練 / 推論（學生實際執行）。nnU-Net 資料目錄固定在 `~/practice_seg/{nnUNet_raw,nnUNet_preprocessed,nnUNet_results}`（執行時自動建立）；**修改資料路徑時必須同步所有 code cell 與已存 output 中的路徑文字**。
- `pixi.toml` / `pixi.lock`：default env = python 3.11 + ipykernel + totalsegmentator + `torch==2.5.1`（CUDA）；`ppt` env = pandoc + python-pptx（簡報工具用）。
- `scripts/pptx_info.py`：pptx 資訊腳本（`pixi run info`）。

## 環境與指令

- 本機的 pixi 在 `~/.pixi/bin/pixi`（非登入 shell 可能不在 PATH，找不到時用全路徑）。
- `pixi run extract`：pandoc 將 pptx 轉 markdown（ppt env）。
- `pixi run info`：顯示 pptx 資訊（ppt env）。
- `pixi.toml` 必須能被目前版本的 pixi（0.83+）解析：每環境相依用 `[environments.<name>.dependencies]`、任務指定環境用 `default-environment = "..."`。舊語法 `[dependencies.<name>]` + `env = "..."` 會解析失敗，不要 reintroduce。
- `torch` 固定 `==2.5.1`（伺服器 GPU 驅動不支援更新版的 CUDA），不要升級。
- nnUNet 部分的 pixi 環境在 `~/nnUNet`（官方 repo clone 下），不在此 repo。

## Notebook 規範

- notebook 內以 `Path(sys.prefix) / "bin" / ...` 呼叫 TotalSegmentator / nnU-Net 執行檔——這是在 pixi env 下不改動即可運行的原因，**不要改成裸指令、conda 路徑或硬編碼家目錄**。
- `pip_2.ipynb` 含一個舊版 `%pip install ... batchgenerators` cell（pixi 流程直接略過，md 已有說明），保留原樣。
- notebook 帶有講師示範的已存 output；編輯 code cell 時注意 output 與程式碼的一致性（output 文字中含路徑）。
- 學生 kernel 名稱：`myenv111`（TotalSegmentator 部分）、`nnunet333`（nnU-Net 部分）；nnU-Net 訓練固定 GPU 2（`CUDA_VISIBLE_DEVICES=2` / notebook 內 `GPU_ID = "2"`）。

## Git

- 推送到 `origin`（github.com/xfuren/practice_seg）的 `main` 分支；commit message 用英文祈使句。
- `nnUNet_raw/`、`nnUNet_preprocessed/`、`nnUNet_results/`、`predictions_3d_fullres/`、`.ipynb_checkpoints/`、`.pixi/` 已 gitignore，**不得 commit 任何影像 / 模型資料**。