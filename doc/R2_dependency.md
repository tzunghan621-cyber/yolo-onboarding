# R2 依賴 / 程式碼掃描 — Ultralytics YOLO

> 開源安全檢查流程第二關（資料抓取於 2026-05-01）
> 來源：GitHub raw 檔案 + docs.ultralytics.com（**尚未本地 clone / pip install**）
>
> **這是原始的調查記錄（raw evidence），整理過的敘事在 [案例.md](../案例.md)。**

## 一句話結論

**通過 ✅** — 依賴全是主流 Python 套件、無 postinstall 腳本、模型權重官方 GitHub releases 提供 SHA256；唯一需處理的是**內建遙測**，教案需明寫關閉指令。

> ⚠️ 上一句中「`.pt` 提供 SHA256」的部份 R3 後來修正：實際上**只有 `.onnx` 有官方 hash**。詳見 [R3_runtime.md](R3_runtime.md)。

## Gate-2 檢查表

| 檢查項 | 觀察 | 評估 |
|--------|------|------|
| 依賴清單來源 | `pyproject.toml`（PEP 621 標準） | ✅ 沒有私有 registry |
| 核心依賴 | numpy / matplotlib / opencv-python / pillow / pyyaml / requests / scipy / torch / torchvision / psutil / polars / ultralytics-thop | ✅ 全是主流套件，無 typosquatting 嫌疑 |
| 可選依賴 | dev / export / solutions / logging / extra / typing 六組 | ✅ 不安裝就不會引入 |
| postinstall / preinstall | **無** | ✅ `pip install` 不會自動執行任意腳本 |
| 進入點 (scripts) | `yolo` → `ultralytics.cfg:entrypoint`、`ultralytics` → 同上 | ✅ 一般 CLI 進入點 |
| Build hooks | setuptools 動態抓 `__version__` | ✅ 標準作法 |
| CVE 掃描 | **未執行**（尚未 clone） | ⏭ Gate-2 完成後安裝時跑 `pip-audit` |

## 對外連線盤點（程式碼層級）

從 `ultralytics/utils/__init__.py`、`ultralytics/hub/utils.py` 找到的硬寫 URL：

| URL | 用途 | 觸發時機 |
|-----|------|---------|
| `github.com/ultralytics/assets/releases/download/v0.0.0` | 預訓練權重下載 | 第一次用某個模型 |
| `api.ultralytics.com` | Hub API（雲端訓練 / 同步） | 只有登入 Hub 才會用 |
| `hub.ultralytics.com` | Hub 網站 | 只有登入 Hub 才會用 |
| `o4504521589325824.ingest.us.sentry.io` | Sentry 錯誤回報 | 只有 `sentry-sdk` 已安裝 + `sync=True` 才觸發 |
| Google Analytics（非硬寫 URL，透過官方 SDK） | 使用統計 | `sync=True` 預設開啟 |

> 重點：**純本地推論的話只需要第一條 URL**（下載權重）。其他都是遙測或雲端服務，可關閉。

## 遙測收集內容（官方隱私頁）

- **Google Analytics**：使用頻率、CLI 參數、系統資訊、訓練 / 驗證 / 推論的效能指標。
- **Sentry**：crash log（**只有額外裝了 `sentry-sdk` 才會送**，套件預設不裝）。
- 官方聲明：**不收 PII、不收訓練 / 推論影像**，資料是聚合而非個人化。

### 關閉方式（教案必寫）

```bash
# CLI
yolo settings sync=False
```

```python
# Python
from ultralytics import settings
settings.update({"sync": False})
```

設定會持久化到 `settings.yaml`（user config dir），重開有效。

## 模型權重來源 / 完整性

| 項目 | 觀察 | 評估 |
|------|------|------|
| 託管位置 | `github.com/ultralytics/assets/releases` | ✅ 官方 GitHub releases，非第三方鏡像 |
| 發布者 | `@glenn-jocher`（Ultralytics CEO） | ✅ |
| 最新 release | `v8.4.0`（2026-01-13）— 含 YOLO26 模型 | ✅ |
| Checksum | ~~每個 `.pt` 檔附 SHA256~~（**Gate-3 修正：只有 `.onnx` 有**） | ⚠️ 詳見 [R3_runtime.md](R3_runtime.md) |

> Gate-3 動作：下載權重後 `Get-FileHash -Algorithm SHA256` 對比 release 頁面公布的 hash（`.onnx` 才有）。

## 紅旗 / 注意事項

- 套件內建 Sentry DSN 已硬寫進原始碼 — **看似可疑但其實正常**：DSN 公開是 Sentry 的設計（client-side key），目的是讓所有使用者都能回報 crash 給 Ultralytics。要關掉就用 `sync=False`。
- `requests`、`torch`、`opencv-python` 是大依賴，過去都有 CVE 紀錄 → **Gate-2 完成 clone 後一定要跑 `pip-audit`**。
- AGPL-3.0 條款仍然套用（Gate-1 已記錄）。

## 待辦：clone 後要跑的指令

```bash
# CVE 掃描
pip-audit -r requirements.txt   # 或從 pyproject 產生
# 或
pip install safety
safety check

# 確認沒有意外的網路連線
# （Windows）監控 Python 程序的對外連線
# 或第一次跑時直接斷網測試
```

## 判定

**PASS ✅ — 進入 Gate-3（執行時觀察）**

- 教案需強調：
  1. 安裝後**先**執行 `yolo settings sync=False` 再跑任何模型
  2. 不要額外 `pip install sentry-sdk`（避免觸發 crash 回報）
  3. 第一次下載權重後驗 SHA256
  4. 第一次推論建議斷網測試（確認本地可用）
