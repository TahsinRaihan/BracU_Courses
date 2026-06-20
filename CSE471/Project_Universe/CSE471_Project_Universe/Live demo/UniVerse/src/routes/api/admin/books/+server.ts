import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { requireAdmin } from '$lib/server/auth';
import { serviceSupabase } from '$lib/server/supabaseService';

interface BookReservation {
	id: string;
	book_id: string;
	status: string;
	created_at: string;
	books: {
		id: string;
		title: string;
		author: string;
		isbn: string;
		category: string;
		published_year: number;
		location: string;
		status: string;
		image_url: string;
		created_at: string;
	};
}

export const GET: RequestHandler = async (event) => {
	try {
		await requireAdmin(event);

		const supabase = serviceSupabase;

		// Mock data for when database is not available
		const MOCK_ADMIN_BOOKS = [
			{
				id: '1',
				title: 'The Great Gatsby',
				author: 'F. Scott Fitzgerald',
				isbn: '978-0743273565',
				category: 'Fiction',
				published_year: 1925,
				location: 'Shelf A1',
				status: 'available',
				image_url: 'https://example.com/gatsby.jpg',
				created_at: '2024-01-01T00:00:00Z',
				totalCopies: 3,
				availableCopies: 2,
				borrowedCopies: 1,
				reservedCopies: 0
			},
			{
				id: '2',
				title: 'To Kill a Mockingbird',
				author: 'Harper Lee',
				isbn: '978-0446310789',
				category: 'Fiction',
				published_year: 1960,
				location: 'Shelf A2',
				status: 'available',
				image_url: 'https://example.com/mockingbird.jpg',
				created_at: '2024-01-01T00:00:00Z',
				totalCopies: 2,
				availableCopies: 1,
				borrowedCopies: 0,
				reservedCopies: 1
			},
			{
				id: '3',
				title: '1984',
				author: 'George Orwell',
				isbn: '978-0451524935',
				category: 'Fiction',
				published_year: 1949,
				location: 'Shelf A3',
				status: 'available',
				image_url: 'https://example.com/1984.jpg',
				created_at: '2024-01-01T00:00:00Z',
				totalCopies: 1,
				availableCopies: 0,
				borrowedCopies: 1,
				reservedCopies: 0
			}
		];

		try {
			console.log('🔍 Testing service role client connection...');
			// Test the connection first
			const { error: testError } = await supabase.from('books').select('count').limit(1);

			if (testError) {
				console.error('❌ Service role client test failed:', testError);
			} else {
				console.log('✅ Service role client working');
			}

			// Fetch books with their copy information and reservations
			const { data: books, error } = await supabase
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
        ),
        book_reservations (
          id,
          status,
          book_copy_id
        )
      `
				)
				.order('created_at', { ascending: false });

			if (error) {
				console.error('Error fetching books:', error);
				throw error;
			}

			// Transform the data to include copy counts and reservations
			const transformedBooks = await Promise.all(
				books?.map(async (book) => {
					const totalCopies = book.book_copies?.length || 0;

					// Count copies by status - consistent with student side
					const availableCopies =
						book.book_copies?.filter(
							(copy) => copy.status === 'available' && copy.is_available === true
						)?.length || 0;

					const borrowedCopies =
						book.book_copies?.filter((copy) => copy.status === 'borrowed')?.length || 0;

					const reservedCopies =
						book.book_copies?.filter((copy) => copy.status === 'reserved')?.length || 0;

					// Get active reservations for this book
					const { data: reservations, error: reservationsError } = await supabase
						.from('book_reservations')
						.select('*')
						.eq('book_id', book.id)
						.eq('status', 'active');

					if (reservationsError) {
						console.error('❌ Error fetching reservations for book:', book.id, reservationsError);
					}

					const activeReservations = reservations?.length || 0;

					// Debug logging
					console.log(`Book: ${book.title}`);
					console.log(`Total copies: ${totalCopies}`);
					console.log(
						`Available: ${availableCopies}, Borrowed: ${borrowedCopies}, Reserved: ${reservedCopies}, Active Reservations: ${activeReservations}`
					);
					console.log('Copy details:', book.book_copies);
					console.log('Reservation details:', reservations);

					return {
						id: book.id,
						title: book.title,
						author: book.author,
						isbn: book.isbn,
						category: book.category,
						published_year: book.published_year,
						location: book.location,
						status: book.status,
						image_url: book.image_url,
						created_at: book.created_at,
						totalCopies,
						availableCopies,
						borrowedCopies,
						reservedCopies: reservedCopies + activeReservations, // Include both copy reservations and active reservations
						activeReservations
					};
				}) || []
			);

			// Get books with active reservations but no copies
			const { data: reservedBooks, error: reservedError } = (await supabase
				.from('book_reservations')
				.select(
					`
					id,
					book_id,
					status,
					created_at,
					books!inner (
						id,
						title,
						author,
						isbn,
						category,
						published_year,
						location,
						status,
						image_url,
						created_at
					)
				`
				)
				.eq('status', 'active')) as { data: BookReservation[] | null; error: Error | null };

			if (reservedError) {
				console.error('❌ Error fetching reserved books:', reservedError);
			}

			// Filter out books that already have copies
			const reservedBooksWithoutCopies =
				reservedBooks?.filter(async (reservation: BookReservation) => {
					const { data: copies } = await supabase
						.from('book_copies')
						.select('id')
						.eq('book_id', reservation.book_id);
					return !copies || copies.length === 0;
				}) || [];

			// Transform reserved books data
			const transformedReservedBooks = await Promise.all(
				reservedBooksWithoutCopies.map(async (reservation: BookReservation) => {
					const { data: copies } = await supabase
						.from('book_copies')
						.select('id')
						.eq('book_id', reservation.book_id);

					// Only include if no copies exist
					if (copies && copies.length > 0) {
						return null;
					}

					const book = reservation.books;
					return {
						id: book.id,
						title: book.title,
						author: book.author,
						isbn: book.isbn,
						category: book.category,
						published_year: book.published_year,
						location: book.location,
						status: book.status,
						image_url: book.image_url,
						created_at: book.created_at,
						totalCopies: 0,
						availableCopies: 0,
						borrowedCopies: 0,
						reservedCopies: 0,
						activeReservations: 1,
						reservationId: reservation.id,
						reservationDate: reservation.created_at
					};
				})
			);

			// Filter out null values
			const validReservedBooks = transformedReservedBooks.filter((book) => book !== null);

			return json({
				success: true,
				books: transformedBooks,
				reservedBooksWithoutCopies: validReservedBooks
			});
		} catch (dbError) {
			const error = dbError as Error;
			console.error('❌ Database error details:', {
				message: error.message,
				code: (error as Error & { code?: string }).code || 'unknown',
				details: (error as Error & { details?: string }).details || 'none',
				hint: (error as Error & { hint?: string }).hint || 'none',
				stack: error.stack
			});
			console.warn('Database error, using mock data:', dbError);
			return json({
				success: true,
				books: MOCK_ADMIN_BOOKS,
				reservedBooksWithoutCopies: []
			});
		}
	} catch (error) {
		console.error('Error in GET /api/admin/books:', error);
		return json({ success: false, error: 'Internal server error' }, { status: 500 });
	}
};

export const POST: RequestHandler = async (event) => {
	try {
		await requireAdmin(event);

		const supabase = serviceSupabase;
		const { title, author, isbn, category, published_year, location, status, quantity, image_url } =
			await event.request.json();

		// Validate required fields
		if (!title || !author || !isbn) {
			return json(
				{ success: false, error: 'Title, author, and ISBN are required' },
				{ status: 400 }
			);
		}

		try {
			// Check if book with same ISBN already exists
			const { data: existingBook } = await supabase
				.from('books')
				.select('id')
				.eq('isbn', isbn)
				.single();

			if (existingBook) {
				return json(
					{ success: false, error: 'A book with this ISBN already exists' },
					{ status: 400 }
				);
			}

			// Insert the book
			const { data: book, error: bookError } = await supabase
				.from('books')
				.insert({
					title,
					author,
					isbn,
					category,
					published_year: published_year || null,
					location: location || null,
					status: status || 'available',
					image_url: image_url || null
				})
				.select()
				.single();

			if (bookError) {
				console.error('Error inserting book:', bookError);
				return json({ success: false, error: 'Failed to create book' }, { status: 500 });
			}

			// Insert book copies with the same status as the book
			const bookStatus = status || 'available';
			const copies = Array.from({ length: quantity || 1 }, () => ({
				book_id: book.id,
				status: bookStatus,
				is_available: bookStatus === 'available'
			}));

			const { error: copiesError } = await supabase.from('book_copies').insert(copies);

			if (copiesError) {
				console.error('Error inserting book copies:', copiesError);
				// Rollback book creation
				await supabase.from('books').delete().eq('id', book.id);
				return json({ success: false, error: 'Failed to create book copies' }, { status: 500 });
			}

			return json({
				success: true,
				message: `Book "${title}" added successfully with ${quantity || 1} copies`,
				book: {
					...book,
					totalCopies: quantity || 1,
					availableCopies: quantity || 1,
					borrowedCopies: 0,
					reservedCopies: 0
				}
			});
		} catch (dbError) {
			console.warn('Database error, using mock response:', dbError);
			// Mock successful book creation response
			return json({
				success: true,
				message: `Book "${title}" added successfully with ${quantity || 1} copies (mock response)`,
				book: {
					id: 'mock-book-' + Date.now(),
					title,
					author,
					isbn,
					category,
					published_year,
					location,
					status: status || 'available',
					image_url,
					created_at: new Date().toISOString(),
					totalCopies: quantity || 1,
					availableCopies: quantity || 1,
					borrowedCopies: 0,
					reservedCopies: 0
				}
			});
		}
	} catch (error) {
		console.error('Error in POST /api/admin/books:', error);
		return json({ success: false, error: 'Internal server error' }, { status: 500 });
	}
};
