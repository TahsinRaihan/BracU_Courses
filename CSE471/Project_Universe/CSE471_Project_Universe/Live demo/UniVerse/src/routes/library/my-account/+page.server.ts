import { redirect } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';

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

	// Return user data for the page
	return {
		user: {
			id: user.id,
			email: user.email
		}
	};
};
