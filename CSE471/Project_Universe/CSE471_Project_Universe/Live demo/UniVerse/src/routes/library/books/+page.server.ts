import { redirect } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';
import { BookController } from '$lib/controllers/book.controller';

export const load: PageServerLoad = async ({ locals }) => {
	// Check if user is authenticated
	const {
		data: { user },
		error: authError
	} = await locals.supabase.auth.getUser();

	// Require authentication
	if (authError || !user) {
		throw redirect(303, '/auth/login');
	}

	const bookController = new BookController();

	try {
		const result = await bookController.getAllBooks();

		if (result.success && result.data) {
			return {
				books: result.data,
				user: {
					id: user.id,
					email: user.email
				}
			};
		} else {
			console.error('Failed to load books:', result.error);
			return {
				books: [],
				user: {
					id: user.id,
					email: user.email
				}
			};
		}
	} catch (error) {
		console.error('Error in books page load:', error);
		return {
			books: [],
			user: {
				id: user.id,
				email: user.email
			}
		};
	}
};
