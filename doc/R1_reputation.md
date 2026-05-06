# R1 信譽快速判斷 — Ultralytics YOLO

> 開源安全檢查流程第一關（資料抓取於 2026-05-01）
> Repo：https://github.com/ultralytics/ultralytics
>
> **這是原始的調查記錄（raw evidence），整理過的敘事在 [案例.md](../案例.md)。**

## 一句話結論

**條件通過 ⚠️** — Stars 5.6 萬、Ultralytics 公司維護、commit 當日活躍；但 license 是 **AGPL-3.0**，商用 / 教案散布要先想清楚。技術面通過，法律面需確認。

## Gate-1 檢查表

| 檢查項 | 數值 / 觀察 | 評估 |
|--------|-------------|------|
| Stars 數 | **56,641** | ✅ 業界 de facto 標準的 YOLO 實作 |
| 最後更新 | `pushed_at` = 2026-04-30 | ✅ 每日皆有 commit |
| Contributors | 約 **356 人** | ✅ 不是單人維護，但核心仍由 Ultralytics 員工主導 |
| Issues / PR | Open issues 328 | ✅ 數量相對小，回覆頻繁（官方有專人 triage） |
| License | **AGPL-3.0** | ⚠️ **強 copyleft**：透過網路提供服務也算散布，需開源衍生作品；商用通常要買 Ultralytics 商業 license |
| 組織背書 | `ultralytics`（Ultralytics Inc., 英國商業公司） | ✅ 公司實體，且為 YOLOv5/v8/v11 原始作者 |
| README 品質 | 完整文件站（docs.ultralytics.com）+ 多語系教學 | ✅ |
| 補充 | Forks **10,896**（非常活躍的 fork 生態）；最新 release `v8.4.45`（2026-04-29） | ✅ |

## 紅旗 / 注意事項

- **AGPL-3.0 是這個專案最大的非技術風險**：
  - 自用 / 教學示範：沒問題。
  - 嵌入學員的個人作品集 / 商用產品：需評估，AGPL 會「感染」整個應用。
  - 提供成 SaaS：使用者連 SaaS 也算觸發 AGPL 條款，需開源後端。
- Forks 數（10,896）異常高，反映社群常 fork 出去客製。fork 了之後仍受 AGPL 約束，這點要在教案裡特別提醒。
- 模型權重（`.pt` 檔）下載自 Ultralytics CDN（如 `https://github.com/ultralytics/assets/releases/...`），Gate-2/3 要驗 hash。
  - **更正（Gate-3 實證）**：`.pt` 檔在 GitHub release metadata 中**沒有公布 SHA256**，只有 `.onnx` 有。詳見 [R3_runtime.md](R3_runtime.md)。實務上採 trust-on-first-use（首次下載自行記錄 hash）。

## Gate-2 預先記錄的觀察點

- Python 套件，需跑 `pip-audit` / `safety check`，特別注意 `torch`、`opencv-python` 等大依賴的 CVE。
- 安裝時會自動下載預訓練權重 — 確認下載源是 GitHub releases 或 ultralytics.com，不是第三方鏡像。
- 套件首次運行時會嘗試發送匿名遙測（usage analytics）到 Ultralytics 的 hub.ultralytics.com — 可由 `settings.yaml` 關閉，但教案要明寫。

## 判定

**CONDITIONAL PASS — 進入 Gate-2，但教學文件需強調 AGPL 條款與遙測關閉方法**
