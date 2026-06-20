import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';

export const POST: RequestHandler = async (event) => {
	try {
		const { request } = event;
		const { bookId } = await request.json();

		// Validate bookId format
		if (!bookId) {
			return json({ success: false, error: 'Book ID is required' }, { status: 400 });
		}

		// Get authenticated user
		const {
			data: { user },
			error: authError
		} = await event.locals.supabase.auth.getUser();

		if (authError || !user) {
			return json(
				{
					success: false,
					error: 'Authentication required. Please log in to cancel reservations.'
				},
				{ status: 401 }
			);
		}

		const userId = user.id;

		// Validate UUID format
		const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
		if (!uuidRegex.test(bookId)) {
			return json(
				{
					success: false,
					error: 'Invalid book ID format. Please select a valid book to cancel reservation.'
				},
				{ status: 400 }
			);
		}

		// Check if user has an active reservation for this book
		const { data: existingReservation, error: checkError } = await event.locals.supabase
			.from('book_reservations')
			.select('id, status')
			.eq('user_id', userId)
			.eq('book_id', bookId)
			.eq('status', 'active')
			.single();

		if (checkError) {
			if (checkError.code === 'PGRST116') {
				// No rows returned
				return json(
					{
						success: false,
						error: 'No active reservation found for this book'
					},
					{ status: 400 }
				);
			}
			console.error('Error checking reservation:', checkError);
			return json({ success: false, error: 'Failed to check reservation' }, { status: 500 });
		}

		// Cancel the reservation
		const { error: updateError } = await event.locals.supabase
			.from('book_reservations')
			.update({
				status: 'cancelled',
				updated_at: new Date().toISOString()
			})
			.eq('id', existingReservation.id);

		if (updateError) {
			console.error('Error cancelling reservation:', updateError);
			return json({ success: false, error: 'Failed to cancel reservation' }, { status: 500 });
		}

		return json({
			success: true,
			message: 'Reservation cancelled successfully'
		});
	} catch (error) {
		console.error('Error in POST /api/books/cancel-reservation:', error);
		return json({ success: false, error: 'Internal server error' }, { status: 500 });
	}
};
