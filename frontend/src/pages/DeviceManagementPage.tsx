import { useState } from 'react';
import { useEffect } from 'react';
import type { Device } from '../types/types';
import { DeviceListItem } from '../components/DeviceListItem';
import { useNavigate } from 'react-router-dom';

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
	const [isLoading, setIsLoading] = useState(false);

	const handleDelete = (device_id: string) => {
		setDevices((prev) => prev.filter((d) => d.device_id !== device_id));
	};

	useEffect(() => {
		const fetchDevices = async () => {
			try {
				const response = await fetch('/api/internal/devices', {
					headers: {
						Authorization: `Bearer ${localStorage.getItem('access_token')}`,
					},
				});
				if (!response.ok) {
					throw new Error('APIエラー');
				}
				const data = await response.json();
				setDevices(data.map((d: any) => parseDevice(d)));
			} catch (error) {
				console.error(error);
				setFailed(true);
			} finally {
				setIsLoading(false);
			}
		};
		fetchDevices();
	}, []);

	if (isLoading) return <p>Loading...</p>;
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
