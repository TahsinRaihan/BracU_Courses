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
	import {
		BookOpen,
		Edit3,
		ArrowLeft,
		Search,
		Filter,
		Eye,
		Pencil,
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

	async function loadBooks() {
		loading = true;
		try {
			const response = await fetch('/api/admin/books');
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
		// First filter out books with no meaningful copies
		const booksWithMeaningfulCopies = books.filter((book) => {
			const availableCopies = book.availableCopies || 0;
			const borrowedCopies = book.borrowedCopies || 0;
			const reservedCopies = book.reservedCopies || 0;
			return availableCopies > 0 || borrowedCopies > 0 || reservedCopies > 0;
		});
		
		if (!searchQuery.trim()) {
			return booksWithMeaningfulCopies;
		}

		const query = searchQuery.toLowerCase();
		return booksWithMeaningfulCopies.filter(
			(book) =>
				book.title?.toLowerCase().includes(query) ||
				book.author?.toLowerCase().includes(query) ||
				book.isbn?.toLowerCase().includes(query) ||
				book.category?.toLowerCase().includes(query)
		);
	}

	function selectBook(book: Book) {
		selectedBook = book;
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

<div class="min-h-screen bg-gradient-to-br from-gray-50 via-white to-blue-50">
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
				<span class="font-medium text-gray-900">Edit Books</span>
			</div>

			<div class="flex flex-col gap-6 lg:flex-row lg:items-center lg:justify-between">
				<div>
					<div class="mb-4 flex items-center gap-4">
						<Button onclick={() => goto('/admin/library')} variant="outline" size="sm">
							<ArrowLeft class="mr-2 h-4 w-4" />
							Back to Library
						</Button>
					</div>
					<h1 class="text-3xl font-bold text-gray-900 sm:text-4xl">Edit Books</h1>
					<p class="mt-2 text-lg text-gray-600">
						Select and modify book information in your library
					</p>
				</div>

				<div class="flex items-center gap-3">
					<div class="rounded-lg border border-purple-200 bg-purple-50 px-3 py-1">
						<span class="text-sm font-medium text-purple-700"> Book Editor </span>
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

		<!-- Search and Filter Section -->
		<Card class="mb-8 border-0 bg-white/80 shadow-xl backdrop-blur-sm">
			<CardHeader class="pb-6">
				<div class="mb-4 flex items-center gap-3">
					<div
						class="flex h-12 w-12 items-center justify-center rounded-full bg-gradient-to-br from-purple-500 to-pink-600"
					>
						<Search class="h-6 w-6 text-white" />
					</div>
					<div>
						<CardTitle class="text-xl text-gray-900">Find Books to Edit</CardTitle>
						<CardDescription class="text-gray-600">
							Search and filter books to select which one to modify
						</CardDescription>
					</div>
				</div>
			</CardHeader>

			<CardContent class="p-6">
				<div class="flex flex-col items-center justify-between gap-4 sm:flex-row">
					<div class="flex-1">
						<Label for="search" class="mb-2 block text-sm font-medium text-gray-700"
							>Search Books</Label
						>
						<div class="relative">
							<Search
								class="absolute top-1/2 left-3 h-4 w-4 -translate-y-1/2 transform text-gray-400"
							/>
							<Input
								id="search"
								bind:value={searchQuery}
								placeholder="Search by title, author, ISBN, or category..."
								class="w-full border-gray-300 pl-10 focus:border-purple-500 focus:ring-purple-500"
							/>
						</div>
					</div>

					<Button onclick={loadBooks} disabled={loading} variant="outline" class="px-6 py-3">
						{#if loading}
							<div
								class="mr-2 h-4 w-4 animate-spin rounded-full border-b-2 border-purple-600"
							></div>
						{/if}
						<Filter class="mr-2 h-4 w-4" />
						Refresh Books
					</Button>
				</div>
			</CardContent>
		</Card>

		<!-- Books List -->
		{#if loading}
			<div class="flex items-center justify-center py-16">
				<div class="text-center">
					<div
						class="mx-auto mb-4 h-12 w-12 animate-spin rounded-full border-b-2 border-purple-600"
					></div>
					<p class="font-medium text-gray-600">Loading books...</p>
				</div>
			</div>
		{:else if filterBooks().length === 0}
			<Card>
				<CardContent class="p-12 text-center">
					<span class="mx-auto mb-4 block text-6xl text-muted-foreground">📚</span>
					<h3 class="mb-2 text-lg font-semibold text-muted-foreground">No books found</h3>
					<p class="mb-4 text-muted-foreground">
						{searchQuery
							? 'No books match your search criteria.'
							: 'No books available for editing.'}
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
			<div class="grid gap-6">
				{#each filterBooks() as book}
					<Card
						class="cursor-pointer transition-shadow hover:shadow-md {selectedBook?.id === book.id
							? 'ring-2 ring-blue-500'
							: ''}"
						onclick={() => selectBook(book)}
					>
						<CardContent class="p-6">
							<div class="flex items-start justify-between">
								<div class="flex-1">
									<div class="mb-3 flex items-center gap-3">
										<h3 class="text-2xl font-bold text-foreground">{book.title}</h3>
										<div
											class="inline-flex items-center rounded-md border border-gray-200 bg-white px-2 py-1 text-xs font-medium text-gray-700"
										>
											book
										</div>
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
									<div class="rounded-lg border border-blue-200 bg-blue-50 p-4">
										<div class="mb-3 flex items-center gap-2">
											<span class="text-xl text-blue-600">📚</span>
											<span class="font-semibold text-blue-800">{book.totalCopies || 0} Copies</span
											>
										</div>

										<div class="grid grid-cols-3 gap-4 text-center">
											<div>
												<span class="font-semibold text-green-600">{book.availableCopies || 0}</span
												>
												<p class="text-xs text-muted-foreground">Available</p>
											</div>
											<div>
												<span class="font-semibold text-orange-600">{book.borrowedCopies || 0}</span
												>
												<p class="text-xs text-muted-foreground">Borrowed</p>
											</div>
											<div>
												<span class="font-semibold text-blue-600">{book.reservedCopies || 0}</span>
												<p class="text-xs text-muted-foreground">Reserved</p>
											</div>
										</div>
									</div>
								</div>

								<!-- Selection Indicator -->
								<div class="ml-6 flex items-center gap-2">
									{#if selectedBook?.id === book.id}
										<div
											class="inline-flex items-center rounded-md bg-blue-600 px-2 py-1 text-xs font-medium text-white"
										>
											Selected
										</div>
									{:else}
										<div
											class="inline-flex items-center rounded-md border border-gray-200 bg-white px-2 py-1 text-xs font-medium text-gray-700"
										>
											Click to select
										</div>
									{/if}
								</div>
							</div>
						</CardContent>
					</Card>
				{/each}
			</div>
		{/if}

		<!-- Edit Button -->
		{#if selectedBook}
			<div class="mt-8 flex justify-center">
				<button
					onclick={() => goto(`/admin/library/edit/${selectedBook.id}`)}
					size="lg"
					class="flex items-center rounded-lg bg-blue-600 px-8 py-3 text-lg font-medium text-white hover:bg-blue-700"
				>
					<span class="mr-2">✏️</span>
					Edit "{selectedBook.title}"
				</button>
			</div>
		{/if}

		<!-- Help Section -->
		<Card class="mt-8">
			<CardHeader>
				<CardTitle>How to Edit Books</CardTitle>
			</CardHeader>
			<CardContent class="space-y-3">
				<div class="flex items-start gap-3">
					<div
						class="mt-1 inline-flex items-center rounded-md border border-gray-200 bg-white px-2 py-1 text-xs font-medium text-gray-700"
					>
						1️⃣
					</div>
					<div>
						<p class="font-medium">Search and Select</p>
						<p class="text-sm text-muted-foreground">
							Use the search bar to find the book you want to edit, then click on it to select.
						</p>
					</div>
				</div>

				<div class="flex items-start gap-3">
					<div
						class="mt-1 inline-flex items-center rounded-md border border-gray-200 bg-white px-2 py-1 text-xs font-medium text-gray-700"
					>
						2️⃣
					</div>
					<div>
						<p class="font-medium">Review Details</p>
						<p class="text-sm text-muted-foreground">
							The selected book will be highlighted with a blue ring and marked as "Selected".
						</p>
					</div>
				</div>

				<div class="flex items-start gap-3">
					<div
						class="mt-1 inline-flex items-center rounded-md border border-gray-200 bg-white px-2 py-1 text-xs font-medium text-gray-700"
					>
						3️⃣
					</div>
					<div>
						<p class="font-medium">Edit Book</p>
						<p class="text-sm text-muted-foreground">
							Click the "Edit" button to open the editing form for the selected book.
						</p>
					</div>
				</div>
			</CardContent>
		</Card>
	</div>
</div>
