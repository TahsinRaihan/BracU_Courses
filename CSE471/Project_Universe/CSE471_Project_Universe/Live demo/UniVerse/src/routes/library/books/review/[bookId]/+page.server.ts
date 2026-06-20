import { redirect } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ params, locals }) => {
	try {
		// Check if user is authenticated
		const {
			data: { user },
			error: authError
		} = await locals.supabase.auth.getUser();

		// Require authentication
		if (authError || !user) {
			throw redirect(303, '/auth/login');
		}

		const { bookId } = params;

		if (!bookId) {
			throw redirect(303, '/library/books');
		}

		// Fetch book details
		const { data: book, error: bookError } = await locals.supabase
			.from('books')
			.select('id, title, author, isbn, category, published_year, location, image_url, created_at')
			.eq('id', bookId)
			.single();

		if (bookError || !book) {
			throw redirect(303, '/library/books');
		}

		// Fetch reviews for the book
		const { data: reviews, error: reviewsError } = await locals.supabase.rpc('get_book_reviews', {
			p_book_id: bookId
		});

		if (reviewsError) {
			console.error('Error fetching book reviews:', reviewsError);
		}

		// Fetch rating summary for the book
		const { data: ratingSummary, error: summaryError } = await locals.supabase.rpc(
			'get_book_rating_summary',
			{ p_book_id: bookId }
		);

		if (summaryError) {
			console.error('Error fetching rating summary:', summaryError);
		}

		return {
			book,
			reviews: reviews || [],
			ratingSummary: ratingSummary?.[0] || null,
			user: {
				id: user.id,
				email: user.email
			}
		};
	} catch (error) {
		console.error('Error in review page load:', error);
		throw redirect(303, '/library/books');
	}
};
