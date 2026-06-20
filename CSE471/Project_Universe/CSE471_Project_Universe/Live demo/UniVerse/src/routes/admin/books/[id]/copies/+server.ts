import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { requireAdmin } from '$lib/server/auth';

export const GET: RequestHandler = async (event) => {
	try {
		await requireAdmin(event);
		const { supabase } = event.locals;
		const bookId = event.params.id;

		// Fetch book copies for the specific book
		const { data: copies, error } = await supabase
			.from('book_copies')
			.select('*')
			.eq('book_id', bookId)
			.order('created_at', { ascending: true });

		if (error) {
			console.error('Error fetching book copies:', error);
			return json({ success: false, error: 'Failed to fetch book copies' }, { status: 500 });
		}

		return json({ success: true, copies: copies || [] });
	} catch (error) {
		console.error('Error in GET /api/admin/books/[id]/copies:', error);
		return json({ success: false, error: 'Internal server error' }, { status: 500 });
	}
};

export const POST: RequestHandler = async (event) => {
	try {
		await requireAdmin(event);
		const { supabase } = event.locals;
		const bookId = event.params.id;
		const { status, is_available } = await event.request.json();

		// Validate required fields
		if (!status) {
			return json({ success: false, error: 'Status is required' }, { status: 400 });
		}

		// Insert the new book copy
		const { data: copy, error } = await supabase
			.from('book_copies')
			.insert({
				book_id: bookId,
				status: status || 'available',
				is_available: is_available !== undefined ? is_available : true
			})
			.select()
			.single();

		if (error) {
			console.error('Error inserting book copy:', error);
			return json({ success: false, error: 'Failed to create book copy' }, { status: 500 });
		}

		return json({
			success: true,
			message: 'Book copy added successfully',
			copy
		});
	} catch (error) {
		console.error('Error in POST /api/admin/books/[id]/copies:', error);
		return json({ success: false, error: 'Internal server error' }, { status: 500 });
	}
};
