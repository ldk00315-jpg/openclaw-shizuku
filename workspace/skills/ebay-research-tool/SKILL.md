---
name: ebay-research-tool
description: "eBayの商品リサーチを効率化するツール。指定されたサイト（ebay.com, ebay.co.uk, ebay.deなど）、カテゴリ、価格帯、出品国（例: Japan）の条件で売れた商品を検索し、その結果をCSVファイルに出力します。特に、ブラウザのフォーム入力で発生しがちなタイムアウトを回避するため、URLを直接構築して検索とデータ抽出を行います。新しい国や品目のリサーチを開始する時、または特定条件での商品トレンドを調査する際に利用してください。"
---

# Ebay Research Tool

## Overview

このスキルは、とんすけのeBayでの商品リサーチを強力にサポートするために作られたツールだよ。特定の条件（対象サイト、カテゴリ、価格帯、出品国）に基づいてeBayで既に取引された商品（Sold Listings）を効率的に検索し、その結果をCSVファイルとして出力することで、市場分析や仕入れ判断の迅速化を助けるね。

ブラウザのUI操作によるタイムアウトや不安定さを避けるため、検索URLを直接構築してブラウザツールでアクセスし、ページの情報を抽出する方式を採用しているよ。

## Workflow

このスキルを使うときの基本的な流れは以下の通りだよ。

1.  **検索条件の指定**: とんすけが、リサーチしたい「対象サイト」「検索キーワード（品目/カテゴリ）」「価格帯（下限/上限）」「出品国」を私に教えてくれるね。
2.  **検索URLの構築**: 教えてもらった条件と、`references/country_codes.md` にあるeBayドメインや出品国コード（`_salic`パラメータ）の情報を元に、正確なeBayのSold Listings検索URLを私が構築するよ。
3.  **検索実行とデータ抽出**: 構築したURLを使って私がブラウザツール（`default_api.browser(action='snapshot', url=構築したURL)`）でeBayにアクセスし、表示されたページのHTMLコンテンツを取得するね。そして、そのHTMLから売れた商品の商品名、販売価格、送料、出品元、商品のeBayへの直接リンクなどの必要な情報を私が抽出するよ。
4.  **CSV出力**: 抽出した情報を私がCSV形式に整理して、指定されたファイル名でワークスペースに保存するね。これで、とんすけはスプレッドシートで簡単にデータを確認できるようになるよ。

## Parameters for Research

リサーチに必要なパラメータは以下の通りだよ。私に伝えるときに参考にしてね。

*   **対象サイト (country_code)**: 例: `uk` (イギリス), `us` (アメリカ), `de` (ドイツ), `au` (オーストラリア)。 `references/country_codes.md` を参照してね。
*   **検索キーワード (keyword)**: 例: `fountain pen`, `seiko prospex`, `sennheiser headphone`。`references/category_keywords.md` に推奨キーワードの例があるよ。
*   **価格帯 (price_low, price_high)**: 通貨記号を含めない数値で、下限と上限を指定してね。（例: `price_low=370`, `price_high=3730`）
*   **出品国 (item_location)**: 例: `Japan`。 `references/country_codes.md` を参照してね。
*   **出力ファイル名 (output_filename)**: 結果を保存するCSVファイルの名前。例: `uk_fountain_pens.csv`。

## Resources

このスキルは以下の参照情報を使って、より正確なリサーチをサポートするよ。

### references/

*   `country_codes.md`: eBayにおける対象サイトごとのドメインと、出品国ごとの`_salic`パラメータ値の対応表だよ。URL構築時に参照するね。
*   `category_keywords.md`: 主要カテゴリ（万年筆、サングラス、腕時計、オーディオ機器など）ごとの推奨検索キーワードのリストだよ。検索キーワードを考えるときに参考にしてね。

---