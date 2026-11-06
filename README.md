# T_Y_Tools

**責任者:** [tumayouzyo](https://github.com/tumayouzyo)  
**作成者:** Codex

VRChat向けUnityツールの共通VPMリポジトリ。

[配布ページ](https://tumayouzyo.github.io/vpm-repository/)

VCC登録URL: `https://tumayouzyo.github.io/vpm-repository/index.json`

## パッケージの追加

1. パッケージ本体のGitHub Releaseへ、VPM用ZIPと同じ内容の `package.json` を添付する。
2. `repository.json` の `repositories` に `owner/repository` を追加する。
3. Publish VPM listing を手動実行するか、定期更新を待つ。

一覧は約30分ごとに更新する。GitHub Actionsの混雑により遅れる場合がある。通常のソース更新だけでは新版は公開されない。

旧UnitypackageのみのReleaseは一覧に含めない。ZIPとマニフェストの一致を確認し、SHA256を一覧に記載する。生成が失敗した場合は前回の公開内容を維持する。

このリポジトリのコードはMITライセンス。配布対象の各パッケージには、それぞれのライセンスが適用される。
