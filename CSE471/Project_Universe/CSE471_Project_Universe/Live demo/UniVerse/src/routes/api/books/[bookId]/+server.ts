import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';

export const GET: RequestHandler = async (event) => {
	try {
		const { params } = event;
		const { bookId } = params;

		if (!bookId) {
			return json({ success: false, error: 'Book ID is required' }, { status: 400 });
		}

		// Get the book details using the server-side Supabase client
		const { data: book, error } = await event.locals.supabase
			.from('books')
			.select('id, title, author, isbn, category, published_year, location, image_url, created_at')
			.eq('id', bookId)
			.single();

		if (error) {
			console.error('Error fetching book:', error);
			return json({ success: false, error: 'Failed to fetch book' }, { status: 500 });
		}

		if (!book) {
			return json({ success: false, error: 'Book not found' }, { status: 404 });
		}

		return json({
			success: true,
			book
		});
	} catch (error) {
		console.error('Error in GET /api/books/[bookId]:', error);
		return json({ success: false, error: 'Internal server error' }, { status: 500 });
	}
};
