# akikenTools の更新履歴 <!-- omit in toc -->

## Version 一覧 <!-- omit in toc -->

- [Ver.1.0.0](#ver100)

## Ver.1.0.0

**Release : 2024/05/28**

- ハルセル機械学習における学習・テスト用データのフォーマット統一を目的としライブラリを作成。
- 画像の前処理を行う関数を用意。→ [img_processing](./akikenToolsDev/module.md#img_processing)
- ディレクトリ内の画像に一括で前処理を行う関数を用意。→ [make_folder](./akikenToolsDev/module.md#make_folder)
- ディレクトリ内部の画像から平均画像を作成する関数を用意。 → [make_average_img](./akikenToolsDev/module.md#make_average_img)
- 画像同士の平均二乗誤差を計算するを用意。 → [calc_MSE](./akikenToolsDev/module.md#calc_MSE)
- ディレクトリ内に存在する画像全てに対し、特定画像との MSE , RMSE を算出する関数を用意。 → [calc_RMSE_table](./akikenToolsDev/module.md#calc_RMSE_table)
- Google Colaboratory 環境で akikenTools の動作を確認。
