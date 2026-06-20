<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import {
		Card,
		CardContent,
		CardDescription,
		CardHeader,
		CardTitle
	} from '$lib/components/ui/card';
	import { Input } from '$lib/components/ui/input';
	import { Label } from '$lib/components/ui/label';
	import { Button } from '$lib/components/ui/button';
	import { Separator } from '$lib/components/ui/separator';
	import { Badge } from '$lib/components/ui/badge';
	import {
		BookOpen,
		Trash2,
		ArrowLeft,
		Search,
		Filter,
		AlertTriangle,
		CheckCircle,
		AlertCircle
	} from '@lucide/svelte';
	import type { Book } from '$lib/types/book';

	let { data } = $props();

	let books = $state<Book[]>([]);
	let selectedBook = $state<Book | null>(null);
	let searchQuery = $state('');
	let loading = $state(false);
	let message = $state('');
	let messageType = $state('success');

	onMount(() => {
		loadBooks();
	});

	// Refresh data when returning from deletion
	$effect(() => {
		// This will run when the component mounts or when dependencies change
		if (books.length === 0 && !loading) {
			loadBooks();
		}
	});

	async function loadBooks() {
		loading = true;
		try {
			// Add timestamp to ensure fresh data
			const response = await fetch(`/api/admin/books?t=${Date.now()}`);
			const result = await response.json();

			if (result.success) {
				books = result.books;
			} else {
				showMessage('Failed to load books: ' + result.error, 'error');
			}
		} catch (error) {
			showMessage('Error loading books: ' + error, 'error');
		} finally {
			loading = false;
		}
	}

	function filterBooks() {
		if (!searchQuery.trim()) {
			return getDeletableBooks();
		}

		const query = searchQuery.toLowerCase();
		return getDeletableBooks().filter(
			(book) =>
				book.title?.toLowerCase().includes(query) ||
				book.author?.toLowerCase().includes(query) ||
				book.isbn?.toLowerCase().includes(query) ||
				book.category?.toLowerCase().includes(query)
		);
	}

	function selectBook(book: Book) {
		// Check if there are any available copies to delete
		if ((book.availableCopies || 0) === 0) {
			showMessage(`Cannot delete "${book.title}": No available copies to delete`, 'error');
			return;
		}

		selectedBook = book;
	}

	// Filter books to only show those that can be deleted
	function getDeletableBooks() {
		return books.filter((book) => {
			const availableCopies = book.availableCopies || 0;
			const borrowedCopies = book.borrowedCopies || 0;
			const reservedCopies = book.reservedCopies || 0;

			// Only show books that have meaningful copies and have available copies to delete
			const hasMeaningfulCopies = availableCopies > 0 || borrowedCopies > 0 || reservedCopies > 0;
			return hasMeaningfulCopies && availableCopies > 0;
		});
	}

	// Get books that cannot be deleted (for informational purposes)
	// Only show books that have borrowed or reserved copies, not books with no copies at all
	function getNonDeletableBooks() {
		return books.filter((book) => {
			const availableCopies = book.availableCopies || 0;
			const borrowedCopies = book.borrowedCopies || 0;
			const reservedCopies = book.reservedCopies || 0;
			const totalCopies = book.totalCopies || 0;

			// Only show books that have copies but they are borrowed or reserved
			// Don't show books that have no copies at all
			return totalCopies > 0 && (borrowedCopies > 0 || reservedCopies > 0);
		});
	}

	function showMessage(msg: string, type: 'success' | 'error') {
		message = msg;
		messageType = type;
		setTimeout(() => {
			message = '';
		}, 5000);
	}

	$effect(() => {
		filterBooks();
	});
</script>

<div class="min-h-screen bg-gradient-to-br from-gray-50 via-white to-red-50">
	<!-- Header Section -->
	<div class="border-b bg-white shadow-sm">
		<div class="mx-auto max-w-7xl px-6 py-8">
			<!-- Breadcrumb Navigation -->
			<div class="mb-4 flex items-center gap-2 text-sm text-gray-600">
				<Button
					onclick={() => goto('/admin')}
					variant="ghost"
					size="sm"
					class="text-gray-500 hover:text-gray-700"
				>
					Admin Dashboard
				</Button>
				<span>/</span>
				<Button
					onclick={() => goto('/admin/library')}
					variant="ghost"
					size="sm"
					class="text-gray-500 hover:text-gray-700"
				>
					Library Management
				</Button>
				<span>/</span>
				<span class="font-medium text-gray-900">Delete Books</span>
			</div>

			<div class="flex flex-col gap-6 lg:flex-row lg:items-center lg:justify-between">
				<div>
					<div class="mb-4 flex items-center gap-4">
						<Button onclick={() => goto('/admin/library')} variant="outline" size="sm">
							<ArrowLeft class="mr-2 h-4 w-4" />
							Back to Library
						</Button>
					</div>
					<h1 class="text-3xl font-bold text-gray-900 sm:text-4xl">Delete Books</h1>
					<p class="mt-2 text-lg text-gray-600">
						Permanently remove books from your library collection
					</p>

					<!-- Warning Banner -->
					<div class="mt-4 rounded-lg border-2 border-red-200 bg-red-50 p-4">
						<div class="flex items-center gap-3">
							<AlertTriangle class="h-5 w-5 text-red-600" />
							<span class="font-medium text-red-700">
								⚠️ Warning: This action cannot be undone. Books and all their copies will be
								permanently deleted.
							</span>
						</div>
					</div>
				</div>

				<div class="flex items-center gap-3">
					<div class="rounded-lg border border-red-200 bg-red-50 px-3 py-1">
						<span class="text-sm font-medium text-red-700"> Book Removal </span>
					</div>
				</div>
			</div>
		</div>
	</div>

	<!-- Main Content -->
	<div class="mx-auto max-w-7xl px-6 py-8">
		<!-- Message Alert -->
		{#if message}
			<div
				class={`mb-8 rounded-lg border-2 p-4 shadow-lg ${
					messageType === 'success'
						? 'border-green-200 bg-green-50 text-green-800'
						: 'border-red-200 bg-red-50 text-red-800'
				}`}
			>
				<div class="flex items-center gap-3">
					{#if messageType === 'success'}
						<CheckCircle class="h-5 w-5 text-green-600" />
					{:else}
						<AlertCircle class="h-5 w-5 text-red-600" />
					{/if}
					<span class="font-medium">{message}</span>
				</div>
			</div>
		{/if}

		<!-- Search Section -->
		<Card class="mb-6">
			<CardContent class="p-6">
				<div class="flex flex-col items-center justify-between gap-4 sm:flex-row">
					<div class="flex-1">
						<h2 class="mb-3 text-lg font-semibold">Search Books</h2>
						<Input
							bind:value={searchQuery}
							placeholder="Search by title, author, ISBN, or category..."
							class="w-full"
						/>
					</div>

					<button
						onclick={loadBooks}
						disabled={loading}
						class="flex items-center rounded-md border border-gray-300 px-4 py-2 disabled:opacity-50"
					>
						{#if loading}
							<span class="mr-2 animate-spin">⏳</span>
						{/if}
						<span class="mr-2">🔄</span>
						Refresh Books
					</button>
				</div>
			</CardContent>
		</Card>

		<!-- Books List -->
		{#if loading}
			<div class="flex items-center justify-center py-12">
				<span class="mr-2 animate-spin text-2xl text-blue-600">⏳</span>
				<span class="text-muted-foreground">Loading books...</span>
			</div>
		{:else if filterBooks().length === 0}
			<Card>
				<CardContent class="p-12 text-center">
					<span class="mx-auto mb-4 block text-6xl text-muted-foreground">📚</span>
					<h3 class="mb-2 text-lg font-semibold text-muted-foreground">No books found</h3>
					<p class="mb-4 text-muted-foreground">
						{searchQuery
							? 'No books match your search criteria.'
							: 'No books available for deletion.'}
					</p>
					<button
						onclick={() => goto('/admin/library/add')}
						class="rounded-lg bg-blue-600 px-6 py-3 text-white hover:bg-blue-700"
					>
						<span class="mr-2">➕</span>
						Add Your First Book
					</button>
				</CardContent>
			</Card>
		{:else}
			<!-- Deletable Books Section -->
			<div class="mb-8">
				<h2 class="mb-4 text-2xl font-bold text-gray-900">📚 Books Available for Deletion</h2>
				<p class="mb-6 text-gray-600">
					These books have available copies that can be safely deleted. Note: Books with borrowed or
					reserved copies will still show available copies for deletion.
				</p>

				<div class="grid gap-6">
					{#each filterBooks() as book}
						<Card
							class="cursor-pointer transition-shadow hover:shadow-md {selectedBook?.id === book.id
								? 'ring-2 ring-red-500'
								: ''}"
							onclick={() => selectBook(book)}
						>
							<CardContent class="p-6">
								<div class="flex items-start justify-between">
									<div class="flex-1">
										<div class="mb-3 flex items-center gap-3">
											<h3 class="text-2xl font-bold text-foreground">{book.title}</h3>
											<Badge variant="outline" class="text-xs">book</Badge>
											<Badge variant="secondary" class="text-xs">Safe to Delete</Badge>
										</div>

										<p class="mb-4 text-lg text-muted-foreground">by {book.author}</p>

										<div class="mb-4 grid grid-cols-2 gap-4 md:grid-cols-4">
											<div class="flex items-center gap-2">
												<span class="text-muted-foreground">🔢</span>
												<span class="text-sm text-muted-foreground">ISBN:</span>
												<span class="font-medium">{book.isbn}</span>
											</div>

											<div class="flex items-center gap-2">
												<span class="text-muted-foreground">📚</span>
												<span class="text-sm text-muted-foreground">Category:</span>
												<span class="font-medium">{book.category}</span>
											</div>

											<div class="flex items-center gap-2">
												<span class="text-muted-foreground">📅</span>
												<span class="text-sm text-muted-foreground">Year:</span>
												<span class="font-medium">{book.published_year}</span>
											</div>

											<div class="flex items-center gap-2">
												<span class="text-muted-foreground">📍</span>
												<span class="text-sm text-muted-foreground">Location:</span>
												<span class="font-medium">{book.location}</span>
											</div>
										</div>

										<!-- Copies Status Box -->
										<div class="rounded-lg border border-green-200 bg-green-50 p-4">
											<div class="mb-3 flex items-center gap-2">
												<span class="text-xl text-green-600">📚</span>
												<span class="font-semibold text-green-800"
													>{book.totalCopies || 0} Total Copies</span
												>
											</div>

											<div class="grid grid-cols-3 gap-4 text-center">
												<div>
													<span class="font-semibold text-green-600"
														>{book.availableCopies || 0}</span
													>
													<p class="text-xs text-muted-foreground">Available</p>
												</div>
												<div>
													<span class="font-semibold text-orange-600"
														>{book.borrowedCopies || 0}</span
													>
													<p class="text-xs text-muted-foreground">Borrowed</p>
												</div>
												<div>
													<span class="font-semibold text-blue-600">{book.reservedCopies || 0}</span
													>
													<p class="text-xs text-muted-foreground">Reserved</p>
												</div>
											</div>

											<div
												class="mt-3 rounded border border-green-200 bg-green-100 p-2 text-center"
											>
												<span class="text-xs font-medium text-green-700">
													✅ Safe to delete: {book.availableCopies || 0} available copies
													{#if (book.borrowedCopies || 0) > 0 || (book.reservedCopies || 0) > 0}
														, {book.borrowedCopies || 0} borrowed, {book.reservedCopies || 0} reserved
													{/if}
												</span>
											</div>
										</div>
									</div>

									<!-- Selection Indicator -->
									<div class="ml-6 flex items-center gap-2">
										{#if selectedBook?.id === book.id}
											<Badge variant="destructive" class="">Selected for Deletion</Badge>
										{:else}
											<Badge variant="outline" class="">Click to select</Badge>
										{/if}
									</div>
								</div>
							</CardContent>
						</Card>
					{/each}
				</div>
			</div>

			<!-- Protected Books Section (Informational) -->
			{#if getNonDeletableBooks().length > 0}
				<div class="mt-8 mb-8">
					<h2 class="mb-4 text-2xl font-bold text-gray-900">
						🔒 Protected Books (Cannot be Deleted)
					</h2>
					<p class="mb-6 text-gray-600">
						These books have copies that are currently borrowed or reserved and cannot be deleted.
					</p>

					<div class="grid gap-6">
						{#each getNonDeletableBooks() as book}
							<Card class="cursor-not-allowed opacity-60">
								<CardContent class="p-6">
									<div class="flex items-start justify-between">
										<div class="flex-1">
											<div class="mb-3 flex items-center gap-3">
												<h3 class="text-2xl font-bold text-foreground">{book.title}</h3>
												<Badge variant="outline" class="text-xs">book</Badge>
												{#if (book.borrowedCopies || 0) > 0 || (book.reservedCopies || 0) > 0}
													<Badge variant="destructive" class="text-xs">Protected</Badge>
												{:else if (book.availableCopies || 0) === 0}
													<Badge variant="secondary" class="text-xs">No Copies</Badge>
												{/if}
											</div>

											<p class="mb-4 text-lg text-muted-foreground">by {book.author}</p>

											<div class="mb-4 grid grid-cols-2 gap-4 md:grid-cols-4">
												<div class="flex items-center gap-2">
													<span class="text-muted-foreground">🔢</span>
													<span class="text-sm text-muted-foreground">ISBN:</span>
													<span class="font-medium">{book.isbn}</span>
												</div>

												<div class="flex items-center gap-2">
													<span class="text-muted-foreground">📚</span>
													<span class="text-sm text-muted-foreground">Category:</span>
													<span class="font-medium">{book.category}</span>
												</div>

												<div class="flex items-center gap-2">
													<span class="text-muted-foreground">📅</span>
													<span class="text-sm text-muted-foreground">Year:</span>
													<span class="font-medium">{book.published_year}</span>
												</div>

												<div class="flex items-center gap-2">
													<span class="text-muted-foreground">📍</span>
													<span class="text-sm text-muted-foreground">Location:</span>
													<span class="font-medium">{book.location}</span>
												</div>
											</div>

											<!-- Copies Status Box -->
											<div class="rounded-lg border border-red-200 bg-red-50 p-4">
												<div class="mb-3 flex items-center gap-2">
													<span class="text-xl text-red-600">📚</span>
													<span class="font-semibold text-red-800"
														>{book.totalCopies || 0} Total Copies</span
													>
												</div>

												<div class="grid grid-cols-3 gap-4 text-center">
													<div>
														<span class="font-semibold text-green-600"
															>{book.availableCopies || 0}</span
														>
														<p class="text-xs text-muted-foreground">Available</p>
													</div>
													<div>
														<span class="font-semibold text-orange-600"
															>{book.borrowedCopies || 0}</span
														>
														<p class="text-xs text-muted-foreground">Borrowed</p>
													</div>
													<div>
														<span class="font-semibold text-blue-600"
															>{book.reservedCopies || 0}</span
														>
														<p class="text-xs text-muted-foreground">Reserved</p>
													</div>
												</div>

												<!-- Warning for books that can't be deleted -->
												{#if (book.borrowedCopies || 0) > 0 || (book.reservedCopies || 0) > 0}
													<div
														class="mt-3 rounded border border-yellow-200 bg-yellow-50 p-2 text-center"
													>
														<span class="text-xs font-medium text-yellow-700">
															⚠️ Cannot delete: Has {(book.borrowedCopies || 0) > 0
																? `${book.borrowedCopies || 0} borrowed`
																: ''}{(book.borrowedCopies || 0) > 0 &&
															(book.reservedCopies || 0) > 0
																? ' and '
																: ''}{(book.reservedCopies || 0) > 0
																? `${book.reservedCopies || 0} reserved`
																: ''} copies
														</span>
													</div>
												{:else if (book.availableCopies || 0) === 0}
													<div
														class="mt-3 rounded border border-gray-200 bg-gray-50 p-2 text-center"
													>
														<span class="text-xs font-medium text-gray-700">
															ℹ️ No copies available for deletion
														</span>
													</div>
												{/if}
											</div>
										</div>

										<!-- Protection Status -->
										<div class="ml-6 flex items-center gap-2">
											<Badge variant="outline" class="text-xs">Protected</Badge>
										</div>
									</div>
								</CardContent>
							</Card>
						{/each}
					</div>
				</div>
			{/if}
		{/if}

		<!-- Delete Button -->
		{#if selectedBook}
			<div class="mt-8 flex justify-center">
				<button
					onclick={() => selectedBook && goto(`/admin/library/delete/${selectedBook.id}`)}
					class="flex items-center rounded-lg bg-red-600 px-8 py-3 text-lg font-medium text-white hover:bg-red-700"
				>
					Delete "{selectedBook.title}"
				</button>
			</div>
		{/if}

		<!-- Help Section -->
		<Card class="mt-8">
			<CardHeader>
				<CardTitle>How to Delete Books</CardTitle>
			</CardHeader>
			<CardContent class="space-y-3">
				<div class="flex items-start gap-3">
					<Badge variant="outline" class="mt-1">1️⃣</Badge>
					<div>
						<p class="font-medium">Search and Select</p>
						<p class="text-sm text-muted-foreground">
							Use the search bar to find the book you want to delete, then click on it to select.
						</p>
					</div>
				</div>

				<div class="flex items-start gap-3">
					<Badge variant="outline" class="mt-1">2️⃣</Badge>
					<div>
						<p class="font-medium">Review Details</p>
						<p class="text-sm text-muted-foreground">
							The selected book will be highlighted with a red ring and marked as "Selected for
							Deletion".
						</p>
					</div>
				</div>

				<div class="flex items-start gap-3">
					<Badge variant="outline" class="mt-1">3️⃣</Badge>
					<div>
						<p class="font-medium">Confirm Deletion</p>
						<p class="text-sm text-muted-foreground">
							Click the "Delete" button to proceed to the confirmation page where you can review and
							confirm the deletion.
						</p>
					</div>
				</div>

				<div class="flex items-start gap-3">
					<Badge variant="outline" class="mt-1">⚠️</Badge>
					<div>
						<p class="font-medium text-red-600">Important Warning</p>
						<p class="text-sm text-red-600">
							Deleting a book will permanently remove it and all its copies from the library. This
							action cannot be undone.
						</p>
					</div>
				</div>

				<div class="flex items-start gap-3">
					<Badge variant="outline" class="mt-1">🔒</Badge>
					<div>
						<p class="font-medium text-orange-600">Deletion Restrictions</p>
						<p class="text-sm text-orange-600">
							Books with borrowed or reserved copies cannot be deleted. Only available copies can be
							removed from the library.
						</p>
					</div>
				</div>
			</CardContent>
		</Card>
	</div>
</div>
