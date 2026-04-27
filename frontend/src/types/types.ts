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

type ApiKey = {
	key_prefix: string;
	created_at: Date;
	last_used_at: Date | null;
};

export type Device = {
	device_id: string;
	device_name: string;
	api_key: ApiKey;
};

export type NewDevice = {
	device_id: string;
	device_name: string;
	api_key: string;
};
