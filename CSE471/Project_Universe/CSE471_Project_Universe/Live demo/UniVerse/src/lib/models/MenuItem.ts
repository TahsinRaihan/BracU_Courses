export type MenuItem = {
	id: string;
	name: string;
	description: string;
	price: number;
	category_id: number;
	image_url?: string | null;
	is_available: boolean;
	created_at?: string;
};
