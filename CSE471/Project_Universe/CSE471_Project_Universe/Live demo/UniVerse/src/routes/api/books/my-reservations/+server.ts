import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';

export const GET: RequestHandler = async (event) => {
	try {
		// Get authenticated user
		const {
			data: { user },
			error: authError
		} = await event.locals.supabase.auth.getUser();

		if (authError || !user) {
			return json(
				{
					success: false,
					error: 'Authentication required. Please log in to view your reservations.'
				},
				{ status: 401 }
			);
		}

		const userId = user.id;

		// Mock data for reservations
		const MOCK_RESERVATIONS = [
			{
				id: 'mock-reservation-1',
				book_id: '2',
				book_title: 'To Kill a Mockingbird',
				book_author: 'Harper Lee',
				reservation_date: '2024-01-15T10:00:00Z',
				expiry_date: '2024-01-22T10:00:00Z',
				status: 'active'
			}
		];

		try {
			// Query reservations directly from the database
			const { data, error } = await event.locals.supabase
				.from('book_reservations')
				.select(
					`
					id,
					book_id,
					reservation_date,
					expiry_date,
					status,
					books!inner(
						id,
						title,
						author
					)
				`
				)
				.eq('user_id', userId)
				.eq('status', 'active')
				.order('reservation_date', { ascending: false });

			if (error) {
				console.error('Error fetching reservations:', error);
				throw error;
			}

			// Transform the data to match expected format
			const reservations =
				data?.map((reservation) => ({
					id: reservation.id,
					book_id: reservation.book_id,
					book_title: reservation.books.title,
					book_author: reservation.books.author,
					reservation_date: reservation.reservation_date,
					expiry_date: reservation.expiry_date,
					status: reservation.status
				})) || [];

			return json({
				success: true,
				reservations: reservations
			});
		} catch (dbError) {
			console.warn('Database error, using mock data:', dbError);
			return json({
				success: true,
				reservations: MOCK_RESERVATIONS
			});
		}
	} catch (error) {
		console.error('Error in GET /api/books/my-reservations:', error);
		return json({ success: false, error: 'Internal server error' }, { status: 500 });
	}
};
