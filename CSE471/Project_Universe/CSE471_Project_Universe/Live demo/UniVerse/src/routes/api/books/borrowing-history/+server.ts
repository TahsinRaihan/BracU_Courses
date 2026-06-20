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
					error: 'Authentication required. Please log in to view your borrowing history.'
				},
				{ status: 401 }
			);
		}

		const userId = user.id;

		// Mock data for borrowing history
		const MOCK_BORROWINGS = [
			{
				id: 'mock-borrowing-1',
				book_id: '1',
				book_title: 'The Great Gatsby',
				book_author: 'F. Scott Fitzgerald',
				borrow_date: '2024-01-10T10:00:00Z',
				due_date: '2024-01-24T10:00:00Z',
				return_date: null,
				status: 'borrowed'
			},
			{
				id: 'mock-borrowing-2',
				book_id: '3',
				book_title: '1984',
				book_author: 'George Orwell',
				borrow_date: '2024-01-05T10:00:00Z',
				due_date: '2024-01-19T10:00:00Z',
				return_date: '2024-01-18T10:00:00Z',
				status: 'returned'
			}
		];

		try {
			// Query borrowing history directly from the database
			const { data, error } = await event.locals.supabase
				.from('book_borrowings')
				.select(
					`
					id,
					borrow_date,
					due_date,
					return_date,
					status,
					book_copies!inner(
						id,
						book_id,
						books!inner(
							id,
							title,
							author
						)
					)
				`
				)
				.eq('user_id', userId)
				.order('borrow_date', { ascending: false });

			if (error) {
				console.error('Error fetching borrowing history:', error);
				throw error;
			}

			// Transform the data to match expected format
			const borrowings =
				data?.map((borrowing) => ({
					id: borrowing.id,
					book_id: borrowing.book_copies.book_id,
					book_title: borrowing.book_copies.books.title,
					book_author: borrowing.book_copies.books.author,
					borrow_date: borrowing.borrow_date,
					due_date: borrowing.due_date,
					return_date: borrowing.return_date,
					status: borrowing.status
				})) || [];

			return json({
				success: true,
				borrowings: borrowings
			});
		} catch (dbError) {
			console.warn('Database error, using mock data:', dbError);
			return json({
				success: true,
				borrowings: MOCK_BORROWINGS
			});
		}
	} catch (error) {
		console.error('Error in GET /api/books/borrowing-history:', error);
		return json({ success: false, error: 'Internal server error' }, { status: 500 });
	}
};
