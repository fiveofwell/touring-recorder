# Touring Recorder

## 概要
Touring Recorderは、Raspberry Pi Zero 2とFastAPIを用いた、車やバイクのツーリング記録システムです。  
GPSデータを取得し、APIサーバに送信して保存します。  
個人開発として、バックエンド設計・API設計・
インフラ構成の理解を目的に開発しています。

## 機能
- GPSデータの取得 (緯度・経度・時刻)
- ツーリングごと (Raspberry Pi 起動ごと) の走行データ取得
- ツーリングごとの走行ルート描画
- 通信切断時のローカルデータ保存・再送

## 表示イメージ
![走行ルート表示](https://github.com/user-attachments/assets/7b841eb2-3c3d-4f7f-9842-88e1a8df1ae0)  
![走行ルート表示(林道)](https://github.com/user-attachments/assets/c20bed3e-e073-4016-9f8e-2d3dfe878090)   
どちらも実際にツーリングした記録です。  
ネットワーク接続が不安定になる林道でも、GPSのデータが取得できていれば問題なく記録できます。

## 構成
![構成図](https://github.com/user-attachments/assets/9290c9b7-2c2d-4403-a596-6fad52978b62)

## API
`/api/internal` はCloudflare Accessによるメールアドレス認証  
  
`/api/public` はRaspberry Piがアクセスする必要があるため、APIキー認証

### GPSデータ送信 (APIキー認証)
```
POST /api/public/tours/{tour_id}
```
### ツーリングデータ取得
```
GET /api/internal/tours/{tour_id}
```
### ツーリングデータ削除
```
DELETE /api/internal/tours/{tour_id}
```
### ツーリング一覧取得
```
GET /api/internal/tours
```

## 使用した技術・サービス
### クライアント
- Raspberry Pi Zero 2
- GPS受信機 (DOCTORADIO GR7-10HZ)
- Python
- sqlite3
### バックエンド
- Docker
- FastAPI
- SQLModel
- sqlite3
### フロントエンド
- nginx
- JavaScript
- Leaflet (地図表示ライブラリ)
### デプロイ
- VPS
- Cloudflare Tunnel
- Cloudflare Access

## 工夫点
- Raspberry Pi起動時にツーリングIDを作成し、ツーリングごとにデータを自動的に分類
- インターネット接続が切断されても継続してGPSデータを蓄積し、接続再開時にまとめてデータを送信
- Leafletを使用しインタラクティブな地図を表示
- GPSデータの取得間隔や送信間隔など様々なパラメーターをsettingsファイルで一元管理
- セキュリティのため、Cloudflare Tunnelを経由しないVPSへの直接アクセスはすべて禁止
- 無駄な処理や通信を抑えるため、データの送信が連続して失敗したときは送信間隔を段階的に延長

## 改善したい・追加したい機能
- ツーリングに名前を付ける機能
- 複数ユーザー、複数デバイスの認証
- 走行距離の計算機能
- ツーリングの表示順の変更
など・・・