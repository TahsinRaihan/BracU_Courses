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
	import { Separator } from '$lib/components/ui/separator';
	import { Tabs, TabsContent, TabsList, TabsTrigger } from '$lib/components/ui/tabs';
	import {
		BookOpen,
		Calendar,
		Clock,
		CheckCircle,
		AlertCircle,
		ArrowLeft,
		History,
		Bookmark,
		TrendingUp,
		User,
		MapPin,
		Star,
		Home,
		X
	} from '@lucide/svelte';
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();

	let reservations = $state<any[]>([]);
	let borrowings = $state<any[]>([]);
	let isLoading = $state(true);
	let activeTab = $state('reservations');
	let errorMessage = $state('');
	let hasError = $state(false);

	onMount(async () => {
		await loadUserData();
	});

	async function loadUserData() {
		try {
			hasError = false;
			errorMessage = '';

			// Load reservations
			const reservationsResponse = await fetch('/api/books/my-reservations');
			if (reservationsResponse.ok) {
				const result = await reservationsResponse.json();
				if (result.success) {
					reservations = result.reservations || [];
				} else {
					console.error('Failed to load reservations:', result.error);
					hasError = true;
					errorMessage = 'Failed to load reservations: ' + result.error;
				}
			} else {
				const errorData = await reservationsResponse.json();
				// Check if it's a "no users" error
				if (errorData.error && errorData.error.includes('No users exist')) {
					console.log('No users in database - showing empty state');
					reservations = [];
					borrowings = [];
					hasError = false;
					errorMessage = '';
				} else {
					console.error('Reservations API error:', reservationsResponse.status);
					hasError = true;
					errorMessage = 'Failed to load reservations. Please try again.';
				}
			}

			// Load borrowing history
			const borrowingsResponse = await fetch('/api/books/borrowing-history');
			if (borrowingsResponse.ok) {
				const result = await borrowingsResponse.json();
				if (result.success) {
					borrowings = result.borrowings || [];
				} else {
					console.error('Failed to load borrowings:', result.error);
					hasError = true;
					errorMessage = 'Failed to load borrowing history: ' + result.error;
				}
			} else {
				const errorData = await borrowingsResponse.json();
				// Check if it's a "no users" error
				if (errorData.error && errorData.error.includes('No users exist')) {
					console.log('No users in database - showing empty state');
					reservations = [];
					borrowings = [];
					hasError = false;
					errorMessage = '';
				} else {
					console.error('Borrowings API error:', borrowingsResponse.status);
					hasError = true;
					errorMessage = 'Failed to load borrowing history. Please try again.';
				}
			}
		} catch (error) {
			console.error('Error loading user data:', error);
			hasError = true;
			errorMessage = 'Network error. Please check your connection and try again.';
		} finally {
			isLoading = false;
		}
	}

	function getStatusColor(status: string) {
		switch (status) {
			case 'active':
				return 'bg-blue-100 text-blue-800 border-blue-200';
			case 'expired':
				return 'bg-red-100 text-red-800 border-red-200';
			case 'cancelled':
				return 'bg-gray-100 text-gray-800 border-gray-200';
			case 'fulfilled':
				return 'bg-green-100 text-green-800 border-green-200';
			case 'borrowed':
				return 'bg-orange-100 text-orange-800 border-orange-200';
			case 'returned':
				return 'bg-green-100 text-green-800 border-green-200';
			case 'overdue':
				return 'bg-red-100 text-red-800 border-red-200';
			default:
				return 'bg-gray-100 text-gray-800 border-gray-200';
		}
	}

	function getStatusIcon(status: string) {
		switch (status) {
			case 'active':
				return '🔵';
			case 'expired':
				return '⏰';
			case 'cancelled':
				return '❌';
			case 'fulfilled':
				return '✅';
			case 'borrowed':
				return '📚';
			case 'returned':
				return '✅';
			case 'overdue':
				return '⚠️';
			default:
				return '❓';
		}
	}

	function formatDate(dateString: string) {
		return new Date(dateString).toLocaleDateString('en-US', {
			year: 'numeric',
			month: 'short',
			day: 'numeric'
		});
	}

	function getDaysRemaining(expiryDate: string) {
		const expiry = new Date(expiryDate);
		const now = new Date();
		const diffTime = expiry.getTime() - now.getTime();
		const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
		return diffDays;
	}

	function getDaysOverdue(dueDate: string) {
		const due = new Date(dueDate);
		const now = new Date();
		const diffTime = now.getTime() - due.getTime();
		const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
		return diffDays > 0 ? diffDays : 0;
	}

	async function returnBook(borrowingId: string) {
		try {
			// Find the borrowing object to get the book ID
			const borrowing = borrowings.find((b) => b.id === borrowingId);
			if (!borrowing) {
				alert('Borrowing record not found.');
				return;
			}

			const response = await fetch('/api/books/return', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ bookId: borrowing.book_id })
			});

			if (response.ok) {
				const result = await response.json();
				if (result.success) {
					// Reload user data to reflect the return
					await loadUserData();
					// Show success message (you can add a toast notification here)
					alert('Book returned successfully!');
				} else {
					alert('Failed to return book: ' + result.error);
				}
			} else {
				alert('Failed to return book. Please try again.');
			}
		} catch (error) {
			console.error('Error returning book:', error);
			alert('Error returning book. Please try again.');
		}
	}

	async function cancelReservation(bookId: string) {
		try {
			const response = await fetch('/api/books/cancel-reservation', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ bookId })
			});

			if (response.ok) {
				const result = await response.json();
				if (result.success) {
					// Reload user data to reflect the cancellation
					await loadUserData();
					alert('Reservation cancelled successfully!');
				} else {
					alert('Failed to cancel reservation: ' + result.error);
				}
			} else {
				alert('Failed to cancel reservation. Please try again.');
			}
		} catch (error) {
			console.error('Error cancelling reservation:', error);
			alert('Error cancelling reservation. Please try again.');
		}
	}
</script>

<svelte:head>
	<title>My Library History - UniVerse Library</title>
</svelte:head>

<div class="min-h-screen w-full bg-gradient-to-br from-blue-50 via-white to-indigo-50">
	<!-- Navigation Bar -->
	<div class="border-b bg-white/95 shadow-sm backdrop-blur-sm">
		<div class="mx-auto w-full max-w-7xl px-4 py-4 sm:px-6 lg:px-8">
			<div class="flex items-center justify-between">
				<div class="flex items-center space-x-4">
					<Button
						onclick={() => goto('/myspace')}
						variant="outline"
						class="flex items-center space-x-2 border-gray-300 bg-white/80 text-gray-700 hover:bg-gray-50"
					>
						<ArrowLeft class="h-4 w-4" />
						<span>Return to MySpace</span>
					</Button>
					<Button
						onclick={() => goto('/library')}
						variant="ghost"
						class="flex items-center space-x-2 text-gray-600 hover:bg-gray-100 hover:text-gray-900"
					>
						<Home class="h-4 w-4" />
						<span>Library Home</span>
					</Button>
				</div>
				<div class="text-sm text-gray-500">My Library History</div>
			</div>
		</div>
	</div>

	<!-- Header Section -->
	<div class="border-b bg-white shadow-sm">
		<div class="mx-auto w-full max-w-7xl px-4 py-6 sm:px-6 sm:py-8 lg:px-8">
			<div class="flex flex-col gap-4 sm:gap-6 lg:flex-row lg:items-center lg:justify-between">
				<div class="flex items-center gap-4">
					<Button onclick={() => goto('/library')} variant="outline" class="p-2">
						<ArrowLeft class="h-4 w-4" />
					</Button>
					<div>
						<h1 class="text-2xl font-bold text-gray-900 sm:text-3xl lg:text-4xl">
							My Library History
						</h1>
						<p class="mt-2 text-base text-gray-600 sm:text-lg">
							Track your reading journey, reservations, and borrowing history
						</p>
					</div>
				</div>

				<div class="flex items-center gap-3">
					<Button onclick={loadUserData} disabled={isLoading} variant="outline" class="px-4 py-2">
						{#if isLoading}
							<div class="mr-2 h-4 w-4 animate-spin rounded-full border-b-2 border-blue-600"></div>
						{/if}
						🔄 Refresh
					</Button>
					<Button onclick={() => goto('/library/books')} class="px-6 py-3">📚 Explore Books</Button>
					<div class="rounded-lg border border-blue-200 bg-blue-50 px-3 py-1">
						<span class="text-sm font-medium text-blue-700"> Current: My Library History </span>
					</div>
				</div>
			</div>
		</div>
	</div>

	<!-- Error Message -->
	{#if hasError}
		<div class="mx-auto w-full max-w-7xl px-4 py-4 sm:px-6 lg:px-8">
			<div class="rounded-lg border border-red-200 bg-red-50 p-4">
				<div class="flex items-center gap-3">
					<AlertCircle class="h-5 w-5 text-red-600" />
					<div>
						<h3 class="text-sm font-medium text-red-800">Error Loading Data</h3>
						<p class="mt-1 text-sm text-red-700">{errorMessage}</p>
					</div>
					<Button
						onclick={loadUserData}
						variant="outline"
						size="sm"
						class="ml-auto border-red-300 text-red-700 hover:bg-red-100"
					>
						Try Again
					</Button>
				</div>
			</div>
		</div>
	{/if}

	<!-- Stats Overview -->
	<div class="mx-auto w-full max-w-7xl px-4 py-6 sm:px-6 sm:py-8 lg:px-8">
		<div class="mb-6 grid gap-4 sm:mb-8 sm:gap-6 md:grid-cols-2 lg:grid-cols-4">
			<Card class="border-0 bg-gradient-to-br from-blue-500 to-blue-600 text-white">
				<CardContent class="p-6">
					<div class="flex items-center gap-4">
						<div class="flex h-12 w-12 items-center justify-center rounded-lg bg-white/20">
							<Bookmark class="h-6 w-6 text-white" />
						</div>
						<div>
							<p class="text-sm text-blue-100">Active Reservations</p>
							<p class="text-2xl font-bold">
								{reservations.filter((r) => r.status === 'active').length}
							</p>
						</div>
					</div>
				</CardContent>
			</Card>

			<Card class="border-0 bg-gradient-to-br from-orange-500 to-orange-600 text-white">
				<CardContent class="p-6">
					<div class="flex items-center gap-4">
						<div class="flex h-12 w-12 items-center justify-center rounded-lg bg-white/20">
							<BookOpen class="h-6 w-6 text-white" />
						</div>
						<div>
							<p class="text-sm text-orange-100">Currently Borrowed</p>
							<p class="text-2xl font-bold">
								{borrowings.filter((b) => b.status === 'borrowed').length}
							</p>
						</div>
					</div>
				</CardContent>
			</Card>

			<Card class="border-0 bg-gradient-to-br from-green-500 to-green-600 text-white">
				<CardContent class="p-6">
					<div class="flex items-center gap-4">
						<div class="flex h-12 w-12 items-center justify-center rounded-lg bg-white/20">
							<CheckCircle class="h-6 w-6 text-white" />
						</div>
						<div>
							<p class="text-sm text-green-100">Books Returned</p>
							<p class="text-2xl font-bold">
								{borrowings.filter((b) => b.status === 'returned').length}
							</p>
						</div>
					</div>
				</CardContent>
			</Card>

			<Card class="border-0 bg-gradient-to-br from-purple-500 to-purple-600 text-white">
				<CardContent class="p-6">
					<div class="flex items-center gap-4">
						<div class="flex h-12 w-12 items-center justify-center rounded-lg bg-white/20">
							<TrendingUp class="h-6 w-6 text-white" />
						</div>
						<div>
							<p class="text-sm text-purple-100">Total Activity</p>
							<p class="text-2xl font-bold">{reservations.length + borrowings.length}</p>
						</div>
					</div>
				</CardContent>
			</Card>
		</div>

		<!-- Main Content Tabs -->
		<Card class="border-0 bg-white/80 shadow-lg backdrop-blur-sm">
			<CardHeader class="pb-4">
				<Tabs bind:value={activeTab} class="w-full">
					<TabsList class="grid w-full grid-cols-2">
						<TabsTrigger value="reservations" class="flex items-center gap-2">
							<Bookmark class="h-4 w-4" />
							Reservations ({reservations.length})
						</TabsTrigger>
						<TabsTrigger value="borrowings" class="flex items-center gap-2">
							<History class="h-4 w-4" />
							Borrowing History ({borrowings.length})
						</TabsTrigger>
					</TabsList>

					<TabsContent value="reservations" class="mt-6">
						{#if isLoading}
							<div class="py-16 text-center">
								<div
									class="mx-auto mb-6 flex h-20 w-20 items-center justify-center rounded-full bg-gradient-to-br from-blue-100 to-indigo-100"
								>
									<div class="h-12 w-12 animate-spin rounded-full border-b-2 border-blue-600"></div>
								</div>
								<h3 class="mb-2 text-lg font-semibold text-gray-900">
									Loading your reservations...
								</h3>
								<p class="text-gray-600">Please wait while we fetch your library data</p>
							</div>
						{:else if reservations.length === 0}
							<div class="py-16 text-center">
								<div
									class="mx-auto mb-6 flex h-20 w-20 items-center justify-center rounded-full bg-gradient-to-br from-blue-100 to-indigo-100"
								>
									<Bookmark class="h-10 w-10 text-blue-500" />
								</div>
								<h3 class="mb-3 text-xl font-semibold text-gray-900">No reservations yet</h3>
								<p class="mx-auto mb-6 max-w-md text-gray-600">
									Start exploring our library to find books you'd like to reserve. When you find a
									book that's currently borrowed, you can reserve it to be notified when it becomes
									available.
								</p>
								<div class="flex flex-col justify-center gap-3 sm:flex-row">
									<Button
										onclick={() => goto('/library/books')}
										class="bg-gradient-to-r from-blue-600 to-indigo-600 px-6 py-3 hover:from-blue-700 hover:to-indigo-700"
									>
										📚 Explore Books
									</Button>
									<Button onclick={() => goto('/library')} variant="outline" class="px-6 py-3">
										🏠 Library Home
									</Button>
								</div>
							</div>
						{:else}
							<div class="space-y-4">
								{#each reservations as reservation}
									<Card
										class="group border-0 bg-white/80 backdrop-blur-sm transition-all duration-300 hover:bg-white/90 hover:shadow-xl"
									>
										<CardContent class="p-6">
											<div class="flex gap-6">
												<div
													class="flex h-24 w-20 flex-shrink-0 items-center justify-center rounded-lg bg-gradient-to-br from-blue-100 to-indigo-100 transition-shadow group-hover:shadow-lg"
												>
													{#if reservation.book_image_url}
														<img
															src={reservation.book_image_url}
															alt={reservation.book_title}
															class="h-full w-full rounded-lg object-cover"
														/>
													{:else}
														<BookOpen class="h-8 w-8 text-blue-400" />
													{/if}
												</div>

												<div class="min-w-0 flex-1">
													<div class="mb-3 flex items-start justify-between">
														<div>
															<CardTitle class="mb-2 text-xl font-semibold text-gray-900">
																{reservation.book_title}
															</CardTitle>
															<CardDescription class="text-gray-600">
																<div class="flex items-center gap-4 text-sm">
																	<span class="flex items-center gap-1">
																		<User class="h-4 w-4" />
																		{reservation.book_author}
																	</span>
																	<span class="flex items-center gap-1">
																		<BookOpen class="h-4 w-4" />
																		{reservation.book_isbn}
																	</span>
																</div>
															</CardDescription>
														</div>

														<div class="flex flex-col items-end gap-2">
															<div
																class={`inline-flex items-center gap-1 rounded-full border px-2 py-1 text-xs font-medium ${getStatusColor(reservation.status)}`}
															>
																{getStatusIcon(reservation.status)}
																{reservation.status}
															</div>
															{#if reservation.status === 'active'}
																<div class="text-xs text-gray-500">
																	Expires in {getDaysRemaining(reservation.expiry_date)} days
																</div>
															{/if}
														</div>
													</div>

													<div class="grid gap-4 text-sm md:grid-cols-2">
														<div class="flex items-center gap-2">
															<Calendar class="h-4 w-4 text-gray-400" />
															<span class="text-gray-600">Reserved:</span>
															<span class="font-medium"
																>{formatDate(reservation.reservation_date)}</span
															>
														</div>

														<div class="flex items-center gap-2">
															<Clock class="h-4 w-4 text-gray-400" />
															<span class="text-gray-600">Expires:</span>
															<span class="font-medium">{formatDate(reservation.expiry_date)}</span>
														</div>
													</div>

													{#if reservation.status === 'active'}
														<div class="mt-4 rounded-lg border border-blue-200 bg-blue-50 p-3">
															<div class="flex items-center gap-2 text-sm text-blue-800">
																<AlertCircle class="h-4 w-4" />
																<span class="font-medium">Active Reservation</span>
															</div>
															<p class="mt-1 text-sm text-blue-700">
																You'll be notified when a copy becomes available. This reservation
																expires in {getDaysRemaining(reservation.expiry_date)} days.
															</p>
															<div class="mt-3">
																<Button
																	onclick={() => cancelReservation(reservation.book_id)}
																	variant="outline"
																	class="transform rounded-lg border-red-300 bg-white px-4 py-2 text-sm font-medium text-red-700 shadow-sm transition-all duration-200 hover:border-red-400 hover:bg-red-50 hover:shadow-md"
																>
																	<X class="mr-2 h-4 w-4" />
																	Cancel Reservation
																</Button>
															</div>
														</div>
													{/if}
												</div>
											</div>
										</CardContent>
									</Card>
								{/each}
							</div>
						{/if}
					</TabsContent>

					<TabsContent value="borrowings" class="mt-6">
						{#if isLoading}
							<div class="py-16 text-center">
								<div
									class="mx-auto mb-6 flex h-20 w-20 items-center justify-center rounded-full bg-gradient-to-br from-orange-100 to-red-100"
								>
									<div
										class="h-12 w-12 animate-spin rounded-full border-b-2 border-orange-600"
									></div>
								</div>
								<h3 class="mb-2 text-lg font-semibold text-gray-900">
									Loading your borrowing history...
								</h3>
								<p class="text-gray-600">Please wait while we fetch your library data</p>
							</div>
						{:else if borrowings.length === 0}
							<div class="py-16 text-center">
								<div
									class="mx-auto mb-6 flex h-20 w-20 items-center justify-center rounded-full bg-gradient-to-br from-orange-100 to-red-100"
								>
									<History class="h-10 w-10 text-orange-500" />
								</div>
								<h3 class="mb-3 text-xl font-semibold text-gray-900">No borrowing history yet</h3>
								<p class="mx-auto mb-6 max-w-md text-gray-600">
									Start borrowing books to build your reading history. Track your borrowed books,
									return them on time, and write reviews to help other students.
								</p>
								<div class="flex flex-col justify-center gap-3 sm:flex-row">
									<Button
										onclick={() => goto('/library/books')}
										class="bg-gradient-to-r from-orange-600 to-red-600 px-6 py-3 hover:from-orange-700 hover:to-red-700"
									>
										📚 Explore Books
									</Button>
									<Button onclick={() => goto('/library')} variant="outline" class="px-6 py-3">
										🏠 Library Home
									</Button>
								</div>
							</div>
						{:else}
							<div class="space-y-4">
								{#each borrowings as borrowing}
									<Card
										class="group border-0 bg-white/80 backdrop-blur-sm transition-all duration-300 hover:bg-white/90 hover:shadow-xl"
									>
										<CardContent class="p-6">
											<div class="flex gap-6">
												<div
													class="flex h-24 w-20 flex-shrink-0 items-center justify-center rounded-lg bg-gradient-to-br from-orange-100 to-red-100 transition-shadow group-hover:shadow-lg"
												>
													{#if borrowing.book_image_url}
														<img
															src={borrowing.book_image_url}
															alt={borrowing.book_title}
															class="h-full w-full rounded-lg object-cover"
														/>
													{:else}
														<BookOpen class="h-8 w-8 text-orange-400" />
													{/if}
												</div>

												<div class="min-w-0 flex-1">
													<div class="mb-3 flex items-start justify-between">
														<div>
															<CardTitle class="mb-2 text-xl font-semibold text-gray-900">
																{borrowing.book_title}
															</CardTitle>
															<CardDescription class="text-gray-600">
																<div class="flex items-center gap-4 text-sm">
																	<span class="flex items-center gap-1">
																		<User class="h-4 w-4" />
																		{borrowing.book_author}
																	</span>
																	<span class="flex items-center gap-1">
																		<BookOpen class="h-4 w-4" />
																		{borrowing.book_isbn}
																	</span>
																</div>
															</CardDescription>
														</div>

														<div class="flex flex-col items-end gap-2">
															<div
																class={`inline-flex items-center gap-1 rounded-full border px-2 py-1 text-xs font-medium ${getStatusColor(borrowing.status)}`}
															>
																{getStatusIcon(borrowing.status)}
																{borrowing.status}
															</div>
															{#if borrowing.status === 'overdue'}
																<div class="text-xs font-medium text-red-600">
																	{getDaysOverdue(borrowing.due_date)} days overdue
																</div>
															{/if}
														</div>
													</div>

													<div class="grid gap-4 text-sm md:grid-cols-3">
														<div class="flex items-center gap-2">
															<Calendar class="h-4 w-4 text-gray-400" />
															<span class="text-gray-600">Borrowed:</span>
															<span class="font-medium">{formatDate(borrowing.borrow_date)}</span>
														</div>

														<div class="flex items-center gap-2">
															<Clock class="h-4 w-4 text-gray-400" />
															<span class="text-gray-600">Due:</span>
															<span class="font-medium">{formatDate(borrowing.due_date)}</span>
														</div>

														{#if borrowing.return_date}
															<div class="flex items-center gap-2">
																<CheckCircle class="h-4 w-4 text-gray-400" />
																<span class="text-gray-600">Returned:</span>
																<span class="font-medium">{formatDate(borrowing.return_date)}</span>
															</div>
														{/if}
													</div>

													{#if borrowing.status === 'borrowed'}
														<div class="mt-4 rounded-lg border border-orange-200 bg-orange-50 p-3">
															<div class="flex items-center gap-2 text-sm text-orange-800">
																<BookOpen class="h-4 w-4" />
																<span class="font-medium">Currently Borrowed</span>
															</div>
															<p class="mt-1 text-sm text-orange-700">
																This book is due on {formatDate(borrowing.due_date)}. Please return
																it on time to avoid overdue fees.
															</p>
															<div class="mt-3 flex gap-3">
																<Button
																	onclick={() => returnBook(borrowing.id)}
																	class="transform rounded-lg bg-gradient-to-r from-green-600 to-emerald-600 px-4 py-2 text-sm font-medium text-white shadow-md transition-all duration-200 hover:-translate-y-0.5 hover:from-green-700 hover:to-emerald-700 hover:shadow-lg"
																>
																	<CheckCircle class="mr-2 h-4 w-4" />
																	Return Book Now
																</Button>
																<Button
																	onclick={() => goto(`/library/books/review/${borrowing.book_id}`)}
																	variant="outline"
																	class="rounded-lg border-blue-300 px-4 py-2 text-sm font-medium text-blue-700 shadow-sm transition-all duration-200 hover:border-blue-400 hover:bg-blue-50 hover:shadow-md"
																>
																	<Star class="mr-2 h-4 w-4" />
																	Write Review
																</Button>
															</div>
														</div>
													{:else if borrowing.status === 'overdue'}
														<div class="mt-4 rounded-lg border border-red-200 bg-red-50 p-3">
															<div class="flex items-center gap-2 text-sm text-red-800">
																<AlertCircle class="h-4 w-4" />
																<span class="font-medium">Overdue</span>
															</div>
															<p class="mt-1 text-sm text-red-700">
																This book is {getDaysOverdue(borrowing.due_date)} days overdue. Please
																return it as soon as possible.
															</p>
															<div class="mt-3 flex gap-3">
																<Button
																	onclick={() => returnBook(borrowing.id)}
																	class="transform rounded-lg bg-gradient-to-r from-red-600 to-rose-600 px-4 py-2 text-sm font-medium text-white shadow-md transition-all duration-200 hover:-translate-y-0.5 hover:from-red-700 hover:to-rose-700 hover:shadow-lg"
																>
																	<CheckCircle class="mr-2 h-4 w-4" />
																	Return Book Now
																</Button>
																<Button
																	onclick={() => goto(`/library/books/review/${borrowing.book_id}`)}
																	variant="outline"
																	class="rounded-lg border-blue-300 px-4 py-2 text-sm font-medium text-blue-700 shadow-sm transition-all duration-200 hover:border-blue-400 hover:bg-blue-50 hover:shadow-md"
																>
																	<Star class="mr-2 h-4 w-4" />
																	Write Review
																</Button>
															</div>
														</div>
													{:else if borrowing.status === 'returned'}
														<div class="mt-4 rounded-lg border border-green-200 bg-green-50 p-3">
															<div class="flex items-center gap-2 text-sm text-green-800">
																<CheckCircle class="h-4 w-4" />
																<span class="font-medium">Returned</span>
															</div>
															<p class="mt-1 text-sm text-green-700">
																Thank you for returning this book on {formatDate(
																	borrowing.return_date
																)}.
															</p>
															<div class="mt-3">
																<Button
																	onclick={() => goto(`/library/books/review/${borrowing.book_id}`)}
																	variant="outline"
																	class="rounded-lg border-blue-300 px-4 py-2 text-sm font-medium text-blue-700 shadow-sm transition-all duration-200 hover:border-blue-400 hover:bg-blue-50 hover:shadow-md"
																>
																	<Star class="mr-2 h-4 w-4" />
																	Write Review
																</Button>
															</div>
														</div>
													{/if}
												</div>
											</div>
										</CardContent>
									</Card>
								{/each}
							</div>
						{/if}
					</TabsContent>
				</Tabs>
			</CardHeader>
		</Card>
	</div>

	<!-- Quick Actions -->
	<div class="mx-auto max-w-7xl px-6 py-16">
		<div
			class="relative overflow-hidden rounded-3xl bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 p-8 text-center text-white md:p-12"
		>
			<!-- Background Pattern -->
			<div class="absolute inset-0 opacity-10">
				<div
					class="absolute top-0 left-0 h-32 w-32 -translate-x-16 -translate-y-16 rounded-full bg-white"
				></div>
				<div
					class="absolute right-0 bottom-0 h-24 w-24 translate-x-12 translate-y-12 rounded-full bg-white"
				></div>
				<div class="absolute top-1/2 left-1/4 h-16 w-16 rounded-full bg-white opacity-50"></div>
			</div>

			<div class="relative z-10">
				<h2 class="mb-4 text-3xl font-bold">Ready for your next read?</h2>
				<p class="mx-auto mb-8 max-w-2xl text-xl text-indigo-100">
					Explore our collection and discover your next favorite book. Build your reading journey
					with our diverse library.
				</p>
				<div class="flex flex-col justify-center gap-4 sm:flex-row">
					<Button
						onclick={() => goto('/library/books')}
						class="transform bg-white px-8 py-4 text-lg font-semibold text-indigo-600 shadow-xl transition-all duration-300 hover:scale-105 hover:bg-indigo-50 hover:shadow-2xl"
					>
						📚 Explore Books
					</Button>
					<Button
						onclick={() => goto('/library')}
						variant="outline"
						class="transform border-white px-8 py-4 text-lg font-semibold text-white transition-all duration-300 hover:scale-105 hover:bg-white hover:text-indigo-600"
					>
						🏠 Library Home
					</Button>
				</div>
			</div>
		</div>
	</div>
</div>
