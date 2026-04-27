import type { Device } from '../types/types';

export const DeviceListItem = ({
	device,
	onDelete,
}: {
	device: Device;
	onDelete: (id: string) => void;
}) => {
	const deleteDevice = async () => {
		if (!confirm('本当にこのデバイスを削除しますか？')) {
			return;
		}

		try {
			const response = await fetch(
				`/api/internal/devices/${device.device_id}`,
				{
					method: 'DELETE',
					headers: {
						Authorization: `Bearer ${localStorage.getItem('access_token')}`,
					},
				},
			);
			if (!response.ok) {
				throw new Error('APIエラー');
			}
			onDelete(device.device_id);
		} catch (error) {
			console.error(error);
			alert('削除に失敗しました');
		}
	};

	return (
		<li>
			<p>デバイス名: {device.device_name}</p>
			<p>キープレフィックス: {device.api_key.key_prefix}</p>
			<p>作成日時: {device.api_key.created_at.toLocaleString()}</p>
			<p>
				最終使用日時:{' '}
				{device.api_key.last_used_at
					? device.api_key.last_used_at.toLocaleString()
					: '未使用'}
			</p>
			<button onClick={deleteDevice}>削除</button>
			<hr />
		</li>
	);
};
