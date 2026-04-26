import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { TourDistance, TourMap } from '../components/MapView';
import type { Point } from '../types/types';

const parsePoint = (raw: any): Point => ({
	...raw,
	timestamp: new Date(raw.timestamp + 'Z'),
});

export const TourDetailPage = () => {
	const { tour_id } = useParams<{ tour_id: string }>();

	const [points, setPoints] = useState<Point[]>([]);
	const [loading, setLoading] = useState(true);
	const [failed, setFailed] = useState(false);

	useEffect(() => {
		fetch(`/api/internal/tours/${tour_id}`)
			.then((response) => {
				if (!response.ok) {
					throw new Error('APIエラー');
				}
				return response.json();
			})
			.then((data) => {
				setPoints(data.points.map((p: any) => parsePoint(p)));
			})
			.catch((error) => {
				console.error(error);
				setFailed(true);
			})
			.finally(() => setLoading(false));
	}, []);

	if (loading) return <p>Loading...</p>;
	if (failed) return <p>エラーが発生しました</p>;

	return (
		<>
			<TourDistance points={points} />
			<TourMap points={points} />
		</>
	);
};
