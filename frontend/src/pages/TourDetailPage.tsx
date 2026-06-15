import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { TourDistance, MapView } from '../components/MapView';
import type { Point } from '../types/types';
import { apiFetch } from '../lib/api';
import { UnauthorizedError } from '../lib/errors';

const parsePoint = (raw: any): Point => ({
	...raw,
	recorded_at: new Date(raw.recorded_at + 'Z'),
});

export const TourDetailPage = () => {
	const { client_tour_id } = useParams<{ client_tour_id: string }>();

	const [points, setPoints] = useState<Point[]>([]);
	const [loading, setLoading] = useState(true);
	const [failed, setFailed] = useState(false);

	useEffect(() => {
		const fetchData = async () => {
			try {
				const response = await apiFetch(
					`/api/internal/tours/${client_tour_id}/points`,
				);

				const data = await response.json();
				setPoints(data.points.map((p: any) => parsePoint(p)));
				setLoading(false);
			} catch (error) {
				if (error instanceof UnauthorizedError) return;
				console.error('ツーリングデータの取得に失敗しました: ', error);
				setFailed(true);
			} finally {
				setLoading(false);
			}
		};

		fetchData();
	}, []);

	if (loading) return <p>Loading...</p>;
	if (failed) return <p>エラーが発生しました</p>;

	return (
		<>
			<TourDistance points={points} />
			<MapView points={points} />
		</>
	);
};
