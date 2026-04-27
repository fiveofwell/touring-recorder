import { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';

export const TourNameChangePage = () => {
	const navigate = useNavigate();
	const { client_tour_id } = useParams<{ client_tour_id: string }>();
	const [newTourName, setNewTourName] = useState('');

	const changeTourName = async () => {
		const normalizedTourName = newTourName.trim();

		if (!normalizedTourName) {
			alert('新しいツーリング名を入力してください');
			return;
		}
		try {
			const response = await fetch(`/api/internal/tours/${client_tour_id}`, {
				method: 'PATCH',
				headers: {
					'Content-Type': 'application/json',
					Authorization: `Bearer ${localStorage.getItem('access_token')}`,
				},
				body: JSON.stringify({
					tour_name: normalizedTourName,
				}),
			});
			if (!response.ok) {
				throw new Error('APIエラー');
			}
			navigate('/tours');
		} catch (error) {
			console.error(error);
			alert('変更に失敗しました。再度お試しください');
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
