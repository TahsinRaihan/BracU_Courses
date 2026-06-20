import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { supabase } from '$lib/supabase';

// Mock data for when database is not available
const MOCK_BOOKS = [
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

export const GET: RequestHandler = async () => {
	try {
		console.log('🔍 API: Starting to fetch books...');

		// Get all books with their copy information
		const { data: books, error: booksError } = await supabase
			.from('books')
			.select('*')
			.order('title');

		console.log('📚 API: Books query result:', { books, booksError });

		if (booksError) {
			console.error('❌ API: Error fetching books:', booksError);
			console.log('🔄 API: Using mock data due to database error');
			return json(MOCK_BOOKS);
		}

		if (!books || books.length === 0) {
			console.log('⚠️ API: No books found in database, using mock data');
			return json(MOCK_BOOKS);
		}

		console.log(`✅ API: Found ${books.length} books, processing copies...`);

		// Get copy information for each book
		const booksWithCopies = await Promise.all(
			books.map(async (book) => {
				const { data: copies, error: copiesError } = await supabase
					.from('book_copies')
					.select('*')
					.eq('book_id', book.id);

				if (copiesError) {
					console.error('❌ API: Error fetching copies for book:', book.id, copiesError);
					return {
						...book,
						totalCopies: 0,
						availableCopies: 0,
						borrowedCopies: 0,
						reservedCopies: 0
					};
				}

				const totalCopies = copies.length;
				const availableCopies = copies.filter(
					(copy) => copy.status === 'available' && copy.is_available
				).length;
				const borrowedCopies = copies.filter((copy) => copy.status === 'borrowed').length;
				const reservedCopies = copies.filter((copy) => copy.status === 'reserved').length;

				console.log(
					`📖 Book: ${book.title} - Copies: ${totalCopies} total, ${availableCopies} available`
				);

				return {
					...book,
					totalCopies,
					availableCopies,
					borrowedCopies,
					reservedCopies,
					// Ensure the book ID is properly formatted for frontend use
					id: book.id
				};
			})
		);

		console.log(`🎉 API: Successfully processed ${booksWithCopies.length} books`);
		return json(booksWithCopies);
	} catch (error) {
		console.error('💥 API: Unexpected error:', error);
		console.log('🔄 API: Using mock data due to error');
		return json(MOCK_BOOKS);
	}
};
