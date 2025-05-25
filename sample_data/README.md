# サンプルデータについて

このディレクトリには、Universal Timeline Parserをテストするためのサンプルデータファイルが含まれています。
これらのファイルには個人情報は含まれておらず、開発・テスト目的のみに使用されるダミーデータです。

## 含まれるファイル

- `sample_android.json` - Android端末のGoogle Timelineデータのサンプル
- `sample_iphone.json` - iPhone端末のGoogle Timelineデータのサンプル

## 使用方法

これらのサンプルファイルを使用してパーサーをテストするには：

```bash
# サンプルファイルをdataディレクトリにコピー
cp sample_data/sample_android.json data/
cp sample_data/sample_iphone.json data/

# パーサーを実行
python main.py
```

## 注意事項

- これらはテスト用の簡易的なサンプルデータです
- 実際のデータ構造はより複雑な場合があります
- 新しいデータ形式のパーサーを開発する際は、このサンプルデータを参考にしてください
