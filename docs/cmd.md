# cmd.md

このファイルは、ローカル実行でよく使うコマンドをまとめる。

Windows PowerShell前提。

---

## build

```powershell
cargo build --release
```

---

## 1ケース実行

```powershell
Get-Content .\in\0000.txt | .\target\release\ahc066.exe > .\out\0000.txt
```

---

## quick

```powershell
python .\simulator.py --trial 1 --output result_quick.csv
```

---

## daily

```powershell
python .\simulator.py --trial 150 --output result.csv
```

---

## 1000ケース評価

```powershell
python .\simulator.py --trial 1000 --output result_1000.csv
```

---

## seed範囲指定

```powershell
python .\simulator.py --start 100 --end 149 --output result_100_149.csv
```

---

## 並列数指定

```powershell
python .\simulator.py --trial 150 --jobs 8 --output result.csv
```

---

## 環境変数付き実行

```powershell
python .\simulator.py --trial 150 --output result_analysis.csv --env AHC_ANALYSIS=1
```

---

## buildしてdaily

```powershell
cargo build --release
python .\simulator.py --trial 150 --output result.csv
```

---

## buildして1000ケース評価

```powershell
cargo build --release
python .\simulator.py --trial 1000 --output result_1000.csv
```

## 分析feature付きbuild

```powershell
cargo build --release --features analysis
```

---

## 分析feature付き評価

```powershell
cargo build --release --features analysis
python .\simulator.py --trial 150 --output result_analysis.csv --env AHC_ANALYSIS=1
```

---

## 提出前通常build

```powershell
cargo build --release
python .\simulator.py --trial 150 --output result.csv
```
