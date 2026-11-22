# Lumo Android — 取り込み状態（第2フェーズ前半）

作成日: 2026-11-22
取り込み先リポジトリ: `seasea1010/Lumo-Android-microg-ungoogled-chromium-Based`
土台: bearinmindcat/microg-ungoogled-chromium @ `6f8014b`（Chromium 155.0.8059.39 / ungoogled-chromium 155.0.8059.39-1）

## 現在の状態： 土台ファイルのコピー実施済み（2026-11-22、オーナー了承済み）

オーナーの明示的な了承を得て、土台 @ `6f8014b` の全ファイル（`.git` を除く235件）を
このツリーへコピーした。あわせて下記の取り込み時変更を実施済み：

- 平文 OAuth 資格情報の除去（`android_flags.release.gn` の2項目。下記仕様どおり実施し、
  ツリー全体の走査で残存ゼロを確認済み）
- ワークフロー／アクションへの Secrets env 追加（`build-steps.yml`、`build-stage/action.yml`。
  詳細は `lumo/README.md` の変更点一覧）
- ライセンス配置： `LICENSE.md`（土台 GPL-3.0 をそのまま）、`LICENSES/GPL-3.0.txt`（同内容の切り出し）、
  `LICENSES/BSD-3-Clause-ungoogled.txt`（本家 LICENSE から転記）
- `README.md` は Lumo Android 用（既存の Lumo 側ファイル）を維持

全ファイルのマニフェスト（パス／サイズ／blob SHA、バッチ番号付き）は `../push-manifest.md` に生成済み。
push は未実施（次工程）。

## ツリー構成（コピー実施後）

計画書（`../import-plan.md`）の構成案どおり、土台のディレクトリ構成をそのまま維持する。

```
import-tree/
├── （土台の構成をそのまま） build.sh / .build_config / android_flags*.gn
│   patches/（Bromite/ Cromite/ Extensions/ MicroG/ Other/ Own/ src-fix/
│             Unobtainium/ Vanadium/ ungoogled-chromium-android/、series、series.pristine）
│   domain_sub_2.list / pruning_2.list / microg/ / misc/ / docs/ / build/
│   .github/（workflows / actions / scripts）/ .gitea/
├── lumo/                      ← Lumo 独自物（このツリーに既存）
├── LICENSE.md                 ← 土台の GPL-3.0 をそのまま保持（コピー時に配置）
├── LICENSES/
│   ├── GPL-3.0.txt            ← 土台 LICENSE.md から切り出し（コピー時に配置）
│   ├── BSD-3-Clause-ungoogled.txt  ← 本家 LICENSE から転記（コピー時に配置）
│   └── LUMO-PROPRIETARY.txt   ← 既存
└── README.md                  ← 既存（Lumo Android 用に差し替え）
```

## 平文 OAuth 資格情報の除去仕様（実施済み）

読み取り確認で特定した平文の所在（**値はここに書かない**）：

| ファイル | 項目名 | 扱い |
|---|---|---|
| `android_flags.release.gn` | `google_default_client_id` | 行ごと除去 |
| `android_flags.release.gn` | `google_default_client_secret` | 行ごと除去 |

- `android_flags.gn` / `android_flags.debug.gn` には平文の実資格情報は無い（debug 側は空文字列のみ）。
- 土台のビルドスクリプトは、環境変数 `GOOGLE_DEFAULT_CLIENT_ID` と `GOOGLE_DEFAULT_CLIENT_SECRET`
  の両方が設定されている場合に限り、それらを生成される args.gn へ追記する仕組みを持つ
  （`GOOGLE_API_KEY` も同様）。除去後はこの env 注入が唯一の経路になる。
- ただし土台同梱の GitHub ワークフロー（`.github/workflows/build-steps.yml`、
  `.github/actions/build-stage/`）は現状これらの環境変数をジョブへ渡していない。
  取り込み時に Lumo 側変更として、ワークフロー／アクションの env に
  GitHub Secrets（`GOOGLE_API_KEY` / `GOOGLE_DEFAULT_CLIENT_ID` / `GOOGLE_DEFAULT_CLIENT_SECRET`、
  デスクトップ版 Lumo と同じ名前・同じ Google Cloud プロジェクトの資格情報）を追加する。
  この変更は土台ファイルへの改変になるため、差分は `lumo/README.md` の変更点一覧に記録する。

## 署名 keystore の扱い（要約）

詳細は `../first-build-requirements.md`。要点：

- 初回スモークビルド（土台のまま arm64）は **Secrets の keystore なしで実行可能**。
  ワークフローは keystore が空なら署名工程を「ビルド成果物をそのままコピー」に切り替え、
  APK は Chromium 既定のデバッグ署名になる。
- Lumo 用の正規 keystore は、継続利用する APK を配る段階（Lumo 化フェーズ）までに
  オーナーが発行し、Secrets（`KEYSTORE_B64` / `KEYSTORE_PASS`）へ登録する。
  デバッグ署名の APK は正規キー署名の APK で上書きインストールできない点に注意。
