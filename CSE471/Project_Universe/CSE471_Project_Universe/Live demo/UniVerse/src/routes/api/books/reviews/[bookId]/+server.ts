import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
export const GET: RequestHandler = async (event) => {
	try {
		const { params } = event;
		const { bookId } = params;

		if (!bookId) {
			return json({ success: false, error: 'Book ID is required' }, { status: 400 });
		}

		// Validate UUID format
		const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
		if (!uuidRegex.test(bookId)) {
			return json(
				{
					success: false,
					error: 'Invalid book ID format'
				},
				{ status: 400 }
			);
		}

		// Get reviews for the book directly from database
		const { data: reviews, error: reviewsError } = await event.locals.supabase
			.from('book_reviews')
			.select(
				`
				id,
				rating,
				review_text,
				review_date,
				user_id
			`
			)
			.eq('book_id', bookId)
			.order('review_date', { ascending: false });

		if (reviewsError) {
			console.error('Error fetching book reviews:', reviewsError);
			return json({ success: false, error: 'Failed to fetch reviews' }, { status: 500 });
		}

		// Get rating summary for the book using direct query
		const { data: ratingData, error: summaryError } = await event.locals.supabase
			.from('book_reviews')
			.select('rating')
			.eq('book_id', bookId);

		if (summaryError) {
			console.error('Error fetching rating summary:', summaryError);
			// Don't fail the entire request, just log the error
		}

		// Calculate rating summary
		let ratingSummary = null;
		if (ratingData && ratingData.length > 0) {
			const totalRatings = ratingData.length;
			const sumRatings = ratingData.reduce((sum, review) => sum + review.rating, 0);
			const averageRating = sumRatings / totalRatings;

			ratingSummary = {
				average_rating: Math.round(averageRating * 10) / 10, // Round to 1 decimal
				total_reviews: totalRatings,
				rating_distribution: {
					1: ratingData.filter((r) => r.rating === 1).length,
					2: ratingData.filter((r) => r.rating === 2).length,
					3: ratingData.filter((r) => r.rating === 3).length,
					4: ratingData.filter((r) => r.rating === 4).length,
					5: ratingData.filter((r) => r.rating === 5).length
				}
			};
		}

		// Transform reviews to include user information
		const transformedReviews =
			reviews?.map((review) => ({
				id: review.id,
				rating: review.rating,
				review_text: review.review_text,
				review_date: review.review_date,
				user_id: review.user_id,
				user_email: 'User ' + review.user_id.substring(0, 8) // Show partial user ID
			})) || [];

		return json({
			success: true,
			reviews: transformedReviews,
			ratingSummary: ratingSummary
		});
	} catch (error) {
		console.error('Error in GET /api/books/reviews/[bookId]:', error);
		return json({ success: false, error: 'Internal server error' }, { status: 500 });
	}
};

export const POST: RequestHandler = async (event) => {
	try {
		const { params, request, locals } = event;
		const { bookId } = params;

		if (!bookId) {
			return json({ success: false, error: 'Book ID is required' }, { status: 400 });
		}

		// Validate UUID format
		const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
		if (!uuidRegex.test(bookId)) {
			return json(
				{
					success: false,
					error: 'Invalid book ID format'
				},
				{ status: 400 }
			);
		}

		// Check if user is authenticated
		const {
			data: { user },
			error: authError
		} = await locals.supabase.auth.getUser();
		if (authError || !user) {
			return json({ success: false, error: 'Authentication required' }, { status: 401 });
		}

		// Parse request body
		const { rating, reviewText } = await request.json();

		if (!rating || rating < 1 || rating > 5) {
			return json({ success: false, error: 'Valid rating (1-5) is required' }, { status: 400 });
		}

		// Check if user has already reviewed this book
		const { data: existingReview, error: checkError } = await locals.supabase
			.from('book_reviews')
			.select('id, rating, review_text')
			.eq('book_id', bookId)
			.eq('user_id', user.id)
			.single();

		if (checkError && checkError.code !== 'PGRST116') {
			// PGRST116 = no rows returned
			console.error('Error checking existing review:', checkError);
			return json({ success: false, error: 'Failed to check existing review' }, { status: 500 });
		}

		let review;
		let message;

		if (existingReview) {
			// Update existing review
			const { data: updatedReview, error: updateError } = await locals.supabase
				.from('book_reviews')
				.update({
					rating: rating,
					review_text: reviewText || null,
					review_date: new Date().toISOString(),
					updated_at: new Date().toISOString()
				})
				.eq('id', existingReview.id)
				.select()
				.single();

			if (updateError) {
				console.error('Error updating review:', updateError);
				return json({ success: false, error: 'Failed to update review' }, { status: 500 });
			}

			review = updatedReview;
			message = 'Review updated successfully';
		} else {
			// Insert new review
			const { data: newReview, error: insertError } = await locals.supabase
				.from('book_reviews')
				.insert({
					book_id: bookId,
					user_id: user.id,
					rating: rating,
					review_text: reviewText || null,
					review_date: new Date().toISOString()
				})
				.select()
				.single();

			if (insertError) {
				console.error('Error inserting review:', insertError);
				return json({ success: false, error: 'Failed to submit review' }, { status: 500 });
			}

			review = newReview;
			message = 'Review submitted successfully';
		}

		return json({
			success: true,
			message: message,
			review: review
		});
	} catch (error) {
		console.error('Error in POST /api/books/reviews/[bookId]:', error);
		return json({ success: false, error: 'Internal server error' }, { status: 500 });
	}
};
