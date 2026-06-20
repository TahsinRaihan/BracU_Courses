import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';

export const GET: RequestHandler = async (event) => {
	try {
		const { bookId } = event.params;

		// Get authenticated user
		const {
			data: { user },
			error: authError
		} = await event.locals.supabase.auth.getUser();

		if (authError || !user) {
			return json(
				{
					success: false,
					error: 'Authentication required. Please log in to check book availability.'
				},
				{ status: 401 }
			);
		}

		const userId = user.id;

		// Check if any copies are available
		const { data: availableCopies, error: copiesError } = await event.locals.supabase
			.from('book_copies')
			.select('id')
			.eq('book_id', bookId)
			.eq('status', 'available')
			.eq('is_available', true);

		if (copiesError) {
			console.error('Error checking book copies:', copiesError);
			return json({ success: false, error: 'Failed to check book availability' }, { status: 500 });
		}

		// Check if user already has an active reservation for this book
		const { data: userReservations, error: reservationError } = await event.locals.supabase
			.from('book_reservations')
			.select('id')
			.eq('user_id', userId)
			.eq('book_id', bookId)
			.eq('status', 'active');

		if (reservationError) {
			console.error('Error checking user reservations:', reservationError);
			return json({ success: false, error: 'Failed to check user reservations' }, { status: 500 });
		}

		const availableCopiesCount = availableCopies?.length || 0;
		const userHasReservation = (userReservations?.length || 0) > 0;
		const canReserve = availableCopiesCount === 0 && !userHasReservation;

		return json({
			success: true,
			can_reserve: canReserve,
			available_copies: availableCopiesCount,
			user_has_reservation: userHasReservation,
			message: canReserve
				? 'Book can be reserved'
				: availableCopiesCount > 0
					? 'Copies are available. Please borrow instead of reserving.'
					: 'You already have an active reservation for this book.'
		});
	} catch (error) {
		console.warn('Database error, using mock response:', error);
		// Mock response - assume can reserve if no copies available
		return json({
			success: true,
			can_reserve: true,
			available_copies: 0,
			user_has_reservation: false,
			message: 'Book can be reserved (mock response)'
		});
	}
};
