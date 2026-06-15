import { useEffect } from 'react';
import {
	MapContainer,
	TileLayer,
	Polyline,
	Popup,
	Marker,
	useMap,
} from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import type { Point } from '../types/types';

const FitBounds = ({ points }: { points: [number, number][] }) => {
	const map = useMap();

	useEffect(() => {
		if (points.length > 0) {
			map.fitBounds(points);
		}
	}, [points, map]);

	return null;
};

const SetMarkers = ({ points }: { points: Point[] }) => {
	if (points.length === 0) return null;

	const startPoint = points[points.length - 1];
	const endPoint = points[0];

	const startMarkerPosition: [number, number] = [
		startPoint.latitude,
		startPoint.longitude,
	];
	const endMarkerPosition: [number, number] = [
		endPoint.latitude,
		endPoint.longitude,
	];

	return (
		<>
			<Marker position={startMarkerPosition}>
				<Popup>
					ツーリング開始:{startPoint.recorded_at.toLocaleString('ja-JP')}
				</Popup>
			</Marker>
			<Marker position={endMarkerPosition}>
				<Popup>
					ツーリング終了:{endPoint.recorded_at.toLocaleString('ja-JP')}
				</Popup>
			</Marker>
		</>
	);
};

export const MapView = ({ points }: { points: Point[] }) => {
	const positions: [number, number][] = points.map((p) => [
		p.latitude,
		p.longitude,
	]);

	return (
		<MapContainer style={{ height: 1000 }}>
			<TileLayer
				attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
				url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
			/>
			<Polyline positions={positions} />
			<SetMarkers points={points} />
			<FitBounds points={positions} />
		</MapContainer>
	);
};

const calculateDistance = (point1: Point, point2: Point) => {
	const a = 6378137;
	const e = 0.00669438;

	const lat1Rad = (point1.latitude * Math.PI) / 180;
	const lon1Rad = (point1.longitude * Math.PI) / 180;
	const lat2Rad = (point2.latitude * Math.PI) / 180;
	const lon2Rad = (point2.longitude * Math.PI) / 180;

	const deltaPhi = lat1Rad - lat2Rad;
	const deltaLambda = lon1Rad - lon2Rad;
	const phi = (lat1Rad + lat2Rad) / 2;

	const M = (a * (1 - e)) / Math.pow(1 - e * Math.pow(Math.sin(phi), 2), 3 / 2);

	const N = a / Math.sqrt(1 - e * Math.pow(Math.sin(phi), 2));

	const d = Math.sqrt(
		Math.pow(M * deltaPhi, 2) + Math.pow(N * Math.cos(phi) * deltaLambda, 2),
	);

	return d;
};

const calculateTotalDistance = (points: Point[]): number => {
	let distance = 0;

	for (let i = 1; i < points.length; i++) {
		distance += calculateDistance(points[i - 1], points[i]);
	}

	return distance;
};

export const TourDistance = ({ points }: { points: Point[] }) => {
	if (points.length === 0) return null;

	const distance = calculateTotalDistance(points);

	return <p>走行距離: 約{(distance / 1000).toFixed(2)}km</p>;
};
