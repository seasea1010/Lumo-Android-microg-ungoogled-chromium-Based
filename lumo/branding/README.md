# Lumo ブランディング

デスクトップ版 Lumo と同一デザインで統一する。

## アイコン

- 正式アイコンは四角版：紺一色（RGB 25,29,73）の正方形キャンバスに単色シアン（0,168,222）の L。
  グロー・グラデ・ツヤなし。原画は `lumo-icon-square.png`（1600×1600）。
- Android 用の15ファイル（mipmap 5密度 × `app_icon.png` / `layered_app_icon.png` /
  `layered_app_icon_background.png`）は `misc/app_icons/` に生成済み。
  ビルド時に `build.sh` が Chromium ツリーの `res_chromium_base/mipmap-*` へ上書きコピーする
  （パッチ適用後なので、`Own/neverdecaf-chromium-icon` パッチよりこちらが優先される）。
- 内訳：`app_icon.png` は四角版そのものの縮小。`layered_app_icon.png`（前景）は L だけを
  抜き出して 90% 縮小・中央配置（アダプティブアイコンのセーフゾーン配慮）。
  `layered_app_icon_background.png`（背景）は紺一色。
- 再生成は `generate-icons.py`（原画のパスはスクリプト冒頭で指定）。

## パッケージ名・アプリ名

- パッケージ名：`com.seasea1019.lumo`
  - `patches/ungoogled-chromium-android/Change-package-name-chromium.patch` で base を設定し、
    `patches/MicroG/Change-package-name-to-microg.patch` で最終値を上書きして確定する
    （`.stable` 等のサフィックスを打ち消す）。
  - パッケージ名が変わるため、microG 設定で新パッケージへの署名偽装を有効にし直す必要がある。
    旧パッケージとは別アプリ扱いになり、上書き更新はできない（入れ直し）。
- アプリ名：`Lumo`（同じく Change-package-name-chromium.patch の `app_name`）。
