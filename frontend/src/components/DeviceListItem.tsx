import type { Device } from '../types/types';
import { apiFetch } from '../lib/api';
import { UnauthorizedError } from '../lib/errors';
import { useState } from 'react';

export const DeviceListItem = ({
	device,
	onDelete,
}: {
	device: Device;
	onDelete: (id: string) => void;
}) => {
	const [isDeleting, setIsDeleting] = useState(false);

	const deleteDevice = async () => {
		if (isDeleting) {
			return;
		}

		if (!confirm('本当にこのデバイスを削除しますか？')) {
			return;
		}

		setIsDeleting(true);
		try {
			await apiFetch(`/api/internal/devices/${device.device_id}`, {
				method: 'DELETE',
			});
			onDelete(device.device_id);
		} catch (error) {
			if (error instanceof UnauthorizedError) return;
			console.error('デバイスの削除に失敗しました: ', error);
			alert('デバイスの削除に失敗しました。再度お試しください。');
		} finally {
			setIsDeleting(false);
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
			<button onClick={deleteDevice} disabled={isDeleting}>
				{isDeleting ? '削除中...' : '削除'}
			</button>
			<hr />
		</li>
	);
};
