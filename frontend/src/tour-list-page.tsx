import { useState, useEffect } from 'react';
import { TourDetail } from './components/tour';
import type { Tour } from './components/types';

const parseTour = (raw: any): Tour => ({
	...raw,
	started_at: new Date(raw.started_at + "Z"),
	last_seen_at: new Date(raw.last_seen_at + "Z"),
})

export const TourListPage = () => {
	const [tours, setTours] = useState<Tour[]>([])
	const [loading, setLoading] = useState(true)
	const [failed, setFailed] = useState(false)

	const handleDelete = (tour_id: string) => {
		setTours(prev => prev.filter(t => t.tour_id !== tour_id))
	}

	useEffect(() => {
		fetch('/api/internal/tours')
		.then(response => {
			if (!response.ok) {
				throw new Error('APIエラー')
			}
			return response.json()
		})
		.then(data => {
			setTours(data.map((t: any) => parseTour(t)))
		})
		.catch(error => {
			console.error(error)
			setFailed(true)
		})
		.finally(() => setLoading(false))
	}, [])

	if (loading) return ( <p>Loading...</p> )
	if (failed) return ( <p>エラーが発生しました</p> )
	return (
		<ul>
			{tours.map(t => (
				<TourDetail
					key={t.tour_id}
					{...t}
					onDelete={handleDelete}
				/>
			))}
		</ul>
	)

}
