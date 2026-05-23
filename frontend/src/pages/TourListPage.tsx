import { useState, useEffect } from 'react';
import { TourDetail } from '../components/TourDetail';
import type { Tour } from '../types/types';
import { apiFetch } from '../lib/api';

const parseTour = (raw: any): Tour => ({
	...raw,
	created_at: new Date(raw.created_at + 'Z'),
	updated_at: new Date(raw.updated_at + 'Z'),
});

export const TourListPage = () => {
	const [tours, setTours] = useState<Tour[]>([]);
	const [loading, setLoading] = useState(true);
	const [failed, setFailed] = useState(false);

	const handleDelete = (client_tour_id: string) => {
		setTours((prev) => prev.filter((t) => t.client_tour_id !== client_tour_id));
	};

	useEffect(() => {
		const fetchTours = async () => {
			try {
				const response = await apiFetch('/api/internal/tours');

				const data = await response.json();
				setTours(data.map((t: any) => parseTour(t)));
			} catch (error) {
				console.error('ツーリングの取得に失敗しました:', error);
				setFailed(true);
			} finally {
				setLoading(false);
			}
		};
		fetchTours();
	}, []);

	if (loading) return <p>Loading...</p>;
	if (failed) return <p>エラーが発生しました</p>;
	return (
		<>
			<h1>ツーリング一覧</h1>
			<ul>
				{tours.map((t) => (
					<TourDetail key={t.client_tour_id} {...t} onDelete={handleDelete} />
				))}
			</ul>
		</>
	);
};
