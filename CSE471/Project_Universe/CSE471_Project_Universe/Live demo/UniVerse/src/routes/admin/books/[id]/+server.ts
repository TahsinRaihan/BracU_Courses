import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { requireAdmin } from '$lib/server/auth';

export const GET: RequestHandler = async (event) => {
	try {
		await requireAdmin(event);
		const { supabase } = event.locals;
		const bookId = event.params.id;

		const { data: book, error } = await supabase
			.from('books')
			.select(
				`
        id,
        title,
        author,
        isbn,
        category,
        published_year,
        location,
        status,
        image_url,
        created_at,
        book_copies (
          id,
          status,
          is_available
        )
      `
			)
			.eq('id', bookId)
			.single();

		if (error) {
			console.error('Error fetching book:', error);
			return json({ success: false, error: 'Book not found' }, { status: 404 });
		}

		// Transform the data to include copy counts - consistent with student side
		const totalCopies = book.book_copies?.length || 0;
		const availableCopies =
			book.book_copies?.filter((copy) => copy.status === 'available')?.length || 0;
		const borrowedCopies =
			book.book_copies?.filter((copy) => copy.status === 'borrowed')?.length || 0;
		const reservedCopies =
			book.book_copies?.filter((copy) => copy.status === 'reserved')?.length || 0;

		const transformedBook = {
			...book,
			totalCopies,
			availableCopies,
			borrowedCopies,
			reservedCopies
		};

		return json({ success: true, book: transformedBook });
	} catch (error) {
		console.error('Error in GET /api/admin/books/[id]:', error);
		return json({ success: false, error: 'Internal server error' }, { status: 500 });
	}
};

export const PUT: RequestHandler = async (event) => {
	try {
		await requireAdmin(event);
		const { supabase } = event.locals;
		const bookId = event.params.id;
		const { title, author, isbn, category, published_year, location, status, image_url } =
			await event.request.json();

		// Validate required fields
		if (!title || !author || !isbn) {
			return json(
				{ success: false, error: 'Title, author, and ISBN are required' },
				{ status: 400 }
			);
		}

		// Check if ISBN is already used by another book
		const { data: existingBook } = await supabase
			.from('books')
			.select('id')
			.eq('isbn', isbn)
			.neq('id', bookId)
			.single();

		if (existingBook) {
			return json(
				{ success: false, error: 'A book with this ISBN already exists' },
				{ status: 400 }
			);
		}

		// Update the book
		const { data: book, error } = await supabase
			.from('books')
			.update({
				title,
				author,
				isbn,
				category,
				published_year: published_year || null,
				location: location || null,
				status: status || 'available',
				image_url: image_url || null,
				updated_at: new Date().toISOString()
			})
			.eq('id', bookId)
			.select()
			.single();

		if (error) {
			console.error('Error updating book:', error);
			return json({ success: false, error: 'Failed to update book' }, { status: 500 });
		}

		// If status changed, update all book copies to match
		if (status && status !== 'available') {
			// Update all copies to have the same status and set is_available to false
			const { error: copiesError } = await supabase
				.from('book_copies')
				.update({
					status: status,
					is_available: false,
					updated_at: new Date().toISOString()
				})
				.eq('book_id', bookId);

			if (copiesError) {
				console.error('Error updating book copies status:', copiesError);
				// Don't fail the entire operation, just log the error
			}
		} else if (status === 'available') {
			// If status is 'available', set all copies to available and is_available to true
			const { error: copiesError } = await supabase
				.from('book_copies')
				.update({
					status: 'available',
					is_available: true,
					updated_at: new Date().toISOString()
				})
				.eq('book_id', bookId);

			if (copiesError) {
				console.error('Error updating book copies status:', copiesError);
				// Don't fail the entire operation, just log the error
			}
		}

		return json({
			success: true,
			message: `Book "${title}" updated successfully`,
			book
		});
	} catch (error) {
		console.error('Error in PUT /api/admin/books/[id]:', error);
		return json({ success: false, error: 'Internal server error' }, { status: 500 });
	}
};

export const DELETE: RequestHandler = async (event) => {
	try {
		await requireAdmin(event);
		const { supabase } = event.locals;
		const bookId = event.params.id;

		// Get book details for confirmation
		const { data: book } = await supabase
			.from('books')
			.select('title, isbn')
			.eq('id', bookId)
			.single();

		if (!book) {
			return json({ success: false, error: 'Book not found' }, { status: 404 });
		}

		// Delete book copies first (due to foreign key constraints)
		const { error: copiesError } = await supabase
			.from('book_copies')
			.delete()
			.eq('book_id', bookId);

		if (copiesError) {
			console.error('Error deleting book copies:', copiesError);
			return json({ success: false, error: 'Failed to delete book copies' }, { status: 500 });
		}

		// Delete the book
		const { error: bookError } = await supabase.from('books').delete().eq('id', bookId);

		if (bookError) {
			console.error('Error deleting book:', bookError);
			return json({ success: false, error: 'Failed to delete book' }, { status: 500 });
		}

		return json({
			success: true,
			message: `Book "${book.title}" deleted successfully`
		});
	} catch (error) {
		console.error('Error in DELETE /api/admin/books/[id]:', error);
		return json({ success: false, error: 'Internal server error' }, { status: 500 });
	}
};
