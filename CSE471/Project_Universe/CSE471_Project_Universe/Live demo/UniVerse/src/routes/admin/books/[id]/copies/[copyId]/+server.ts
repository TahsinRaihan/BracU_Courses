import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { requireAdmin } from '$lib/server/auth';

export const PUT: RequestHandler = async (event) => {
	try {
		await requireAdmin(event);
		const { supabase } = event.locals;
		const copyId = event.params.copyId;
		const { status, is_available } = await event.request.json();

		// Debug logging
		console.log('Updating copy:', copyId);
		console.log('Requested status:', status);
		console.log('Requested is_available:', is_available);

		// Validate required fields
		if (!status) {
			return json({ success: false, error: 'Status is required' }, { status: 400 });
		}

		// Calculate the correct is_available value
		const calculatedIsAvailable =
			status === 'available' ? (is_available !== undefined ? is_available : true) : false;
		console.log('Calculated is_available:', calculatedIsAvailable);

		// Update the book copy
		const { data: copy, error } = await supabase
			.from('book_copies')
			.update({
				status,
				is_available: calculatedIsAvailable,
				updated_at: new Date().toISOString()
			})
			.eq('id', copyId)
			.select()
			.single();

		if (error) {
			console.error('Error updating book copy:', error);
			return json({ success: false, error: 'Failed to update book copy' }, { status: 500 });
		}

		console.log('Updated copy result:', copy);

		return json({
			success: true,
			message: 'Book copy updated successfully',
			copy
		});
	} catch (error) {
		console.error('Error in PUT /api/admin/books/[id]/copies/[copyId]:', error);
		return json({ success: false, error: 'Internal server error' }, { status: 500 });
	}
};

export const DELETE: RequestHandler = async (event) => {
	try {
		await requireAdmin(event);
		const { supabase } = event.locals;
		const copyId = event.params.copyId;

		// First, check if the copy exists and get its current status
		const { data: existingCopy, error: fetchError } = await supabase
			.from('book_copies')
			.select('id, status, is_available')
			.eq('id', copyId)
			.single();

		if (fetchError) {
			console.error('Error fetching book copy:', fetchError);
			return json({ success: false, error: 'Book copy not found' }, { status: 404 });
		}

		// Check if the copy is borrowed or reserved
		if (existingCopy.status === 'borrowed' || existingCopy.status === 'reserved') {
			return json({ 
				success: false, 
				error: `Cannot delete book copy with status '${existingCopy.status}'. Only available copies can be deleted.` 
			}, { status: 400 });
		}

		// Additional safety check - ensure the copy is actually available
		if (!existingCopy.is_available) {
			return json({ 
				success: false, 
				error: 'Cannot delete book copy that is not available. Please check the copy status.' 
			}, { status: 400 });
		}

		// Delete the book copy
		const { error } = await supabase.from('book_copies').delete().eq('id', copyId);

		if (error) {
			console.error('Error deleting book copy:', error);
			return json({ success: false, error: 'Failed to delete book copy' }, { status: 500 });
		}

		return json({
			success: true,
			message: 'Book copy deleted successfully'
		});
	} catch (error) {
		console.error('Error in DELETE /api/admin/books/[id]/copies/[copyId]:', error);
		return json({ success: false, error: 'Internal server error' }, { status: 500 });
	}
};
