# AGENTS.md

## 專案性質

`practice_seg` 是醫學影像分割課程教材 repo（TotalSegmentator + nnU-Net）。學生在課程的 Jupyter 伺服器上依 `步驟第二版.md`（繁體中文）逐步操作（伺服器網址與帳號密碼不外流於 repo，請參考課程公告）。環境管理全部使用 **Pixi**；舊版 Conda / pip 流程與相關檔案（`task1-conda.ipynb`、`pip.ipynb`、`conda.ipynb`、`practice_seg.txt`、`nnUNet.txt`、`*-step-2.txt`、`environment*.yml`）已移除，必要時可自 git history 找回。

## 重要檔案

- `步驟第二版.md`：主教程（維護版本）。
- `1-totalsegmentator.ipynb`：TotalSegmentator 範例（學生實際執行）。
- `2-nnunet.ipynb`：nnU-Net 資料集 / 訓練 / 推論（學生實際執行）。nnU-Net 資料目錄固定在 `~/practice_seg/{nnUNet_raw,nnUNet_preprocessed,nnUNet_results}`（執行時自動建立）；**修改資料路徑時必須同步所有 code cell 與已存 output 中的路徑文字**。
- `pixi.toml` / `pixi.lock`：**單一 default 環境**含課程兩部分全部相依——python 3.11 + ipykernel/jupyter_client + gcc/g++/graphviz + pypi: `totalsegmentator`、`torch/torchvision/torchaudio==2.5.1`、`batchgenerators==0.25.5`、`nnunetv2`（官方 git 相依）。**教程流程一律用 `pixi install` + `pixi run`，不要引入 `pixi init` / `pixi add`**；增刪相依請編輯 `pixi.toml` 後跑 `pixi lock` + `pixi install` 並一起 commit。
- 不要用多個 pixi 環境拆課程相依：pixi 0.83 已驗證 (a) 非 default 環境的 pypi 相依會洩漏進 default 環境的 lock；(b) `[tasks]` 的 `default-environment` 不生效（task 一律跑在 default）。
- nnU-Net 部分不需要另外 clone 官方 repo：`nnunetv2` 由 `pixi.toml` 的 git 相依在安裝時自 GitHub 拉取，環境在 `.pixi/envs/default`。


## 環境與指令

- 本機的 pixi 在 `~/.pixi/bin/pixi`（非登入 shell 可能不在 PATH，找不到時用全路徑）。

- 共享快取：課程伺服器上用 `export RATTLER_CACHE_DIR=/home/pipcache/pixi` 可讓全班共用 pixi 下載快取（已驗證 conda 套件、PyPI wheel、repodata 都走這個目錄，第二個專案可直接複用）。
- 常用 tasks：`register-kernel`（myenv111）/ `register-kernel-nnunet`（nnunet333）/ `test-torch` / `test-totalseg` / `test-nnunet`（全部 `pixi run <task>`）。
- `pixi.toml` 必須能被目前版本的 pixi（0.83+）解析：每環境相依用 `[environments.<name>.dependencies]`、任務指定環境用 `default-environment = "..."`。舊語法 `[dependencies.<name>]` + `env = "..."` 會解析失敗，不要 reintroduce。
- `torch` 固定 `==2.5.1`（伺服器 GPU 驅動不支援更新版的 CUDA），不要升級。
- nnUNet 部分的 pixi 環境在 `~/nnUNet`（官方 repo clone 下），不在此 repo。

## Notebook 規範

- notebook 內以 `Path(sys.prefix) / "bin" / ...` 呼叫 TotalSegmentator / nnU-Net 執行檔——這是在 pixi env 下不改動即可運行的原因，**不要改成裸指令、conda 路徑或硬編碼家目錄**。
- `2-nnunet.ipynb` 沒有 `%pip install` cell：`batchgenerators==0.25.5` 由 `pixi.toml` 固定，notebook 該位置是版本檢查 cell。
- notebook 帶有講師示範的已存 output；編輯 code cell 時注意 output 與程式碼的一致性（output 文字中含路徑）。
- 學生 kernel 名稱：`myenv111`（TotalSegmentator 部分）、`nnunet333`（nnU-Net 部分），兩者都由同一個 pixi 環境註冊（`pixi run register-kernel` / `pixi run register-kernel-nnunet`）；nnU-Net 訓練固定 GPU 2（`CUDA_VISIBLE_DEVICES=2` / notebook 內 `GPU_ID = "2"`）。

## Git

- 推送到 `origin`（github.com/xfuren/practice_seg）的 `main` 分支；commit message 用英文祈使句。
- `nnUNet_raw/`、`nnUNet_preprocessed/`、`nnUNet_results/`、`predictions_3d_fullres/`、`.ipynb_checkpoints/`、`.pixi/` 已 gitignore，**不得 commit 任何影像 / 模型資料**。