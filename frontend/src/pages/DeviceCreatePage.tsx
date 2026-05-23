import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import type { NewDevice } from '../types/types';
import { apiFetch } from '../lib/api';

export const DeviceCreatePage = () => {
	const navigate = useNavigate();
	const [newDeviceName, setNewDeviceName] = useState('');
	const [newDevice, setNewDevice] = useState<NewDevice | null>(null);

	const createDevice = async () => {
		const normalizedDeviceName = newDeviceName.trim();

		if (!normalizedDeviceName) {
			alert('新しいデバイス名を入力してください');
			return;
		}
		try {
			const response = await apiFetch(`/api/internal/devices`, {
				method: 'POST',
				body: JSON.stringify({
					device_name: normalizedDeviceName,
				}),
			});
			setNewDevice(await response.json());
		} catch (error) {
			if (error instanceof Error && error.message.includes('409')) {
				alert('デバイス名が既に存在しています。別の名前を入力してください。');
				return;
			}
			console.error('デバイスの作成に失敗しました:', error);
			alert('変更に失敗しました。再度お試しください');
		}
	};

	if (newDevice) {
		return (
			<>
				<h1>デバイスが作成されました</h1>
				<p style={{ color: 'red' }}>
					APIキーはこの画面でしか表示されません。必ず控えてください。
				</p>
				<p>デバイスID: {newDevice.device_id}</p>
				<p>デバイス名: {newDevice.device_name}</p>
				<p style={{ color: 'red', fontSize: '1.5em' }}>
					APIキー: {newDevice.api_key}
				</p>
				<button
					onClick={() => navigator.clipboard.writeText(newDevice.api_key)}
				>
					APIキーをコピー
				</button>
				<button onClick={() => navigate('/devices')}>デバイス管理へ</button>
			</>
		);
	}

	return (
		<>
			<h1>デバイス作成</h1>
			<label>
				新しいデバイス名:
				<input
					value={newDeviceName}
					onChange={(event) => setNewDeviceName(event.target.value)}
				/>
			</label>
			<button onClick={createDevice}>デバイスを作成</button>
		</>
	);
};
