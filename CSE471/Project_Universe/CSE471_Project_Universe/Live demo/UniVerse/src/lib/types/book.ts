export type Book = {
	id: string;
	title: string;
	author: string;
	isbn: string;
	status: 'available' | 'borrowed' | 'reserved';
	category: string;
	published_year: number;
	location: string;
	image_url?: string;
	created_at: string;
	totalCopies?: number;
	availableCopies?: number;
	borrowedCopies?: number;
	reservedCopies?: number;
	activeReservations?: number;
};

export type BookCopy = {
	id: string;
	book_id: string;
	status: 'available' | 'borrowed' | 'reserved';
	is_available: boolean;
	created_at?: string;
	updated_at?: string;
};
