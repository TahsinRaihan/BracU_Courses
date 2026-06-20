import { supabase } from '$lib/supabase';
import type { Book } from '$lib/types/book';

// Mock data for when database is not available
const MOCK_BOOKS: Book[] = [
	{
		id: '1',
		title: 'The Great Gatsby',
		author: 'F. Scott Fitzgerald',
		isbn: '978-0743273565',
		status: 'available',
		category: 'Fiction',
		published_year: 1925,
		location: 'Shelf A1',
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
		status: 'available',
		category: 'Fiction',
		published_year: 1960,
		location: 'Shelf A2',
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
		status: 'available',
		category: 'Fiction',
		published_year: 1949,
		location: 'Shelf A3',
		image_url: 'https://example.com/1984.jpg',
		created_at: '2024-01-01T00:00:00Z',
		totalCopies: 1,
		availableCopies: 0,
		borrowedCopies: 1,
		reservedCopies: 0
	}
];

export class BookRepository {
	async getAllBooks(): Promise<Book[]> {
		try {
			const { data, error } = await supabase
				.from('books')
				.select(
					`
					id, 
					title, 
					author, 
					isbn, 
					status, 
					category, 
					published_year, 
					location, 
					image_url, 
					created_at,
					book_copies (
						id,
						status,
						is_available
					)
				`
				)
				.order('title');

			if (error) {
				throw new Error(`Failed to fetch books: ${error.message}`);
			}

			// Transform the data to include copy counts
			return (data || []).map((book) => {
				const totalCopies = book.book_copies?.length || 0;
				const availableCopies =
					book.book_copies?.filter(
						(copy) => copy.status === 'available' && copy.is_available === true
					)?.length || 0;
				const borrowedCopies =
					book.book_copies?.filter((copy) => copy.status === 'borrowed')?.length || 0;
				const reservedCopies =
					book.book_copies?.filter((copy) => copy.status === 'reserved')?.length || 0;

				return {
					...book,
					totalCopies,
					availableCopies,
					borrowedCopies,
					reservedCopies
				};
			});
		} catch (error) {
			console.warn('Database connection failed, using mock data:', error);
			return MOCK_BOOKS;
		}
	}

	async getBookById(id: string): Promise<Book | null> {
		try {
			const { data, error } = await supabase
				.from('books')
				.select(
					`
					id, 
					title, 
					author, 
					isbn, 
					status, 
					category, 
					published_year, 
					location, 
					image_url, 
					created_at,
					book_copies (
						id,
						status,
						is_available
					)
				`
				)
				.eq('id', id)
				.single();

			if (error) {
				if (error.code === 'PGRST116') {
					return null; // No rows returned
				}
				throw new Error(`Failed to fetch book: ${error.message}`);
			}

			// Transform the data to include copy counts
			const totalCopies = data.book_copies?.length || 0;
			const availableCopies =
				data.book_copies?.filter((copy) => copy.status === 'available')?.length || 0;
			const borrowedCopies =
				data.book_copies?.filter((copy) => copy.status === 'borrowed')?.length || 0;
			const reservedCopies =
				data.book_copies?.filter((copy) => copy.status === 'reserved')?.length || 0;

			return {
				...data,
				totalCopies,
				availableCopies,
				borrowedCopies,
				reservedCopies
			};
		} catch (error) {
			console.warn('Database connection failed, using mock data:', error);
			return MOCK_BOOKS.find((book) => book.id === id) || null;
		}
	}

	async searchBooks(query: string): Promise<Book[]> {
		try {
			const { data, error } = await supabase
				.from('books')
				.select(
					`
					id, 
					title, 
					author, 
					isbn, 
					status, 
					category, 
					published_year, 
					location, 
					image_url, 
					created_at,
					book_copies (
						id,
						status,
						is_available
					)
				`
				)
				.or(`title.ilike.%${query}%,author.ilike.%${query}%`)
				.order('title');

			if (error) {
				throw new Error(`Failed to fetch books: ${error.message}`);
			}

			// Transform the data to include copy counts
			return (data || []).map((book) => {
				const totalCopies = book.book_copies?.length || 0;
				const availableCopies =
					book.book_copies?.filter(
						(copy) => copy.status === 'available' && copy.is_available === true
					)?.length || 0;
				const borrowedCopies =
					book.book_copies?.filter((copy) => copy.status === 'borrowed')?.length || 0;
				const reservedCopies =
					book.book_copies?.filter((copy) => copy.status === 'reserved')?.length || 0;

				return {
					...book,
					totalCopies,
					availableCopies,
					borrowedCopies,
					reservedCopies
				};
			});
		} catch (error) {
			console.warn('Database connection failed, using mock data:', error);
			return MOCK_BOOKS.filter(
				(book) =>
					book.title.toLowerCase().includes(query.toLowerCase()) ||
					book.author.toLowerCase().includes(query.toLowerCase())
			);
		}
	}

	async getBooksByStatus(status: Book['status']): Promise<Book[]> {
		try {
			const { data, error } = await supabase
				.from('books')
				.select(
					`
					id, 
					title, 
					author, 
					isbn, 
					status, 
					category, 
					published_year, 
					location, 
					image_url, 
					created_at,
					book_copies (
						id,
						status,
						is_available
					)
				`
				)
				.eq('status', status)
				.order('title');

			if (error) {
				throw new Error(`Failed to fetch books by status: ${error.message}`);
			}

			// Transform the data to include copy counts
			return (data || []).map((book) => {
				const totalCopies = book.book_copies?.length || 0;
				const availableCopies =
					book.book_copies?.filter(
						(copy) => copy.status === 'available' && copy.is_available === true
					)?.length || 0;
				const borrowedCopies =
					book.book_copies?.filter((copy) => copy.status === 'borrowed')?.length || 0;
				const reservedCopies =
					book.book_copies?.filter((copy) => copy.status === 'reserved')?.length || 0;

				return {
					...book,
					totalCopies,
					availableCopies,
					borrowedCopies,
					reservedCopies
				};
			});
		} catch (error) {
			console.warn('Database connection failed, using mock data:', error);
			return MOCK_BOOKS.filter((book) => book.status === status);
		}
	}

	async canDeleteBook(bookId: string): Promise<{
		canDelete: boolean;
		reason?: string;
		availableCopies: number;
		borrowedCopies: number;
		reservedCopies: number;
	}> {
		try {
			const { data, error } = await supabase
				.from('book_copies')
				.select('status, is_available')
				.eq('book_id', bookId);

			if (error) {
				throw new Error(`Failed to check book deletion status: ${error.message}`);
			}

			const copies = data || [];
			const availableCopies = copies.filter(
				(copy) => copy.status === 'available' && copy.is_available
			).length;
			const borrowedCopies = copies.filter((copy) => copy.status === 'borrowed').length;
			const reservedCopies = copies.filter((copy) => copy.status === 'reserved').length;

			// Check if there are any borrowed or reserved copies
			if (borrowedCopies > 0) {
				return {
					canDelete: false,
					reason: `Cannot delete book: ${borrowedCopies} copy(ies) are currently borrowed`,
					availableCopies,
					borrowedCopies,
					reservedCopies
				};
			}

			if (reservedCopies > 0) {
				return {
					canDelete: false,
					reason: `Cannot delete book: ${reservedCopies} copy(ies) are currently reserved`,
					availableCopies,
					borrowedCopies,
					reservedCopies
				};
			}

			return {
				canDelete: true,
				availableCopies,
				borrowedCopies,
				reservedCopies
			};
		} catch (error) {
			console.warn('Database connection failed, using mock data:', error);
			const book = MOCK_BOOKS.find((b) => b.id === bookId);
			if (!book) {
				return {
					canDelete: false,
					reason: 'Book not found',
					availableCopies: 0,
					borrowedCopies: 0,
					reservedCopies: 0
				};
			}
			return {
				canDelete: book.borrowedCopies === 0 && book.reservedCopies === 0,
				reason:
					book.borrowedCopies > 0
						? `Cannot delete book: ${book.borrowedCopies} copy(ies) are currently borrowed`
						: book.reservedCopies > 0
							? `Cannot delete book: ${book.reservedCopies} copy(ies) are currently reserved`
							: undefined,
				availableCopies: book.availableCopies,
				borrowedCopies: book.borrowedCopies,
				reservedCopies: book.reservedCopies
			};
		}
	}

	async canDeleteCopy(
		copyId: string
	): Promise<{ canDelete: boolean; reason?: string; status: string; isAvailable: boolean }> {
		try {
			const { data, error } = await supabase
				.from('book_copies')
				.select('status, is_available')
				.eq('id', copyId)
				.single();

			if (error) {
				throw new Error(`Failed to check copy deletion status: ${error.message}`);
			}

			const copy = data;

			// Check if the copy is borrowed or reserved
			if (copy.status === 'borrowed' || copy.status === 'reserved') {
				return {
					canDelete: false,
					reason: `Cannot delete copy with status '${copy.status}'. Only available copies can be deleted.`,
					status: copy.status,
					isAvailable: copy.is_available
				};
			}

			// Additional check for availability
			if (!copy.is_available) {
				return {
					canDelete: false,
					reason: 'Cannot delete copy that is not available. Please check the copy status.',
					status: copy.status,
					isAvailable: copy.is_available
				};
			}

			return {
				canDelete: true,
				status: copy.status,
				isAvailable: copy.is_available
			};
		} catch (error) {
			console.warn('Database connection failed, using mock data:', error);
			// For mock data, assume copies can be deleted if they're available
			return {
				canDelete: true,
				status: 'available',
				isAvailable: true
			};
		}
	}
}
