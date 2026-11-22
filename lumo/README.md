# lumo/ — Lumo 独自物の置き場

土台（microg-ungoogled-chromium、GPL-3.0）への Lumo 側の追加・変更は、
上流との差分追随を容易にするため、このディレクトリに分離して管理する。

## 中身

- `patches/` — Lumo 独自パッチ（History 同期の有効化、ブランド差し替え等。第2フェーズ後半以降で追加）
- `branding/` — Lumo アイコン素材（ビルド時に `misc/app_icons/` へ上書きする元）
- `keystore.gn.example` — ローカルビルド用の署名設定の雛形（実 keystore は置かない）

## 土台ファイルへの Lumo 側変更（差分記録）

取り込みにあたって土台ファイルへ加える変更はここに記録する：

1. `android_flags.release.gn` — 平文で記載されていた上流の OAuth クライアント情報
   （`google_default_client_id` / `google_default_client_secret` の2項目）を除去。
   以後は GitHub Secrets から環境変数で注入する（下記参照）。
2. `.github/workflows/build-steps.yml` および `.github/actions/build-stage/action.yml` —
   ビルド工程へ Google API 資格情報の環境変数を渡すよう env を追加（**実施済み**、2026-11-22 取り込み時）。
   具体的には、build-steps.yml の prep ジョブ（args.gn を生成する工程）の env と、
   part-01〜08 の build-stage 呼び出し（keystore と同じ with 受け渡し方式）に3変数を追加し、
   build-stage アクション側に同名の inputs を新設して Build ステップの env へ渡した。
   渡す Secrets はデスクトップ版 Lumo と同じ Google Cloud プロジェクトのもの：
   `GOOGLE_API_KEY` / `GOOGLE_DEFAULT_CLIENT_ID` / `GOOGLE_DEFAULT_CLIENT_SECRET`。
   土台のビルドスクリプトは ID と SECRET の両方が env にある場合に args.gn へ追記する仕様。
3. `README.md` — Lumo Android 用に差し替え（クレジットは土台から引き継ぎ）。

## 署名 keystore について

- GitHub ホストのビルドでは Secrets `KEYSTORE_B64`（base64 化した .jks）と
  `KEYSTORE_PASS` から投入する。未登録の場合はデバッグ署名のまま成果物がコピーされ、
  初回スモークビルドはその状態で実行できる。
- 署名工程の既定エイリアスは `key0`。正規 keystore を作る際はエイリアスを `key0` にするか、
  環境変数 `UGC_KEYSTORE_ALIAS` で合わせること。
- 一度配った APK と同じキーでないと上書きインストールできない。キーのバックアップは
  オーナーがリポジトリ外で保管する。
