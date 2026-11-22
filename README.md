# Lumo Android

オーナーが個人で使うための、microG 対応 Chromium 系 Android ブラウザ。
デスクトップ版 Lumo の Android 版プロジェクト。

## 土台とクレジット

本プロジェクトは [microg-ungoogled-chromium](https://github.com/bearinmindcat/microg-ungoogled-chromium)
（bearinmindcat 氏）を土台に取り込み、Google サービスを通常利用できる形に戻す変更と
Lumo 化（名前・アイコン等）を加えたものです。土台および借用元のクレジットは以下のとおりです：

- Chromium — The Chromium Project（BSD 3-Clause）
- ungoogled-chromium — ungoogled-software（BSD 3-Clause）
- microg-ungoogled-chromium — bearinmindcat（GPL-3.0）
- Bromite / Cromite（GPL-3.0）
- Vanadium — GrapheneOS
- Unobtainium、Kiwi 系の拡張機能パッチほか、土台リポジトリの Credits に記載の各プロジェクト

土台側のライセンス（GPL-3.0）は `LICENSE.md` にそのまま保持しています。
ライセンスの切り分けは `LICENSES/` を参照してください。
Lumo 独自の追加物は `lumo/` ディレクトリに分離しています。

## 方針

- Google 排除系のパッチは外し、サインインと同期（ブックマーク・拡張機能・履歴）を使う。
- microG パッチは残す（端末側に microG GmsCore 系が必要）。
- パスワード同期は対象外（microG 側の Trusted Vault 実装が別プロジェクト級のため）。
- オーナー専用。第三者への配布は想定していない。

## ビルド

GitHub Actions の `build-hosted` ワークフロー（ステージ分割方式）でビルドする。
初回ビルドの要件は `first-build-requirements.md`（リポジトリ外の作業ドキュメント）を参照。
Google API 資格情報は平文で置かず、GitHub Secrets から環境変数で注入する。
