# R3 安裝 / 執行時驗證 — Ultralytics YOLO

> 開源安全檢查流程第三 + 四關（執行於 2026-05-01）
> 環境：Python 3.12.10（系統）→ venv `.venv\` 隔離
>
> **這是原始的調查記錄（raw evidence），整理過的敘事在 [案例.md](../案例.md)。**

## 一句話結論

**通過 ✅** — 全新 venv 安裝、無 CVE、遙測已關、模型可離線推論；發現一個小落差：**`.pt` 權重沒有官方 SHA256**（只有 `.onnx` 有），需用「首次下載自行記錄」做 trust-on-first-use。

## 環境

| 項目 | 值 |
|------|-----|
| Python | 3.12.10 |
| venv | `.venv\`（專案目錄下） |
| ultralytics | 8.4.45 |
| torch | 2.11.0 |
| pip-audit | 2.10.0 |
| sentry-sdk | **未安裝** ✅（套件預設不裝，crash reporting 不會啟用） |

## 步驟與結果

### 1. 建 venv + 安裝
```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip ultralytics pip-audit
```
- 結果：57 個套件成功安裝，記錄於 `.venv\install.log`。
- 沒有觸發任何 postinstall script（pyproject.toml 已先確認）。

### 2. 立即關閉遙測
```powershell
.\.venv\Scripts\yolo.exe settings sync=False
```
- 設定檔：`%APPDATA%\Ultralytics\settings.json`
- `"sync": false` ✅
- 連帶會關掉的整合：`tensorboard`、`wandb`（預設已 false）；`clearml/comet/dvc/hub/mlflow/neptune/raytune` 預設 true 但只有實際使用時才會發送。

### 3. CVE 掃描
```powershell
.\.venv\Scripts\pip-audit.exe
```
- 結果：**No known vulnerabilities found** ✅
- 涵蓋全部已安裝套件（含 torch、opencv-python、requests 等大依賴）。
- 完整輸出：`.venv\pip-audit.log`

### 4. 模型權重下載 + hash 記錄

```powershell
Invoke-WebRequest "https://github.com/ultralytics/assets/releases/download/v8.3.0/yolo11n.pt" -OutFile .\weights\yolo11n.pt
Get-FileHash -Algorithm SHA256 .\weights\yolo11n.pt
```

| 檔案 | 大小 | SHA256 (本地計算) |
|------|------|------------------|
| `yolo11n.pt` | 5,613,764 bytes (5.4 MB) | `0EBBC80D4A7680D14987A577CD21342B65ECFD94632BD9A8DA63AE6417644EE1` |

> **發現**：GitHub release v8.3.0 的 API metadata 中，**`.pt` 檔的 `digest` 欄位為 `null`**，只有 `.onnx` 有公布 SHA256（如 `yolo11n.onnx: sha256:634279b40c07c6391472c51ad45b81ebc48706a9a1fe72dd3396322acd0c053b`）。
>
> 這修正了 R1 報告中「每個 .pt 都有 SHA256」的誤判 — Gate-3 才實證確認。
>
> **教案做法**：把上表的 hash 釘進教材，學員第一次下載後比對，之後若 hash 變了要警覺（trust-on-first-use 模式）。或建議學員改用 ONNX 版（有官方 hash）。

### 5. 離線推論煙霧測試
```powershell
.\.venv\Scripts\python.exe -c "from ultralytics import YOLO; m = YOLO('./weights/yolo11n.pt'); r = m.predict(source='bus.jpg', save=False, verbose=False); ..."
```

| 指標 | 值 |
|------|-----|
| 推論裝置 | CPU |
| 單張推論時間 | 66.1 ms |
| 偵測物件數 | 5 |
| 類別 | bus, person × 4 |

✅ 圖片來源用本地檔（`bus.jpg`），推論過程**無對外連線需求**。

## 紅旗 / 注意事項

1. **`.pt` 無官方 hash**（已詳述）→ R1 報告需更正。
2. 安裝過程要 ~3 分鐘下載 ~2 GB（torch + opencv 大宗）— 教案要先警告學員。
3. `bus.jpg` 等示範圖會自動下載到 cwd — 教案中要明寫此行為（避免學員誤以為有遙測）。
4. `weights_dir` 預設是相對路徑 `weights`，會在 cwd 下產生資料夾。

## Gate-4 觀察清單（未來上 webcam 時）

- [ ] 開啟 webcam 推論時用 `Get-NetTCPConnection` 監看 Python 程序的對外連線（應只看到 localhost）
- [ ] 第一次跑 webcam 後再次確認 settings.json 的 `sync` 仍是 false（不會被覆寫）
- [ ] 若教案要部署成 web demo（streamlit / flask），AGPL-3.0 條款會觸發 — 需重新評估

## 判定

**PASS ✅ — 安全檢查四關卡完成**

可進入正式專案啟動（撰寫教案、設計 webcam demo）。需在教案中明寫的事項：

1. 安裝步驟要包含 `yolo settings sync=False`
2. 不要 `pip install sentry-sdk`
3. 模型權重首次下載後自行記錄 SHA256 並比對
4. `.pt` vs `.onnx`：商用 / 教學散布若擔心 supply chain，建議優先用 `.onnx`（有官方 hash）
5. AGPL-3.0：學員作品要部署成 web service 前先諮詢
