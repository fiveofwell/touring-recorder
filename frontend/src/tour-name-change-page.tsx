import { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';

export const TourNameChangePage = () => {
	const navigate = useNavigate();
	const { tour_id } = useParams<{ tour_id: string }>()
	const [newTourName, setNewTourName] = useState('')
	

	const changeTourName = async () => {
		try {
			const response = await fetch(
				`/api/internal/tours/${tour_id}`,
				{
					method: 'PATCH',
					headers: {
						"Content-Type": "application/json",
					},
					body: JSON.stringify({
						tour_name: newTourName
					})
				}
			)
			if (!response.ok) {
				throw new Error('APIエラー')
			}
			navigate('/')
		} catch (error) {
			console.error(error)
			alert('変更に失敗しました。再度お試しください')
		}
	}

	return (
		<>
			<label>
				新しいツーリング名:
				<input
					value={newTourName}
					onChange={(event) => setNewTourName(event.target.value)}
				/>
			</label>
			<button onClick={changeTourName}>
				名前を変更
			</button>

		</>
	)
}
