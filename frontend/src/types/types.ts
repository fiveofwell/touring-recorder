export type Point = {
	latitude: number;
	longitude: number;
	timestamp: Date;
};

export type Tour = {
	tour_name: string;
	client_tour_id: string;
	device_name: string;
	created_at: Date;
	updated_at: Date;
};

export type TourLinkProps = {
	tour_name: string;
	client_tour_id: string;
};

export type TourDetailProps = Tour & {
	onDelete: (client_tour_id: string) => void;
};
