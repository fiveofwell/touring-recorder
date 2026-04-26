export type Point = {
	latitude: number;
	longitude: number;
	timestamp: Date;
};

export type Tour = {
	tour_name: string;
	tour_id: string;
	device_id: string;
	started_at: Date;
	last_seen_at: Date;
};

export type TourLinkProps = {
	name: string;
	id: string;
};

export type TourDetailProps = Tour & {
	onDelete: (tour_id: string) => void;
};
