# akikenTools の更新履歴 <!-- omit in toc -->

## Version 一覧 <!-- omit in toc -->

- [Ver.1.0.0](#ver100)
- [Ver.1.0.1](#ver101)

## Ver.1.0.0

**Release : 2024/05/28**

- ハルセル機械学習における学習・テスト用データのフォーマット統一を目的としライブラリを作成。
- 画像の前処理を行う関数を用意。→ [img_processing](./akikenTools/module.md#img_processing)
- ディレクトリ内の画像に一括で前処理を行う関数を用意。→ [make_folder](./akikenTools/module.md#make_folder)
- ディレクトリ内部の画像から平均画像を作成する関数を用意。 → [make_average_img](./akikenTools/module.md#make_average_img)
- 画像同士の平均二乗誤差を計算するを用意。 → [calc_MSE](./akikenTools/module.md#calc_mse)
- ディレクトリ内に存在する画像全てに対し、特定画像との MSE , RMSE を算出する関数を用意。 → [calc_RMSE_table](./akikenTools/module.md#calc_rmse_table)
- Google Colaboratory 環境で akikenTools の動作を確認。

## Ver.1.0.1

**Release : 2024/06/03**

- issue #1 を修正。
- RGB 画像の特定行について、RGB 値を取得する関数を用意。 → [get_RGB](./akikenTools/module.md#get_rgb)
