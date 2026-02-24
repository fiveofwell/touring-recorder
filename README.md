# Touring Recorder

## 概要
Touring Recorderは、Raspberry Pi Zero 2とFastAPIを用いた、車やバイクのツーリング記録システムです。  
GPSデータを取得し、APIサーバに送信して保存します。  
通信が不安定な環境でもデータを欠損させず記録できる、実運用中のシステムです。

## 機能
- GPSデータの取得 (緯度・経度・時刻)
- ツーリングごと (Raspberry Pi 起動ごと) の走行データ取得
- ツーリングごとの走行ルート描画
- 通信切断時のローカルデータ保存・再送
- ツーリングへの命名

## 表示イメージ
![走行ルート表示](https://github.com/user-attachments/assets/7b841eb2-3c3d-4f7f-9842-88e1a8df1ae0)  
![走行ルート表示(林道)](https://github.com/user-attachments/assets/c20bed3e-e073-4016-9f8e-2d3dfe878090)   
どちらも実際のツーリング記録です。  
ネットワーク接続が不安定な林道でも、GPSのデータをローカルに一時保存し、接続回復後に自動で再送することで記録が失われません。

## 構成
![構成図](https://github.com/user-attachments/assets/ad5cc470-907a-45cd-a946-01d87fdc9380)

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
### ツーリングの名前の変更
```
PATCH /api/internal/tours/{tour_id}
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
- pytest
### フロントエンド
- nginx
- JavaScript
- Leaflet (地図表示ライブラリ)
### デプロイ
- VPS
- Cloudflare Tunnel
- Cloudflare Access

## 工夫点
- Raspberry Pi起動時にツーリングIDを作成し、ツーリングごとにデータを自動分類
- インターネット接続が切断されても継続してGPSデータを蓄積し、データ欠損を防止
- Leafletを使用しインタラクティブな地図を表示
- GPSデータの取得間隔や送信間隔などのパラメーターをsettingsファイルで一元管理
- セキュリティのため、Cloudflare Tunnelを経由しないVPSへの直接アクセスはすべて禁止
- データの送信が連続して失敗したときは送信間隔を段階的に延長
- 全サービスをDocker Composeで管理し、コマンド一つで起動可能
- pytestによる自動テスト

## 改善したい・追加したい機能
- 複数ユーザー、複数デバイスの認証
- 走行距離の計算機能
- ツーリングの表示順の変更
など・・・
