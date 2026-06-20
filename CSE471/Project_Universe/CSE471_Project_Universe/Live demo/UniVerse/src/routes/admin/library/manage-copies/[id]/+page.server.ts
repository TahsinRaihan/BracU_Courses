import type { PageServerLoad } from './$types';
import { requireAdmin } from '$lib/server/auth';

export const load: PageServerLoad = async (event) => {
	const session = await requireAdmin(event);
	const { supabase } = event.locals;
	const bookId = event.params.id;

	try {
		// Load book details
		const { data: book, error: bookError } = await supabase
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

		if (bookError) {
			console.error('Error fetching book:', bookError);
			return {
				session,
				isAdmin: true,
				book: null,
				copies: [],
				error: 'Book not found'
			};
		}

		// Load book copies
		const { data: copies, error: copiesError } = await supabase
			.from('book_copies')
			.select('*')
			.eq('book_id', bookId)
			.order('created_at', { ascending: true });

		if (copiesError) {
			console.error('Error fetching copies:', copiesError);
		}

		// Transform the book data to include copy counts
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

		return {
			session,
			isAdmin: true,
			book: transformedBook,
			copies: copies || [],
			error: null
		};
	} catch (error) {
		console.error('Error in manage-copies page load:', error);
		return {
			session,
			isAdmin: true,
			book: null,
			copies: [],
			error: 'Failed to load book data'
		};
	}
};
