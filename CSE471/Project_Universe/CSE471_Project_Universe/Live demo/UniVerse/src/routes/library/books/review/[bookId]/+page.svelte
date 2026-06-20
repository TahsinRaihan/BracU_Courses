<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { Button } from '$lib/components/ui/button';
	import {
		Card,
		CardContent,
		CardDescription,
		CardHeader,
		CardTitle
	} from '$lib/components/ui/card';
	// Badge component not available, using custom styling
	import { Input } from '$lib/components/ui/input';
	import { Label } from '$lib/components/ui/label';
	import { Separator } from '$lib/components/ui/separator';
	import { Textarea } from '$lib/components/ui/textarea';
	import {
		BookOpen,
		User,
		Calendar,
		MapPin,
		Star,
		ArrowLeft,
		Send,
		MessageSquare,
		ThumbsUp,
		Heart
	} from '@lucide/svelte';

	export let data: any;

	let book = data.book;
	let reviews = data.reviews || [];
	let ratingSummary = data.ratingSummary;

	let userRating = 0;
	let reviewText = '';
	let isSubmitting = false;
	let showReviewForm = false;
	let isUpdating = false;

	onMount(() => {
		if (!book) {
			goto('/library/books');
		}
	});

	async function submitReview() {
		if (userRating === 0) {
			alert('Please select a rating');
			return;
		}

		isSubmitting = true;
		try {
			const response = await fetch(`/api/books/reviews/${book.id}`, {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ rating: userRating, reviewText })
			});

			if (response.ok) {
				const result = await response.json();

				// Optimistically update the UI
				await updateReviewData();

				// Reset form
				userRating = 0;
				reviewText = '';
				showReviewForm = false;

				// Show success message
				alert('Review submitted successfully!');
			} else {
				const error = await response.json();
				alert(`Error: ${error.error}`);
			}
		} catch (error) {
			alert('Error submitting review');
		} finally {
			isSubmitting = false;
		}
	}

	async function updateReviewData() {
		isUpdating = true;
		try {
			// Fetch updated reviews and rating summary in a single call
			const response = await fetch(`/api/books/reviews/${book.id}`);

			if (response.ok) {
				const data = await response.json();
				reviews = data.reviews || [];
				ratingSummary = data.ratingSummary;
			}
		} catch (error) {
			console.error('Error updating review data:', error);
		} finally {
			isUpdating = false;
		}
	}

	function getRatingStars(rating: number) {
		return Array.from({ length: 5 }, (_, i) => i < rating);
	}

	function getRatingColor(rating: number) {
		if (rating >= 4) return 'text-green-600';
		if (rating >= 3) return 'text-yellow-600';
		return 'text-red-600';
	}

	function getRatingLabel(rating: number) {
		if (rating === 5) return 'Excellent';
		if (rating === 4) return 'Very Good';
		if (rating === 3) return 'Good';
		if (rating === 2) return 'Fair';
		if (rating === 1) return 'Poor';
		return '';
	}
</script>

<svelte:head>
	<title>{book?.title} - Reviews - UniVerse Library</title>
</svelte:head>

<div class="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50">
	<!-- Header Section -->
	<div class="border-b bg-white shadow-sm">
		<div class="mx-auto max-w-7xl px-6 py-8">
			<div class="flex flex-col gap-6 lg:flex-row lg:items-center lg:justify-between">
				<div class="flex items-center gap-4">
					<Button onclick={() => goto('/library/books')} variant="outline" class="p-2">
						<ArrowLeft class="h-4 w-4" />
					</Button>
					<div>
						<h1 class="text-3xl font-bold text-gray-900 sm:text-4xl">Book Reviews</h1>
						<p class="mt-2 text-lg text-gray-600">
							Read and write reviews for "{book?.title}"
						</p>
					</div>
				</div>

				<div class="flex items-center gap-3">
					<Button onclick={() => goto('/library/books')} variant="outline" class="px-6 py-3">
						📚 Explore Books
					</Button>
					<div class="rounded-lg border border-blue-200 bg-blue-50 px-3 py-1">
						<span class="text-sm font-medium text-blue-700"> Current: Book Reviews </span>
					</div>
				</div>
			</div>
		</div>
	</div>

	<div class="mx-auto max-w-7xl px-6 py-8">
		<!-- Book Information Card -->
		<Card class="mb-8 border-0 bg-white/80 shadow-lg backdrop-blur-sm">
			<CardContent class="p-8">
				<div class="grid gap-8 md:grid-cols-2">
					<!-- Book Cover -->
					<div
						class="flex aspect-[3/4] items-center justify-center overflow-hidden rounded-2xl bg-gradient-to-br from-blue-100 to-indigo-100"
					>
						{#if book?.image_url}
							<img src={book.image_url} alt={book.title} class="h-full w-full object-cover" />
						{:else}
							<BookOpen class="h-24 w-24 text-blue-400" />
						{/if}
					</div>

					<!-- Book Details -->
					<div class="space-y-6">
						<div>
							<h2 class="mb-3 text-3xl font-bold text-gray-900">{book?.title}</h2>
							<p class="mb-4 text-xl text-gray-600">by {book?.author}</p>

							<!-- Rating Summary -->
							{#if ratingSummary}
								<div class="mb-6 flex items-center gap-4">
									<div class="flex items-center gap-2">
										<div class="text-3xl font-bold {getRatingColor(ratingSummary.average_rating)}">
											{ratingSummary.average_rating}
										</div>
										<div class="flex items-center gap-1">
											{#each getRatingStars(Math.round(ratingSummary.average_rating)) as isFilled}
												<Star
													class="h-6 w-6 {isFilled
														? 'fill-yellow-400 text-yellow-400'
														: 'text-gray-300'}"
												/>
											{/each}
										</div>
									</div>
									<div class="text-gray-600">
										<span class="font-medium">{ratingSummary.total_reviews}</span> reviews
									</div>
								</div>
							{/if}
						</div>

						<!-- Book Metadata -->
						<div class="space-y-3">
							<div class="flex items-center gap-2">
								<BookOpen class="h-5 w-5 text-gray-400" />
								<span class="text-gray-600">ISBN:</span>
								<span class="font-medium">{book?.isbn}</span>
							</div>

							<div class="flex items-center gap-2">
								<MapPin class="h-5 w-5 text-gray-400" />
								<span class="text-gray-600">Category:</span>
								<div
									class="inline-flex items-center rounded-full bg-gray-100 px-2 py-1 text-xs font-medium text-gray-800"
								>
									{book?.category}
								</div>
							</div>

							<div class="flex items-center gap-2">
								<Calendar class="h-5 w-5 text-gray-400" />
								<span class="text-gray-600">Published:</span>
								<span class="font-medium">{book?.published_year || 'N/A'}</span>
							</div>

							<div class="flex items-center gap-2">
								<MapPin class="h-5 w-5 text-gray-400" />
								<span class="text-gray-600">Location:</span>
								<span class="font-medium">{book?.location}</span>
							</div>
						</div>

						<!-- Write Review Button -->
						{#if !showReviewForm}
							<Button
								onclick={() => (showReviewForm = true)}
								class="w-full border-0 bg-gradient-to-r from-blue-600 to-purple-600 text-white transition-all duration-300 hover:from-blue-700 hover:to-purple-700"
							>
								<MessageSquare class="mr-2 h-4 w-4" />
								{reviews.find((r: any) => r.user_email === data.user.email)
									? 'Update Your Review'
									: 'Write a Review'}
							</Button>
						{/if}
					</div>
				</div>
			</CardContent>
		</Card>

		<!-- Review Form -->
		{#if showReviewForm}
			<Card class="mb-8 border-0 bg-gradient-to-r from-blue-50 to-indigo-50 shadow-lg">
				<CardHeader>
					<CardTitle class="text-xl text-gray-900">Share Your Thoughts</CardTitle>
					<CardDescription>
						Help other readers by sharing your experience with this book
					</CardDescription>
				</CardHeader>
				<CardContent class="space-y-6">
					<!-- Rating Selection -->
					<div>
						<Label class="mb-3 block text-sm font-medium text-gray-700">Your Rating</Label>
						<div class="flex items-center gap-4">
							<div class="flex items-center gap-1">
								{#each Array.from({ length: 5 }, (_, i) => i + 1) as starValue}
									<button
										onclick={() => (userRating = starValue)}
										class="transition-all duration-200 hover:scale-110"
									>
										<Star
											class="h-8 w-8 {starValue <= userRating
												? 'fill-yellow-400 text-yellow-400'
												: 'text-gray-300'}"
										/>
									</button>
								{/each}
							</div>
							{#if userRating > 0}
								<div class="ml-4">
									<span class="text-lg font-medium {getRatingColor(userRating)}">
										{getRatingLabel(userRating)}
									</span>
								</div>
							{/if}
						</div>
					</div>

					<!-- Review Text -->
					<div>
						<Label for="review" class="mb-3 block text-sm font-medium text-gray-700">
							Your Review (Optional)
						</Label>
						<Textarea
							id="review"
							bind:value={reviewText}
							placeholder="Share your thoughts about this book..."
							rows={4}
							class="w-full resize-none rounded-lg border border-gray-300 px-4 py-3 focus:border-blue-500 focus:ring-2 focus:ring-blue-500 focus:outline-none"
						/>
					</div>

					<!-- Submit Button -->
					<Button
						onclick={submitReview}
						disabled={isSubmitting || userRating === 0}
						class="w-full border-0 bg-gradient-to-r from-green-600 to-teal-600 text-white transition-all duration-300 hover:from-green-700 hover:to-teal-700 disabled:opacity-50"
					>
						<Send class="mr-2 h-4 w-4" />
						{isSubmitting ? 'Submitting...' : 'Submit Review'}
					</Button>
				</CardContent>
			</Card>
		{/if}

		<!-- Reviews Section -->
		<Card class="border-0 bg-white/80 shadow-lg backdrop-blur-sm">
			<CardHeader>
				<div class="flex items-center justify-between">
					<div class="flex items-center gap-3">
						<div>
							<CardTitle class="text-2xl text-gray-900">Reader Reviews</CardTitle>
							<CardDescription>
								{reviews.length} review{reviews.length !== 1 ? 's' : ''} from our community
							</CardDescription>
						</div>
						{#if isUpdating}
							<div class="flex items-center gap-2 text-blue-600">
								<div
									class="h-4 w-4 animate-spin rounded-full border-2 border-blue-600 border-t-transparent"
								></div>
								<span class="text-sm">Updating...</span>
							</div>
						{:else}
							<Button onclick={updateReviewData} variant="outline" size="sm" class="text-xs">
								<div class="mr-1 h-3 w-3">↻</div>
								Refresh
							</Button>
						{/if}
					</div>

					{#if ratingSummary}
						<div class="text-right">
							<div class="text-2xl font-bold text-gray-900">{ratingSummary.average_rating}</div>
							<div class="text-sm text-gray-600">Average Rating</div>
						</div>
					{/if}
				</div>
			</CardHeader>

			<CardContent>
				{#if reviews.length === 0}
					<div class="py-16 text-center">
						<MessageSquare class="mx-auto mb-4 h-16 w-16 text-gray-400" />
						<h3 class="mb-2 text-lg font-medium text-gray-900">No reviews yet</h3>
						<p class="mb-6 text-gray-600">Be the first to share your thoughts about this book!</p>
						<Button onclick={() => (showReviewForm = true)} class="px-6 py-3">
							Write First Review
						</Button>
					</div>
				{:else}
					<div class="space-y-6">
						{#each reviews as review}
							<div class="border-b border-gray-200 pb-6 last:border-b-0">
								<div class="mb-4 flex items-start justify-between">
									<div class="flex items-center gap-3">
										<div
											class="flex h-10 w-10 items-center justify-center rounded-full bg-gradient-to-br from-blue-500 to-purple-600 font-semibold text-white"
										>
											{review.user_email?.charAt(0).toUpperCase() || 'U'}
										</div>
										<div>
											<div class="font-medium text-gray-900">
												{review.user_email || 'Anonymous User'}
											</div>
											<div class="text-sm text-gray-500">
												{new Date(review.review_date).toLocaleDateString('en-US', {
													year: 'numeric',
													month: 'long',
													day: 'numeric'
												})}
											</div>
										</div>
									</div>

									<div class="flex items-center gap-1">
										{#each getRatingStars(review.rating) as isFilled}
											<Star
												class="h-5 w-5 {isFilled
													? 'fill-yellow-400 text-yellow-400'
													: 'text-gray-300'}"
											/>
										{/each}
									</div>
								</div>

								{#if review.review_text}
									<p class="leading-relaxed text-gray-700">{review.review_text}</p>
								{/if}

								<div class="mt-4 flex items-center gap-4 text-sm text-gray-500">
									<button class="flex items-center gap-1 transition-colors hover:text-blue-600">
										<ThumbsUp class="h-4 w-4" />
										Helpful
									</button>
									<button class="flex items-center gap-1 transition-colors hover:text-red-600">
										<Heart class="h-4 w-4" />
										Like
									</button>
								</div>
							</div>
						{/each}
					</div>
				{/if}
			</CardContent>
		</Card>
	</div>
</div>
