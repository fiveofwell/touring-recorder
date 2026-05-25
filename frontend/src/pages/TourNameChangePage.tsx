import { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { apiFetch } from '../lib/api';
import { UnauthorizedError } from '../lib/errors';

export const TourNameChangePage = () => {
	const navigate = useNavigate();
	const { client_tour_id } = useParams<{ client_tour_id: string }>();
	const [newTourName, setNewTourName] = useState('');

	const changeTourName = async () => {
		const normalizedTourName = newTourName.trim();

		if (!normalizedTourName) {
			alert('新しいツーリング名を入力してください。');
			return;
		}
		try {
			await apiFetch(`/api/internal/tours/${client_tour_id}`, {
				method: 'PATCH',
				body: JSON.stringify({
					tour_name: normalizedTourName,
				}),
			});
			navigate('/tours');
		} catch (error) {
			if (error instanceof UnauthorizedError) return;
			console.error('ツーリング名の変更に失敗しました: ', error);
			alert('ツーリング名の変更に失敗しました。再度お試しください。');
		}
	};

	return (
		<>
			<h1>ツーリング名変更</h1>
			<label>
				新しいツーリング名:
				<input
					value={newTourName}
					onChange={(event) => setNewTourName(event.target.value)}
				/>
			</label>
			<button onClick={changeTourName}>名前を変更</button>
		</>
	);
};
