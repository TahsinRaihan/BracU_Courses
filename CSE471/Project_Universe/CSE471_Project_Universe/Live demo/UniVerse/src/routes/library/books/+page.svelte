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
	import { Input } from '$lib/components/ui/input';
	import { Label } from '$lib/components/ui/label';
	import { Separator } from '$lib/components/ui/separator';
	import { Tabs, TabsContent, TabsList, TabsTrigger } from '$lib/components/ui/tabs';
	import {
		Search,
		BookOpen,
		User,
		Calendar,
		MapPin,
		Star,
		Filter,
		Grid3X3,
		List,
		Eye,
		ArrowLeft,
		Home,
		RefreshCw
	} from '@lucide/svelte';
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();

	let books = $state<any[]>(data.books || []);
	let filteredBooks = $state<any[]>(data.books || []);
	let searchQuery = $state('');
	let viewMode = $state<'grid' | 'list'>('grid');
	let selectedBook = $state<any>(null);
	let showModal = $state(false);
	let isBorrowing = $state(false);
	let isReserving = $state(false);
	let canReserveBook = $state(false);
	let isRefreshing = $state(false);

	onMount(() => {
		// Books are already loaded from server-side data
		console.log(`✅ Frontend: Loaded ${books.length} books from server`);
		// Apply filtering immediately after loading
		filterBooks();

		// Add visibility change listener to refresh data when page becomes visible
		const handleVisibilityChange = () => {
			if (!document.hidden) {
				console.log('🔄 Page became visible, refreshing books...');
				refreshBooks().catch(console.error);
			}
		};

		document.addEventListener('visibilitychange', handleVisibilityChange);

		// Cleanup listener on component destroy
		return () => {
			document.removeEventListener('visibilitychange', handleVisibilityChange);
		};
	});

	async function refreshBooks() {
		isRefreshing = true;
		try {
			console.log('🔄 Refreshing books from server...');
			const response = await fetch('/api/books?t=' + Date.now());
			if (response.ok) {
				const result = await response.json();
				// The API returns the books array directly, not wrapped in success/data
				books = result;
				filterBooks();
				console.log(`✅ Refreshed: ${books.length} books from server`);
			}
		} catch (error) {
			console.error('Error refreshing books:', error);
		} finally {
			isRefreshing = false;
		}
	}

	function filterBooks() {
		// First filter out books with no meaningful copies
		const booksWithMeaningfulCopies = books.filter((book) => {
			const availableCopies = book.availableCopies || 0;
			const borrowedCopies = book.borrowedCopies || 0;
			const reservedCopies = book.reservedCopies || 0;
			return availableCopies > 0 || borrowedCopies > 0 || reservedCopies > 0;
		});

		if (!searchQuery.trim()) {
			filteredBooks = booksWithMeaningfulCopies;
			return;
		}

		const query = searchQuery.toLowerCase().trim();
		filteredBooks = booksWithMeaningfulCopies.filter((book) => {
			return (
				book.title.toLowerCase().includes(query) ||
				book.author.toLowerCase().includes(query) ||
				book.isbn.includes(query)
			);
		});
	}

	function handleSearch() {
		filterBooks();
	}

	function handleClearSearch() {
		searchQuery = '';
		filteredBooks = [...books];
	}

	async function showBookDetails(book: any) {
		selectedBook = book;
		showModal = true;
		await checkBookReservationStatus(book.id);
	}

	async function checkBookReservationStatus(bookId: string) {
		try {
			const response = await fetch(`/api/books/can-reserve/${bookId}`);
			if (response.ok) {
				const data = await response.json();
				canReserveBook = data.can_reserve;
			}
		} catch (error) {
			console.error('Error checking reservation status:', error);
		}
	}

	async function handleBorrow() {
		if (!selectedBook) return;

		isBorrowing = true;
		try {
			const response = await fetch('/api/books/borrow', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ bookId: selectedBook.id })
			});

			const result = await response.json();

			if (response.ok && result.success) {
				alert(`Book borrowed successfully! Due date: ${result.dueDate || 'N/A'}`);
				showModal = false;
				// Update the book's available copies count locally
				if (selectedBook && selectedBook.availableCopies > 0) {
					selectedBook.availableCopies -= 1;
					selectedBook.borrowedCopies = (selectedBook.borrowedCopies || 0) + 1;
				}
				// Refresh the filtered books to reflect changes
				filteredBooks = [...filteredBooks];
			} else {
				alert(`Error: ${result.error || 'Failed to borrow book'}`);
			}
		} catch (error) {
			console.error('Borrow error:', error);
			alert('Error borrowing book. Please try again.');
		} finally {
			isBorrowing = false;
		}
	}

	async function handleReserve() {
		if (!selectedBook) return;

		isReserving = true;
		try {
			const response = await fetch('/api/books/reserve', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ bookId: selectedBook.id })
			});

			const result = await response.json();

			if (response.ok && result.success) {
				const estimatedDate = result.estimatedAvailability
					? new Date(result.estimatedAvailability).toLocaleDateString()
					: 'Unknown';
				alert(`Book reserved successfully! Estimated availability: ${estimatedDate}`);
				showModal = false;
				// Update the book's reserved copies count locally
				if (selectedBook) {
					selectedBook.reservedCopies = (selectedBook.reservedCopies || 0) + 1;
				}
				// Refresh the filtered books to reflect changes
				filteredBooks = [...filteredBooks];
			} else {
				alert(`Error: ${result.error || 'Failed to reserve book'}`);
			}
		} catch (error) {
			console.error('Reservation error:', error);
			alert('Error reserving book. Please try again.');
		} finally {
			isReserving = false;
		}
	}

	// Filter books when search query changes
	$effect(() => {
		if (searchQuery.trim()) {
			filterBooks();
		} else {
			filteredBooks = [...books];
		}
	});
</script>

<svelte:head>
	<title>Explore Books - UniVerse Library</title>
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
				<div class="text-sm text-gray-500">Explore Books</div>
			</div>
		</div>
	</div>

	<!-- Header Section -->
	<div class="border-b bg-white shadow-sm">
		<div class="mx-auto w-full max-w-7xl px-4 py-6 sm:px-6 sm:py-8 lg:px-8">
			<div class="flex flex-col gap-4 sm:gap-6 lg:flex-row lg:items-center lg:justify-between">
				<div>
					<h1 class="text-2xl font-bold text-gray-900 sm:text-3xl lg:text-4xl">
						Explore Our Collection
					</h1>
					<p class="mt-2 text-base text-gray-600 sm:text-lg">
						Discover thousands of books across all subjects and disciplines
					</p>
				</div>
				<div class="flex flex-col items-start gap-3 sm:flex-row sm:items-center">
					<button
						onclick={() => goto('/library')}
						class="rounded-md border border-gray-300 bg-white px-6 py-3 text-gray-700 transition-colors hover:bg-gray-50"
					>
						🏠 Back to Library
					</button>
					<button
						onclick={() => goto('/library/my-account')}
						class="rounded-md border border-gray-300 bg-white px-6 py-3 text-gray-700 transition-colors hover:bg-gray-50"
					>
						📋 My Library History
					</button>
					<div class="rounded-lg border border-blue-200 bg-blue-50 px-3 py-1">
						<span class="text-sm font-medium text-blue-700">
							{filteredBooks.length} books found
						</span>
					</div>
				</div>
			</div>
		</div>
	</div>

	<!-- Search and Filter Section -->
	<div class="mx-auto w-full max-w-7xl px-4 py-6 sm:px-6 sm:py-8 lg:px-8">
		<div class="mb-6 rounded-2xl bg-white p-4 shadow-lg sm:mb-8 sm:p-6">
			<div class="grid gap-4 sm:gap-6 md:grid-cols-1 lg:grid-cols-2">
				<!-- Search Input -->
				<div>
					<Label for="search" class="mb-2 block text-sm font-medium text-gray-700">
						Search Books
					</Label>
					<div class="relative">
						<Search
							class="absolute top-1/2 left-3 h-5 w-5 -translate-y-1/2 transform text-gray-400"
						/>
						<input
							id="search"
							bind:value={searchQuery}
							placeholder="Search by title, author, or ISBN..."
							class="w-full rounded-md border border-gray-300 py-3 pr-24 pl-10 focus:border-blue-500 focus:ring-2 focus:ring-blue-500 focus:outline-none"
							onkeydown={(e: KeyboardEvent) => e.key === 'Enter' && handleSearch()}
						/>
						<button
							onclick={handleSearch}
							class="absolute top-1/2 right-3 h-8 -translate-y-1/2 transform rounded-md border-0 bg-blue-600 px-3 text-white transition-colors hover:bg-blue-700"
							aria-label="Search books"
						>
							<Search class="h-4 w-4" />
						</button>
						<button
							onclick={handleClearSearch}
							class="absolute top-1/2 right-16 h-8 -translate-y-1/2 transform rounded-md border-0 bg-gray-500 px-3 text-white transition-colors hover:bg-gray-600"
							aria-label="Clear search"
						>
							<svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="2"
									d="M6 18L18 6M6 6l12 12"
								></path>
							</svg>
						</button>
						<button
							onclick={refreshBooks}
							disabled={isRefreshing}
							class="absolute top-1/2 right-28 h-8 -translate-y-1/2 transform rounded-md border-0 bg-green-600 px-3 text-white transition-colors hover:bg-green-700 disabled:opacity-50"
							aria-label="Refresh books"
						>
							<RefreshCw class="h-4 w-4 {isRefreshing ? 'animate-spin' : ''}" />
						</button>
					</div>
				</div>

				<!-- View Mode Toggle -->
				<div>
					<Label class="mb-2 block text-sm font-medium text-gray-700">View Mode</Label>
					<div class="flex overflow-hidden rounded-md border border-gray-300">
						<button
							onclick={() => (viewMode = 'grid')}
							class="flex-1 px-3 py-3 text-sm font-medium transition-colors {viewMode === 'grid'
								? 'bg-blue-600 text-white'
								: 'bg-white text-gray-700 hover:bg-gray-50'}"
						>
							<Grid3X3 class="mx-auto h-4 w-4" />
						</button>
						<button
							onclick={() => (viewMode = 'list')}
							class="flex-1 px-3 py-3 text-sm font-medium transition-colors {viewMode === 'list'
								? 'bg-blue-600 text-white'
								: 'bg-white text-gray-700 hover:bg-gray-50'}"
						>
							<List class="mx-auto h-4 w-4" />
						</button>
					</div>
				</div>
			</div>
		</div>

		<!-- Books Grid/List -->
		{#if viewMode === 'grid'}
			<div class="grid gap-4 sm:gap-6 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
				{#each filteredBooks as book}
					<Card
						class="group transform overflow-hidden border-0 bg-white/80 backdrop-blur-sm transition-all duration-300 hover:-translate-y-2 hover:shadow-2xl"
					>
						<div
							class="relative flex aspect-[3/4] items-center justify-center overflow-hidden bg-gradient-to-br from-blue-100 to-indigo-100"
						>
							{#if book.image_url}
								<img src={book.image_url} alt={book.title} class="h-full w-full object-cover" />
							{:else}
								<div class="p-6 text-center">
									<BookOpen class="mx-auto mb-4 h-16 w-16 text-blue-400" />
									<p class="text-sm text-gray-500">No image available</p>
								</div>
							{/if}
							<div
								class="absolute inset-0 bg-black/0 transition-all duration-300 group-hover:bg-black/20"
							></div>
						</div>

						<CardContent class="p-4 sm:p-6">
							<div class="mb-3 flex items-start justify-between">
								<div
									class="inline-flex items-center rounded-full bg-gray-100 px-2 py-1 text-xs font-medium text-gray-800"
								>
									{book.category}
								</div>
								<div class="flex items-center gap-1 text-yellow-500">
									<Star class="h-4 w-4 fill-current" />
									<span class="text-sm font-medium">4.5</span>
								</div>
							</div>

							<CardTitle
								class="mb-2 line-clamp-2 text-lg font-semibold text-gray-900 transition-colors group-hover:text-blue-600"
							>
								{book.title}
							</CardTitle>

							<CardDescription class="mb-4 text-gray-600">
								<div class="mb-2 flex items-center gap-2">
									<User class="h-4 w-4" />
									<span class="text-sm">{book.author}</span>
								</div>
								<div class="mb-2 flex items-center gap-2">
									<BookOpen class="h-4 w-4" />
									<span class="text-sm">ISBN: {book.isbn}</span>
								</div>
								<div class="flex items-center gap-2">
									<MapPin class="h-4 w-4" />
									<span class="text-sm">{book.location}</span>
								</div>
							</CardDescription>

							<!-- Availability Status -->
							<div class="mb-4">
								{#if (book.availableCopies || 0) > 0}
									<div class="flex items-center gap-2 text-green-600">
										<div class="h-2 w-2 rounded-full bg-green-500"></div>
										<span class="text-sm font-medium">✅ Available to Borrow</span>
									</div>
								{:else}
									<div class="flex items-center gap-2 text-blue-600">
										<div class="h-2 w-2 rounded-full bg-blue-500"></div>
										<span class="text-sm font-medium">📋 Available to Reserve</span>
									</div>
								{/if}
							</div>

							<button
								onclick={() => showBookDetails(book)}
								class="flex w-full items-center justify-center gap-2 rounded-md border-0 bg-gradient-to-r from-blue-600 to-purple-600 px-4 py-2 text-white transition-all duration-300 group-hover:shadow-lg hover:from-blue-700 hover:to-purple-700"
							>
								<Eye class="h-4 w-4" />
								View Details
							</button>
						</CardContent>
					</Card>
				{/each}
			</div>
		{:else}
			<!-- List View -->
			<div class="space-y-4">
				{#each filteredBooks as book}
					<Card
						class="border-0 bg-white/80 backdrop-blur-sm transition-all duration-300 hover:shadow-lg"
					>
						<CardContent class="p-4 sm:p-6">
							<div class="flex gap-4 sm:gap-6">
								<div
									class="flex h-32 w-24 flex-shrink-0 items-center justify-center rounded-lg bg-gradient-to-br from-blue-100 to-indigo-100"
								>
									{#if book.image_url}
										<img
											src={book.image_url}
											alt={book.title}
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
												{book.title}
											</CardTitle>
											<CardDescription class="text-gray-600">
												<div class="flex items-center gap-4 text-sm">
													<span class="flex items-center gap-1">
														<User class="h-4 w-4" />
														{book.author}
													</span>
													<span class="flex items-center gap-1">
														<BookOpen class="h-4 w-4" />
														{book.isbn}
													</span>
													<span class="flex items-center gap-1">
														<MapPin class="h-4 w-4" />
														{book.location}
													</span>
												</div>
											</CardDescription>
										</div>

										<div class="flex flex-col items-end gap-2">
											<div
												class="inline-flex items-center rounded-full bg-gray-100 px-2 py-1 text-xs font-medium text-gray-800"
											>
												{book.category}
											</div>
											<div class="flex items-center gap-1 text-yellow-500">
												<Star class="h-4 w-4 fill-current" />
												<span class="text-sm font-medium">4.5</span>
											</div>
										</div>
									</div>

									<!-- Availability Status -->
									<div class="mb-4">
										{#if (book.availableCopies || 0) > 0}
											<div class="flex items-center gap-2 text-green-600">
												<div class="h-2 w-2 rounded-full bg-green-500"></div>
												<span class="text-sm font-medium">✅ Available to Borrow</span>
											</div>
										{:else}
											<div class="flex items-center gap-2 text-blue-600">
												<div class="h-2 w-2 rounded-full bg-blue-500"></div>
												<span class="text-sm font-medium">📋 Available to Reserve</span>
											</div>
										{/if}
									</div>

									<button
										onclick={() => showBookDetails(book)}
										class="flex items-center gap-2 rounded-md border-0 bg-gradient-to-r from-blue-600 to-purple-600 px-4 py-2 text-white transition-all duration-300 hover:from-blue-700 hover:to-purple-700"
									>
										<Eye class="h-4 w-4" />
										View Details
									</button>
								</div>
							</div>
						</CardContent>
					</Card>
				{/each}
			</div>
		{/if}

		<!-- No Results -->
		{#if filteredBooks.length === 0}
			<div class="py-16 text-center">
				<BookOpen class="mx-auto mb-4 h-16 w-16 text-gray-400" />
				<h3 class="mb-2 text-lg font-medium text-gray-900">No books found</h3>
				<p class="text-gray-600">Try adjusting your search or filter criteria.</p>
			</div>
		{/if}
	</div>

	<!-- Book Details Modal -->
	{#if showModal && selectedBook}
		<div class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
			<div class="max-h-[90vh] w-full max-w-2xl overflow-y-auto rounded-2xl bg-white">
				<div class="p-6">
					<div class="mb-6 flex items-start justify-between">
						<h2 class="text-2xl font-bold text-gray-900">{selectedBook.title}</h2>
						<button
							onclick={() => (showModal = false)}
							class="text-gray-400 transition-colors hover:text-gray-600"
							aria-label="Close modal"
						>
							<svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="2"
									d="M6 18L18 6M6 6l12 12"
								></path>
							</svg>
						</button>
					</div>

					<div class="mb-6 grid gap-6 md:grid-cols-2">
						<div
							class="flex aspect-[3/4] items-center justify-center overflow-hidden rounded-lg bg-gradient-to-br from-blue-100 to-indigo-100"
						>
							{#if selectedBook.image_url}
								<img
									src={selectedBook.image_url}
									alt={selectedBook.title}
									class="h-full w-full object-cover"
								/>
							{:else}
								<BookOpen class="h-16 w-16 text-blue-400" />
							{/if}
						</div>

						<div class="space-y-4">
							<div>
								<Label class="text-sm font-medium text-gray-700">Author</Label>
								<p class="text-gray-900">{selectedBook.author}</p>
							</div>

							<div>
								<Label class="text-sm font-medium text-gray-700">ISBN</Label>
								<p class="text-gray-900">{selectedBook.isbn}</p>
							</div>

							<div>
								<Label class="text-sm font-medium text-gray-700">Category</Label>
								<div
									class="inline-flex items-center rounded-full bg-gray-100 px-2 py-1 text-xs font-medium text-gray-800"
								>
									{selectedBook.category}
								</div>
							</div>

							<div>
								<Label class="text-sm font-medium text-gray-700">Location</Label>
								<p class="text-gray-900">{selectedBook.location}</p>
							</div>

							<div>
								<Label class="text-sm font-medium text-gray-700">Published Year</Label>
								<p class="text-gray-900">{selectedBook.published_year || 'N/A'}</p>
							</div>
						</div>
					</div>

					<Separator class="my-6" />

					<!-- Availability Section -->
					<div class="mb-6">
						<h3 class="mb-4 text-lg font-semibold text-gray-900">Availability</h3>

						{#if (selectedBook.availableCopies || 0) > 0}
							<div class="mb-4 rounded-lg border border-green-200 bg-green-50 p-4">
								<div class="mb-2 flex items-center gap-2 text-green-800">
									<div class="h-2 w-2 rounded-full bg-green-500"></div>
									<span class="font-medium">Copies Available</span>
								</div>
								<p class="text-sm text-green-700">
									This book is currently available for borrowing. You can borrow it now and keep it
									for 14 days.
								</p>
							</div>

							<button
								onclick={handleBorrow}
								disabled={isBorrowing}
								class="w-full rounded-md border-0 bg-green-600 px-4 py-3 text-white transition-all duration-300 hover:bg-green-700 disabled:cursor-not-allowed disabled:opacity-50"
							>
								{isBorrowing ? 'Processing...' : 'Borrow Book'}
							</button>
						{:else}
							<div class="mb-4 rounded-lg border border-blue-200 bg-blue-50 p-4">
								<div class="mb-2 flex items-center gap-2 text-blue-800">
									<div class="h-2 w-2 rounded-full bg-blue-500"></div>
									<span class="font-medium">No Copies Available</span>
								</div>
								<p class="text-sm text-blue-700">
									All copies of this book are currently borrowed. You can reserve it and we'll
									notify you when it becomes available.
								</p>
							</div>

							<button
								onclick={handleReserve}
								disabled={isReserving}
								class="w-full rounded-md border-0 bg-blue-600 px-4 py-3 text-white transition-all duration-300 hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-50"
							>
								{isReserving ? 'Reserving...' : 'Reserve Book (No Copies Available)'}
							</button>
						{/if}
					</div>

					<!-- Action Instructions -->
					<div class="rounded-lg bg-gray-50 p-4">
						<h4 class="mb-2 font-medium text-gray-900">What happens next?</h4>
						<ul class="space-y-1 text-sm text-gray-600">
							{#if (selectedBook.availableCopies || 0) > 0}
								<li>• Book will be marked as borrowed in your account</li>
								<li>• Due date will be set to 14 days from today</li>
								<li>• You can return it anytime before the due date</li>
							{:else}
								<li>• Book will be added to your reservations</li>
								<li>• You'll be notified when a copy becomes available</li>
								<li>• Reservation expires in 7 days if not fulfilled</li>
							{/if}
						</ul>
					</div>
				</div>
			</div>
		</div>
	{/if}
</div>
