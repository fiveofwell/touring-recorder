import { useState } from 'react';
import { useEffect } from 'react';
import type { Device } from '../types/types';
import { DeviceListItem } from '../components/DeviceListItem';
import { useNavigate } from 'react-router-dom';
import { apiFetch } from '../lib/api';
import { UnauthorizedError } from '../lib/errors';

const parseDevice = (raw: any): Device => ({
	...raw,
	api_key: {
		...raw.api_key,
		created_at: new Date(raw.api_key.created_at + 'Z'),
		last_used_at: raw.api_key.last_used_at
			? new Date(raw.api_key.last_used_at + 'Z')
			: null,
	},
});

export const DeviceManagementPage = () => {
	const navigate = useNavigate();
	const [devices, setDevices] = useState<Device[]>([]);
	const [failed, setFailed] = useState(false);
	const [loading, setLoading] = useState(true);

	const handleDelete = (device_id: string) => {
		setDevices((prev) => prev.filter((d) => d.device_id !== device_id));
	};

	useEffect(() => {
		const fetchDevices = async () => {
			try {
				const response = await apiFetch('/api/internal/devices');
				const data = await response.json();
				setDevices(data.map((d: any) => parseDevice(d)));
			} catch (error) {
				if (error instanceof UnauthorizedError) return;
				console.error('デバイスの取得に失敗しました: ', error);
				setFailed(true);
			} finally {
				setLoading(false);
			}
		};
		fetchDevices();
	}, []);

	if (loading) return <p>Loading...</p>;
	if (failed) return <p>デバイスの取得に失敗しました</p>;

	return (
		<>
			<h1>デバイス管理</h1>
			<button onClick={() => navigate('/devices/new')}>新規デバイス追加</button>
			<ul>
				{devices.map((device) => (
					<DeviceListItem
						key={device.device_id}
						device={device}
						onDelete={handleDelete}
					/>
				))}
			</ul>
		</>
	);
};
