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
	import {
		BookOpen,
		Plus,
		Search,
		Filter,
		Settings,
		Users,
		BarChart3,
		TrendingUp,
		AlertCircle,
		CheckCircle,
		Clock,
		Edit,
		Edit3,
		Trash2,
		Eye,
		ArrowRight,
		Info
	} from '@lucide/svelte';

	let books: any[] = [];
	let filteredBooks: any[] = [];
	let reservedBooksWithoutCopies: any[] = [];
	let searchQuery = '';
	let isLoading = true;
	let selectedBook: any = null;
	let showBookModal = false;
	let bookReviews: any[] = [];
	let ratingSummary: any = null;
	let isLoadingReviews = false;
	let stats = {
		totalBooks: 0,
		totalCopies: 0,
		borrowedCopies: 0,
		availableCopies: 0,
		reservedCopies: 0,
		overdueCopies: 0
	};

	onMount(async () => {
		await loadLibraryData();
	});

	async function loadLibraryData() {
		try {
			// Load books
			const response = await fetch('/api/admin/books');
			if (response.ok) {
				const result = await response.json();
				console.log('Admin API response:', result);

				if (result.success && result.books) {
					books = result.books;
					reservedBooksWithoutCopies = result.reservedBooksWithoutCopies || [];
					// Apply filtering immediately after loading
					filterBooks();
					calculateStats();
				} else {
					console.error('API returned error:', result.error);
					books = [];
					filteredBooks = [];
					reservedBooksWithoutCopies = [];
				}
			} else {
				console.error('Failed to fetch books:', response.status);
				books = [];
				filteredBooks = [];
				reservedBooksWithoutCopies = [];
			}
		} catch (error) {
			console.error('Error loading library data:', error);
			books = [];
			filteredBooks = [];
			reservedBooksWithoutCopies = [];
		} finally {
			isLoading = false;
		}
	}

	function calculateStats() {
		// Calculate stats from filtered books (books with meaningful copies)
		stats.totalBooks = filteredBooks.length;
		stats.totalCopies = filteredBooks.reduce((sum, book) => sum + (book.totalCopies || 0), 0);
		stats.borrowedCopies = filteredBooks.reduce((sum, book) => sum + (book.borrowedCopies || 0), 0);
		stats.availableCopies = filteredBooks.reduce(
			(sum, book) => sum + (book.availableCopies || 0),
			0
		);
		stats.reservedCopies = filteredBooks.reduce((sum, book) => sum + (book.reservedCopies || 0), 0);
		stats.overdueCopies = filteredBooks.reduce((sum, book) => sum + (book.overdueCopies || 0), 0);
	}

	function filterBooks() {
		console.log('🔍 Filtering books...', { searchQuery, totalBooks: books.length });

		filteredBooks = books.filter((book) => {
			// Show books that have meaningful copies OR active reservations
			const availableCopies = book.availableCopies || 0;
			const borrowedCopies = book.borrowedCopies || 0;
			const reservedCopies = book.reservedCopies || 0;
			const activeReservations = book.activeReservations || 0;
			const hasMeaningfulCopies = availableCopies > 0 || borrowedCopies > 0 || reservedCopies > 0;
			const hasActiveReservations = activeReservations > 0;

			const matchesSearch =
				book.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
				book.author.toLowerCase().includes(searchQuery.toLowerCase()) ||
				book.isbn.includes(searchQuery);

			console.log(`📖 Book: ${book.title}`, {
				hasMeaningfulCopies,
				hasActiveReservations,
				activeReservations,
				availableCopies,
				borrowedCopies,
				reservedCopies,
				totalCopies: book.totalCopies,
				matchesSearch,
				searchQuery: searchQuery.toLowerCase(),
				title: book.title.toLowerCase(),
				author: book.author.toLowerCase(),
				isbn: book.isbn,
				willShow: (hasMeaningfulCopies || hasActiveReservations) && matchesSearch
			});

			return (hasMeaningfulCopies || hasActiveReservations) && matchesSearch;
		});

		console.log(
			`✅ Filtered results: ${filteredBooks.length} books (out of ${books.length} total)`
		);

		// Recalculate stats after filtering
		calculateStats();
	}

	function getStatusColor(status: string) {
		switch (status) {
			case 'available':
				return 'bg-green-100 text-green-800 border-green-200';
			case 'borrowed':
				return 'bg-orange-100 text-orange-800 border-orange-200';
			case 'reserved':
				return 'bg-blue-100 text-blue-800 border-blue-200';
			case 'overdue':
				return 'bg-red-100 text-red-800 border-red-200';
			default:
				return 'bg-gray-100 text-gray-800 border-gray-200';
		}
	}

	function clearSearch() {
		searchQuery = '';
		filterBooks();
	}

	async function showBookDetails(book: any) {
		selectedBook = book;
		showBookModal = true;
		await loadBookReviews(book.id);
	}

	function closeBookModal() {
		showBookModal = false;
		selectedBook = null;
		bookReviews = [];
		ratingSummary = null;
	}

	async function loadBookReviews(bookId: string) {
		isLoadingReviews = true;
		try {
			const response = await fetch(`/api/books/reviews/${bookId}`);
			if (response.ok) {
				const data = await response.json();
				if (data.success) {
					bookReviews = data.reviews || [];
					ratingSummary = data.ratingSummary;
				}
			}
		} catch (error) {
			console.error('Error loading book reviews:', error);
		} finally {
			isLoadingReviews = false;
		}
	}

	function getRatingStars(rating: number) {
		const stars = [];
		for (let i = 1; i <= 5; i++) {
			if (i <= rating) {
				stars.push('★');
			} else {
				stars.push('☆');
			}
		}
		return stars.join('');
	}

	function getRatingColor(rating: number) {
		if (rating >= 4) return 'text-green-600';
		if (rating >= 3) return 'text-yellow-600';
		return 'text-red-600';
	}

	function getRatingLabel(rating: number) {
		if (rating >= 4.5) return 'Excellent';
		if (rating >= 4) return 'Very Good';
		if (rating >= 3.5) return 'Good';
		if (rating >= 3) return 'Average';
		if (rating >= 2.5) return 'Below Average';
		return 'Poor';
	}
</script>

<svelte:head>
	<title>Library Management - Admin Dashboard</title>
</svelte:head>

<div class="min-h-screen bg-gradient-to-br from-gray-50 via-white to-blue-50">
	<!-- Header Section -->
	<div class="border-b bg-white shadow-sm">
		<div class="mx-auto max-w-7xl px-6 py-8">
			<div class="flex flex-col gap-6 lg:flex-row lg:items-center lg:justify-between">
				<div>
					<h1 class="text-3xl font-bold text-gray-900 sm:text-4xl">Library Management</h1>
					<p class="mt-2 text-lg text-gray-600">
						Manage books, monitor circulation, and oversee library operations
					</p>
				</div>

				<div class="flex items-center gap-3">
					<Button onclick={() => goto('/admin')} variant="outline" class="px-6 py-3">
						Return to Admin Dashboard
					</Button>
				</div>
			</div>
		</div>
	</div>

	<!-- Stats Overview -->
	<div class="mx-auto max-w-7xl px-6 py-8">
		<div class="mb-8 grid gap-6 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-7">
			<Card class="border-0 bg-gradient-to-br from-blue-500 to-blue-600 text-white">
				<CardContent class="p-6">
					<div class="flex items-center gap-4">
						<div class="flex h-12 w-12 items-center justify-center rounded-lg bg-white/20">
							<BookOpen class="h-6 w-6 text-white" />
						</div>
						<div>
							<p class="text-sm text-blue-100">Total Books</p>
							<p class="text-2xl font-bold">{stats.totalBooks}</p>
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
							<p class="text-sm text-green-100">Available</p>
							<p class="text-2xl font-bold">{stats.availableCopies}</p>
						</div>
					</div>
				</CardContent>
			</Card>

			<Card class="border-0 bg-gradient-to-br from-orange-500 to-orange-600 text-white">
				<CardContent class="p-6">
					<div class="flex items-center gap-4">
						<div class="flex h-12 w-12 items-center justify-center rounded-lg bg-white/20">
							<Users class="h-6 w-6 text-white" />
						</div>
						<div>
							<p class="text-sm text-orange-100">Borrowed</p>
							<p class="text-2xl font-bold">{stats.borrowedCopies}</p>
						</div>
					</div>
				</CardContent>
			</Card>

			<Card class="border-0 bg-gradient-to-br from-purple-500 to-purple-600 text-white">
				<CardContent class="p-6">
					<div class="flex items-center gap-4">
						<div class="flex h-12 w-12 items-center justify-center rounded-lg bg-white/20">
							<Clock class="h-6 w-6 text-white" />
						</div>
						<div>
							<p class="text-sm text-purple-100">Reserved</p>
							<p class="text-2xl font-bold">{stats.reservedCopies}</p>
						</div>
					</div>
				</CardContent>
			</Card>

			<Card class="border-0 bg-gradient-to-br from-red-500 to-red-600 text-white">
				<CardContent class="p-6">
					<div class="flex items-center gap-4">
						<div class="flex h-12 w-12 items-center justify-center rounded-lg bg-white/20">
							<AlertCircle class="h-6 w-6 text-white" />
						</div>
						<div>
							<p class="text-sm text-red-100">Overdue</p>
							<p class="text-2xl font-bold">{stats.overdueCopies}</p>
						</div>
					</div>
				</CardContent>
			</Card>

			<Card class="border-0 bg-gradient-to-br from-indigo-500 to-indigo-600 text-white">
				<CardContent class="p-6">
					<div class="flex items-center gap-4">
						<div class="flex h-12 w-12 items-center justify-center rounded-lg bg-white/20">
							<BarChart3 class="h-6 w-6 text-white" />
						</div>
						<div>
							<p class="text-sm text-indigo-100">Total Copies</p>
							<p class="text-2xl font-bold">{stats.totalCopies}</p>
						</div>
					</div>
				</CardContent>
			</Card>

			<Card class="border-0 bg-gradient-to-br from-amber-500 to-amber-600 text-white">
				<CardContent class="p-6">
					<div class="flex items-center gap-4">
						<div class="flex h-12 w-12 items-center justify-center rounded-lg bg-white/20">
							<AlertCircle class="h-6 w-6 text-white" />
						</div>
						<div>
							<p class="text-sm text-amber-100">Awaiting Copies</p>
							<p class="text-2xl font-bold">{reservedBooksWithoutCopies.length}</p>
						</div>
					</div>
				</CardContent>
			</Card>
		</div>

		<!-- Status Summary -->
		<div class="mb-8">
			<div class="rounded-2xl bg-white p-6 shadow-lg">
				<div class="mb-6 text-center">
					<h3 class="mb-2 text-lg font-semibold text-gray-900">Current Library Status</h3>
					<p class="text-gray-600">Overview of your library's current state and recommendations</p>
				</div>

				<div class="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
					<div class="rounded-lg border border-blue-200 bg-blue-50 p-4 text-center">
						<div class="mb-1 text-2xl font-bold text-blue-600">{stats.totalBooks}</div>
						<div class="text-sm text-blue-700">Total Books</div>
						<div class="mt-1 text-xs text-blue-600">
							{stats.totalBooks === 0 ? 'Start building your collection' : 'Books in library'}
						</div>
					</div>

					<div class="rounded-lg border border-green-200 bg-green-50 p-4 text-center">
						<div class="mb-1 text-2xl font-bold text-green-600">{stats.availableCopies}</div>
						<div class="text-sm text-green-700">Available Copies</div>
						<div class="mt-1 text-xs text-green-600">
							{stats.availableCopies === 0 ? 'All copies borrowed' : 'Ready for borrowing'}
						</div>
					</div>

					<div class="rounded-lg border border-orange-200 bg-orange-50 p-4 text-center">
						<div class="mb-1 text-2xl font-bold text-orange-600">{stats.borrowedCopies}</div>
						<div class="text-sm text-orange-700">Currently Borrowed</div>
						<div class="mt-1 text-xs text-orange-600">
							{stats.borrowedCopies === 0 ? 'No active loans' : 'Books out on loan'}
						</div>
					</div>

					<div class="rounded-lg border border-purple-200 bg-purple-50 p-4 text-center">
						<div class="mb-1 text-2xl font-bold text-purple-600">{stats.reservedCopies}</div>
						<div class="text-sm text-purple-700">Reserved</div>
						<div class="mt-1 text-xs text-purple-600">
							{stats.reservedCopies === 0 ? 'No pending reservations' : 'Students waiting'}
						</div>
					</div>
				</div>

				{#if stats.totalBooks === 0}
					<div class="mt-6 text-center">
						<div
							class="inline-flex items-center gap-2 rounded-lg border border-yellow-200 bg-yellow-50 px-4 py-2"
						>
							<AlertCircle class="h-4 w-4 text-yellow-600" />
							<span class="text-sm text-yellow-700"
								>Your library is empty. Start by adding your first book!</span
							>
						</div>
					</div>
				{:else if stats.availableCopies === 0}
					<div class="mt-6 text-center">
						<div
							class="inline-flex items-center gap-2 rounded-lg border border-blue-200 bg-blue-50 px-4 py-2"
						>
							<Info class="h-4 w-4 text-blue-600" />
							<span class="text-sm text-blue-700"
								>All books are currently borrowed. Consider adding more copies!</span
							>
						</div>
					</div>
				{/if}
			</div>
		</div>

		<!-- Search Section -->
		<div class="mb-8 rounded-2xl bg-white p-6 shadow-lg">
			<div class="flex items-end gap-4">
				<!-- Search Input -->
				<div class="flex-1">
					<Label for="search" class="mb-2 block text-sm font-medium text-gray-700">
						Search Books
					</Label>
					<Input
						id="search"
						bind:value={searchQuery}
						placeholder="Search by title, author, or ISBN..."
						class="w-full border-gray-300 px-4 py-3 focus:border-blue-500 focus:ring-blue-500"
					/>
				</div>

				<!-- Search Button -->
				<div class="flex gap-2">
					<Button onclick={filterBooks} class="px-6 py-3">Search</Button>
					<Button onclick={clearSearch} variant="outline" class="px-6 py-3">Clear</Button>
				</div>
			</div>
		</div>

		<!-- Books Management -->
		<Card class="border-0 bg-white/80 shadow-lg backdrop-blur-sm">
			<CardHeader>
				<div class="flex items-center justify-between">
					<div>
						<CardTitle class="text-2xl text-gray-900">Book Collection</CardTitle>
						<CardDescription>
							{filteredBooks.length} book{filteredBooks.length !== 1 ? 's' : ''} found
						</CardDescription>
					</div>
				</div>
			</CardHeader>

			<CardContent>
				{#if isLoading}
					<div class="py-12 text-center">
						<div
							class="mx-auto mb-4 h-12 w-12 animate-spin rounded-full border-b-2 border-blue-600"
						></div>
						<p class="text-gray-600">Loading library data...</p>
					</div>
				{:else if filteredBooks.length === 0}
					<div class="py-16 text-center">
						<BookOpen class="mx-auto mb-4 h-16 w-16 text-gray-400" />
						<h3 class="mb-2 text-lg font-medium text-gray-900">No books found</h3>
						<p class="mb-6 text-gray-600">
							Start building your library collection by adding the first book.
						</p>
						<Button onclick={() => goto('/admin/library/add')} class="px-6 py-3">
							Add First Book
						</Button>
					</div>
				{:else}
					<div class="overflow-x-auto">
						<table class="w-full">
							<thead>
								<tr class="border-b border-gray-200">
									<th class="px-4 py-3 text-left font-medium text-gray-900">Book</th>
									<th class="px-4 py-3 text-left font-medium text-gray-900">Category</th>
									<th class="px-4 py-3 text-left font-medium text-gray-900">Copies</th>
									<th class="px-4 py-3 text-left font-medium text-gray-900">Status</th>
									<th class="px-4 py-3 text-left font-medium text-gray-900">Actions</th>
								</tr>
							</thead>
							<tbody class="divide-y divide-gray-200">
								{#each filteredBooks as book}
									<tr class="transition-colors hover:bg-gray-50">
										<td class="px-4 py-4">
											<div class="flex items-center gap-4">
												<div
													class="flex h-20 w-16 flex-shrink-0 items-center justify-center rounded-lg bg-gradient-to-br from-blue-100 to-indigo-100"
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
												<div>
													<div class="font-medium text-gray-900">{book.title}</div>
													<div class="text-sm text-gray-600">by {book.author}</div>
													<div class="text-xs text-gray-500">ISBN: {book.isbn}</div>
												</div>
											</div>
										</td>

										<td class="px-4 py-4">
											<div
												class="inline-flex items-center rounded-full bg-gray-100 px-2.5 py-0.5 text-xs font-medium text-gray-800"
											>
												{book.category}
											</div>
										</td>

										<td class="px-4 py-4">
											<div class="space-y-1">
												<div class="flex items-center gap-2 text-sm">
													<div class="h-2 w-2 rounded-full bg-green-500"></div>
													<span>Available: {book.availableCopies || 0}</span>
												</div>
												<div class="flex items-center gap-2 text-sm">
													<div class="h-2 w-2 rounded-full bg-orange-500"></div>
													<span>Borrowed: {book.borrowedCopies || 0}</span>
												</div>
												<div class="flex items-center gap-2 text-sm">
													<div class="h-2 w-2 rounded-full bg-blue-500"></div>
													<span>Reserved: {book.reservedCopies || 0}</span>
												</div>
											</div>
										</td>

										<td class="px-4 py-4">
											{#if (book.availableCopies || 0) > 0}
												<div
													class="inline-flex items-center rounded-full border border-green-200 bg-green-100 px-2.5 py-0.5 text-xs font-medium text-green-800"
												>
													<CheckCircle class="mr-1 h-3 w-3" />
													Available
												</div>
											{:else if (book.borrowedCopies || 0) > 0}
												<div
													class="inline-flex items-center rounded-full border border-orange-200 bg-orange-100 px-2.5 py-0.5 text-xs font-medium text-orange-800"
												>
													<Users class="mr-1 h-3 w-3" />
													Borrowed
												</div>
											{:else}
												<div
													class="inline-flex items-center rounded-full border border-blue-200 bg-blue-100 px-2.5 py-0.5 text-xs font-medium text-blue-800"
												>
													<Clock class="mr-1 h-3 w-3" />
													Reserved
												</div>
											{/if}
										</td>

										<td class="px-4 py-4">
											<div class="flex items-center gap-2">
												<Button
													size="sm"
													variant="outline"
													onclick={() => goto(`/admin/library/edit/${book.id}`)}
												>
													<Edit class="h-3 w-3" />
												</Button>
												<Button
													size="sm"
													variant="outline"
													onclick={() => goto(`/admin/library/manage-copies/${book.id}`)}
												>
													<Settings class="h-3 w-3" />
												</Button>
												<Button size="sm" variant="outline" onclick={() => showBookDetails(book)}>
													<Eye class="h-3 w-3" />
												</Button>
											</div>
										</td>
									</tr>
								{/each}
							</tbody>
						</table>
					</div>
				{/if}
			</CardContent>
		</Card>

		<!-- Reserved Books Without Copies Table -->
		{#if reservedBooksWithoutCopies.length > 0}
			<Card class="mt-8 border-0 bg-white/80 shadow-lg backdrop-blur-sm">
				<CardHeader>
					<div class="flex items-center justify-between">
						<div>
							<CardTitle class="text-2xl text-gray-900"
								>Reserved Books (No Copies Available)</CardTitle
							>
							<CardDescription>
								Books that students have reserved but have no physical copies in the library
							</CardDescription>
						</div>
						<div class="flex items-center gap-2">
							<div class="rounded-full bg-orange-100 px-3 py-1">
								<span class="text-sm font-medium text-orange-800">
									{reservedBooksWithoutCopies.length} Reserved
								</span>
							</div>
						</div>
					</div>
				</CardHeader>

				<CardContent>
					<div class="overflow-x-auto">
						<table class="w-full">
							<thead>
								<tr class="border-b border-gray-200">
									<th class="px-4 py-3 text-left font-medium text-gray-900">Book</th>
									<th class="px-4 py-3 text-left font-medium text-gray-900">Category</th>
									<th class="px-4 py-3 text-left font-medium text-gray-900">Reservation Date</th>
									<th class="px-4 py-3 text-left font-medium text-gray-900">Status</th>
									<th class="px-4 py-3 text-left font-medium text-gray-900">Actions</th>
								</tr>
							</thead>
							<tbody class="divide-y divide-gray-200">
								{#each reservedBooksWithoutCopies as book}
									<tr class="transition-colors hover:bg-gray-50">
										<td class="px-4 py-4">
											<div class="flex items-center gap-4">
												<div
													class="flex h-20 w-16 flex-shrink-0 items-center justify-center rounded-lg bg-gradient-to-br from-orange-100 to-red-100"
												>
													{#if book.image_url}
														<img
															src={book.image_url}
															alt={book.title}
															class="h-full w-full rounded-lg object-cover"
														/>
													{:else}
														<BookOpen class="h-8 w-8 text-orange-400" />
													{/if}
												</div>
												<div>
													<div class="font-medium text-gray-900">{book.title}</div>
													<div class="text-sm text-gray-600">by {book.author}</div>
													<div class="text-xs text-gray-500">ISBN: {book.isbn}</div>
												</div>
											</div>
										</td>

										<td class="px-4 py-4">
											<div
												class="inline-flex items-center rounded-full bg-gray-100 px-2.5 py-0.5 text-xs font-medium text-gray-800"
											>
												{book.category}
											</div>
										</td>

										<td class="px-4 py-4">
											<div class="text-sm text-gray-600">
												{new Date(book.reservationDate).toLocaleDateString()}
											</div>
											<div class="text-xs text-gray-500">
												{new Date(book.reservationDate).toLocaleTimeString()}
											</div>
										</td>

										<td class="px-4 py-4">
											<div
												class="inline-flex items-center rounded-full border border-orange-200 bg-orange-100 px-2.5 py-0.5 text-xs font-medium text-orange-800"
											>
												<Clock class="mr-1 h-3 w-3" />
												Awaiting Copies
											</div>
										</td>

										<td class="px-4 py-4">
											<div class="flex items-center gap-2">
												<Button
													size="sm"
													variant="outline"
													onclick={() => goto(`/admin/library/manage-copies/${book.id}`)}
													class="text-green-600 hover:text-green-700"
												>
													<Plus class="h-3 w-3" />
													Add Copies
												</Button>
												<Button
													size="sm"
													variant="outline"
													onclick={() => goto(`/admin/library/edit/${book.id}`)}
												>
													<Edit class="h-3 w-3" />
												</Button>
												<Button size="sm" variant="outline" onclick={() => showBookDetails(book)}>
													<Eye class="h-3 w-3" />
												</Button>
											</div>
										</td>
									</tr>
								{/each}
							</tbody>
						</table>
					</div>
				</CardContent>
			</Card>
		{/if}

		<!-- Book Details Modal -->
		{#if showBookModal && selectedBook}
			<div
				class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4 backdrop-blur-sm"
			>
				<div
					class="max-h-[90vh] w-full max-w-2xl overflow-y-auto rounded-lg border border-gray-200 bg-white/95 shadow-2xl backdrop-blur-md"
				>
					<!-- Modal Header -->
					<div class="flex items-center justify-between border-b border-gray-200 p-6">
						<h2 class="text-2xl font-bold text-gray-900">Book Details</h2>
						<Button onclick={closeBookModal} variant="outline" size="sm">✕</Button>
					</div>

					<!-- Modal Content -->
					<div class="p-6">
						<div class="mb-6 flex gap-6">
							<!-- Book Cover -->
							<div
								class="flex h-40 w-32 flex-shrink-0 items-center justify-center rounded-lg bg-gradient-to-br from-blue-100 to-indigo-100"
							>
								{#if selectedBook.image_url}
									<img
										src={selectedBook.image_url}
										alt={selectedBook.title}
										class="h-full w-full rounded-lg object-cover"
									/>
								{:else}
									<BookOpen class="h-16 w-16 text-blue-400" />
								{/if}
							</div>

							<!-- Book Info -->
							<div class="flex-1">
								<h3 class="mb-2 text-2xl font-bold text-gray-900">{selectedBook.title}</h3>
								<p class="mb-3 text-lg text-gray-600">by {selectedBook.author}</p>

								<div class="grid grid-cols-2 gap-4 text-sm">
									<div>
										<span class="font-medium text-gray-700">ISBN:</span>
										<span class="ml-2 text-gray-600">{selectedBook.isbn}</span>
									</div>
									<div>
										<span class="font-medium text-gray-700">Category:</span>
										<span class="ml-2 text-gray-600">{selectedBook.category}</span>
									</div>
									<div>
										<span class="font-medium text-gray-700">Published Year:</span>
										<span class="ml-2 text-gray-600">{selectedBook.published_year || 'N/A'}</span>
									</div>
									<div>
										<span class="font-medium text-gray-700">Location:</span>
										<span class="ml-2 text-gray-600">{selectedBook.location || 'N/A'}</span>
									</div>
								</div>
							</div>
						</div>

						<!-- Copy Information -->
						<div class="border-t border-gray-200 pt-6">
							<h4 class="mb-4 text-lg font-semibold text-gray-900">Copy Information</h4>
							<div class="grid grid-cols-2 gap-4 md:grid-cols-4">
								<div class="rounded-lg bg-blue-50 p-4 text-center">
									<div class="text-2xl font-bold text-blue-600">
										{selectedBook.totalCopies || 0}
									</div>
									<div class="text-sm text-blue-600">Total Copies</div>
								</div>
								<div class="rounded-lg bg-green-50 p-4 text-center">
									<div class="text-2xl font-bold text-green-600">
										{selectedBook.availableCopies || 0}
									</div>
									<div class="text-sm text-green-600">Available</div>
								</div>
								<div class="rounded-lg bg-orange-50 p-4 text-center">
									<div class="text-2xl font-bold text-orange-600">
										{selectedBook.borrowedCopies || 0}
									</div>
									<div class="text-sm text-orange-600">Borrowed</div>
								</div>
								<div class="rounded-lg bg-purple-50 p-4 text-center">
									<div class="text-2xl font-bold text-purple-600">
										{selectedBook.reservedCopies || 0}
									</div>
									<div class="text-sm text-purple-600">Reserved</div>
								</div>
							</div>
						</div>

						<!-- Book Status -->
						<div class="border-t border-gray-200 pt-6">
							<h4 class="mb-4 text-lg font-semibold text-gray-900">Current Status</h4>
							<div class="flex items-center gap-2">
								{#if (selectedBook.availableCopies || 0) > 0}
									<div
										class="inline-flex items-center rounded-full border border-green-200 bg-green-100 px-2.5 py-0.5 text-xs font-medium text-green-800"
									>
										<CheckCircle class="mr-1 h-4 w-4" />
										Available to Borrow
									</div>
								{:else if (selectedBook.borrowedCopies || 0) > 0}
									<div
										class="inline-flex items-center rounded-full border border-orange-200 bg-orange-100 px-2.5 py-0.5 text-xs font-medium text-orange-800"
									>
										<Users class="mr-1 h-4 w-4" />
										Currently Borrowed
									</div>
								{:else}
									<div
										class="inline-flex items-center rounded-full border border-blue-200 bg-blue-100 px-2.5 py-0.5 text-xs font-medium text-blue-800"
									>
										<Clock class="mr-1 h-4 w-4" />
										Available for Reservation
									</div>
								{/if}
							</div>
						</div>

						<!-- Rating Summary -->
						{#if ratingSummary}
							<div class="border-t border-gray-200 pt-6">
								<h4 class="mb-4 text-lg font-semibold text-gray-900">Rating Summary</h4>
								<div class="flex items-center gap-4">
									<div class="text-center">
										<div class="text-3xl font-bold {getRatingColor(ratingSummary.average_rating)}">
											{ratingSummary.average_rating?.toFixed(1) || 'N/A'}
										</div>
										<div class="text-sm text-gray-600">
											{getRatingLabel(ratingSummary.average_rating)}
										</div>
										<div class="mt-1 text-lg text-yellow-500">
											{getRatingStars(ratingSummary.average_rating)}
										</div>
									</div>
									<div class="flex-1">
										<div class="mb-2 text-sm text-gray-600">
											Based on {ratingSummary.total_reviews} review{ratingSummary.total_reviews !==
											1
												? 's'
												: ''}
										</div>
										<div class="space-y-1">
											{#each [5, 4, 3, 2, 1] as star}
												{@const count = ratingSummary[`rating_${star}`] || 0}
												{@const percentage =
													ratingSummary.total_reviews > 0
														? (count / ratingSummary.total_reviews) * 100
														: 0}
												<div class="flex items-center gap-2 text-sm">
													<span class="w-8 text-yellow-500">{star}★</span>
													<div class="h-2 flex-1 rounded-full bg-gray-200">
														<div
															class="h-2 rounded-full bg-yellow-500"
															style="width: {percentage}%"
														></div>
													</div>
													<span class="w-8 text-gray-600">{count}</span>
												</div>
											{/each}
										</div>
									</div>
								</div>
							</div>
						{/if}

						<!-- Reviews Section -->
						<div class="border-t border-gray-200 pt-6">
							<h4 class="mb-4 text-lg font-semibold text-gray-900">
								Student Reviews ({bookReviews.length})
							</h4>

							{#if isLoadingReviews}
								<div class="py-8 text-center">
									<div
										class="mx-auto mb-2 h-6 w-6 animate-spin rounded-full border-b-2 border-blue-600"
									></div>
									<p class="text-gray-600">Loading reviews...</p>
								</div>
							{:else if bookReviews.length === 0}
								<div class="py-8 text-center text-gray-500">
									<p>
										No reviews yet. Students can review this book after borrowing and returning it.
									</p>
								</div>
							{:else}
								<div class="max-h-64 space-y-4 overflow-y-auto">
									{#each bookReviews as review}
										<div class="rounded-lg bg-gray-50 p-4">
											<div class="mb-2 flex items-start justify-between">
												<div class="flex items-center gap-2">
													<div
														class="flex h-8 w-8 items-center justify-center rounded-full bg-blue-100"
													>
														<span class="text-sm font-medium text-blue-600">
															{review.user_name?.charAt(0) || 'U'}
														</span>
													</div>
													<div>
														<div class="font-medium text-gray-900">
															{review.user_name || 'Anonymous'}
														</div>
														<div class="text-sm text-gray-500">
															{new Date(review.review_date).toLocaleDateString()}
														</div>
													</div>
												</div>
												<div class="flex items-center gap-1">
													<span class="text-lg text-yellow-500">
														{getRatingStars(review.rating)}
													</span>
													<span class="text-sm text-gray-600">({review.rating}/5)</span>
												</div>
											</div>
											{#if review.review_text}
												<p class="text-sm leading-relaxed text-gray-700">{review.review_text}</p>
											{/if}
										</div>
									{/each}
								</div>
							{/if}
						</div>

						<!-- Action Instructions (Admin View) -->
						<div class="border-t border-gray-200 pt-6">
							<h4 class="mb-4 text-lg font-semibold text-gray-900">Admin Information</h4>
							<div class="rounded-lg bg-blue-50 p-4">
								<h5 class="mb-2 font-medium text-blue-900">Book Management Actions</h5>
								<ul class="space-y-1 text-sm text-blue-800">
									<li>• <strong>Edit:</strong> Modify book details, category, or location</li>
									<li>• <strong>Manage Copies:</strong> Add, remove, or update book copy status</li>
									<li>
										• <strong>View Details:</strong> See comprehensive book information and student feedback
									</li>
									<li>• <strong>Delete:</strong> Remove book from library (use with caution)</li>
								</ul>
							</div>
						</div>
					</div>

					<!-- Modal Footer -->
					<div class="flex items-center justify-end gap-3 border-t border-gray-200 p-6">
						<Button onclick={closeBookModal} variant="outline">Close</Button>
					</div>
				</div>
			</div>
		{/if}
	</div>

	<!-- Footer Navigation -->
	<div class="mt-16 border-t bg-white">
		<div class="mx-auto max-w-7xl px-6 py-12">
			<div class="mb-8 text-center">
				<h3 class="mb-2 text-xl font-semibold text-gray-900">Library Management Hub</h3>
				<p class="text-gray-600">Complete access to all library administration functions</p>
			</div>

			<div class="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
				<!-- Add Books Section -->
				<div class="text-center">
					<div
						class="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-green-100"
					>
						<Plus class="h-6 w-6 text-green-600" />
					</div>
					<h4 class="mb-2 font-semibold text-gray-900">Add Books</h4>
					<p class="mb-4 text-sm text-gray-600">Expand your collection with new books</p>
					<Button
						onclick={() => goto('/admin/library/add')}
						variant="outline"
						size="sm"
						class="w-full"
					>
						Go to Add Books
					</Button>
				</div>

				<!-- Edit Books Section -->
				<div class="text-center">
					<div
						class="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-blue-100"
					>
						<Edit3 class="h-6 w-6 text-blue-600" />
					</div>
					<h4 class="mb-2 font-semibold text-gray-900">Edit Books</h4>
					<p class="mb-4 text-sm text-gray-600">Modify existing book information</p>
					<Button
						onclick={() => goto('/admin/library/edit')}
						variant="outline"
						size="sm"
						class="w-full"
					>
						Go to Edit Books
					</Button>
				</div>

				<!-- Delete Books Section -->
				<div class="text-center">
					<div
						class="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-red-100"
					>
						<Trash2 class="h-6 w-6 text-red-600" />
					</div>
					<h4 class="mb-2 font-semibold text-gray-900">Delete Books</h4>
					<p class="mb-4 text-sm text-gray-600">Remove outdated or damaged books</p>
					<Button
						onclick={() => goto('/admin/library/delete')}
						variant="outline"
						size="sm"
						class="w-full"
					>
						Go to Delete Books
					</Button>
				</div>

				<!-- Manage Copies Section -->
				<div class="text-center">
					<div
						class="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-purple-100"
					>
						<Settings class="h-6 w-6 text-purple-600" />
					</div>
					<h4 class="mb-2 font-semibold text-gray-900">Manage Copies</h4>
					<p class="mb-4 text-sm text-gray-600">Control book copy availability</p>
					<Button
						onclick={() => goto('/admin/library/manage-copies')}
						variant="outline"
						size="sm"
						class="w-full"
					>
						Go to Manage Copies
					</Button>
				</div>
			</div>

			<div class="mt-8 border-t border-gray-200 pt-8 text-center">
				<Button onclick={() => goto('/admin')} variant="ghost" size="sm">
					← Back to Admin Dashboard
				</Button>
			</div>
		</div>
	</div>
</div>
