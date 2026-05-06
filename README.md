# yolo-onboarding

**怎麼負責任地引入一個開源專案 — 以 Ultralytics YOLO 為案例**

---

## 一、本教材要解決的問題

開源套件的安裝普遍被當成「`pip install` 一行就好」。這個觀念在 2026 年已不再安全：

- **供應鏈攻擊**已成常態。`npm`、`PyPI`、HuggingFace 每年都有惡意套件被回報，從 typosquatting（拼字相近的偽造套件）、postinstall 腳本注入、到模型權重被替換。
- **遙測（telemetry）**是商業開源的常態實踐。多數套件首次運行就會發送匿名統計，部分含 CLI 參數、系統資訊、效能指標。
- **License 條款**會「感染」使用者的應用。AGPL-3.0、SSPL 等強 copyleft 授權，若直接 `import`，整個應用的法律狀態都會被改變。

本教材主張：**任何開源套件在首次安裝前，應通過四道關卡的檢查**。本 repo 同時提供：

1. 抽象的方法論 → [`流程.md`](流程.md)
2. 在 Ultralytics YOLO 上的實際操作示範 → [`案例.md`](案例.md)
3. 案例中產出的原始證據（raw evidence）→ [`doc/R1_reputation.md`](doc/R1_reputation.md)、[`doc/R2_dependency.md`](doc/R2_dependency.md)、[`doc/R3_runtime.md`](doc/R3_runtime.md)
4. 進階主題（YOLOE、訓練、ONNX、商用授權）→ [`進階.md`](進階.md)

## 二、讀者前提與閱讀路徑

本教材假設讀者具備以下其中之一即可：

- 能在終端機執行 `pip install`、複製貼上指令、編輯設定檔
- 對 AI 視覺有興趣，願意花一兩個小時動手跑通

不要求讀者熟悉資安、軟體工程實務或機器學習。所有專業詞彙在首次出現時即解釋。

建議閱讀順序：

1. 本 README — 理解問題與框架
2. [`流程.md`](流程.md) — 抽象方法論（不喜歡抽象可先跳過）
3. [`案例.md`](案例.md) — 跟著做一遍
4. [`webcam.py`](webcam.py) — 動手跑
5. [`doc/`](doc/) — 想看細節時的補充
6. [`進階.md`](進階.md) — 進一步探索

## 三、本案例的主要結論

以 Ultralytics YOLO 為例，四關卡檢查產出的判斷如下：

| 階段 | 結果 | 關鍵發現 |
|------|------|---------|
| Gate-1 信譽 | CONDITIONAL PASS ⚠️ | 技術面通過；AGPL-3.0 強 copyleft 條款限制商用部署 |
| Gate-2 依賴 | PASS ✅ | 依賴全屬主流套件、無 postinstall 腳本、CVE 為零 |
| Gate-3 執行時 | PASS ✅ | 遙測可關閉、本地推論不需網路、模型推論行為符合預期 |

期間發現一項 Ultralytics 官方未明示的事實：**`.pt` 模型權重在 GitHub release metadata 中未公布 SHA256**，僅 `.onnx` 格式有。此事實影響了模型供應鏈驗證的實務做法（採 trust-on-first-use 而非比對官方 hash）。詳見 [`案例.md`](案例.md) §5。

## 四、環境需求

- Windows 10/11（本案例以 PowerShell 為主；Linux/macOS 同樣可行，指令略改）
- Python 3.10 以上
- 硬碟空間 ~3 GB（PyTorch + OpenCV 等依賴）
- Webcam（最後 demo 階段需要）

無需 GPU。本案例所有推論皆在 CPU 上執行（YOLO11n 約 60–80 ms / 幀）。

## 五、授權

本教材採 **AGPL-3.0**，與 Ultralytics 一致。理由：[`webcam.py`](webcam.py) 直接 `import ultralytics`，依 AGPL 條款被認定為衍生作品，需採同等強度授權。詳見 [`LICENSE`](LICENSE) 與 [`進階.md`](進階.md) §AGPL 商用評估。

## 六、相關

- 本案例的個人探索版本（私有 repo，含開放式實驗紀錄）
- Ultralytics YOLO 上游：<https://github.com/ultralytics/ultralytics>
- 本流程的更早期版本（KB 內部筆記）：未公開

## 七、回饋

歡迎 issue / PR。若您將本流程套用到其他開源專案並產出對應的 R1~R3 報告，歡迎以 PR 形式提交至 `案例庫/`（規劃中）。
