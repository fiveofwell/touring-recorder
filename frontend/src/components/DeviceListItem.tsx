import type { Device } from '../types/types';
import { apiFetch } from '../lib/api';

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
			await apiFetch(`/api/internal/devices/${device.device_id}`, {
				method: 'DELETE',
			});
			onDelete(device.device_id);
		} catch (error) {
			console.error('デバイスの削除に失敗しました: ', error);
			alert('削除に失敗しました。再度お試しください。');
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
