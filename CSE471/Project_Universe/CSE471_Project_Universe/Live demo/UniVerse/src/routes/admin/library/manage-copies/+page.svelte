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
	import { Badge } from '$lib/components/ui/badge';
	import { BookOpen, Settings, ArrowLeft, Search, Filter, Plus, Edit } from '@lucide/svelte';

	let books = $state<any[]>([]);
	let filteredBooks = $state<any[]>([]);
	let searchQuery = $state('');
	let selectedCategory = $state('all');
	let isLoading = $state(true);
	let error = $state('');

	const categories = [
		'all',
		'Fiction',
		'Non-Fiction',
		'Science',
		'Technology',
		'History',
		'Philosophy',
		'Literature',
		'Mathematics',
		'Computer Science'
	];

	onMount(async () => {
		await loadBooks();
	});

	async function loadBooks() {
		try {
			isLoading = true;
			error = '';
			console.log('Loading books...');
			
			const response = await fetch('/api/admin/books');
			console.log('Response status:', response.status);
			
			if (response.ok) {
				const result = await response.json();
				console.log('API result:', result);
				
				if (result.success && result.books) {
					books = result.books;
					// Apply filtering immediately after loading
					filterBooks();
					console.log('Books loaded:', books.length);
				} else {
					books = [];
					filteredBooks = [];
					error = result.error || 'No books found';
				}
			} else {
				error = `HTTP ${response.status}: ${response.statusText}`;
				books = [];
				filteredBooks = [];
			}
		} catch (err) {
			console.error('Error loading books:', err);
			error = err instanceof Error ? err.message : 'Failed to load books';
			books = [];
			filteredBooks = [];
		} finally {
			isLoading = false;
		}
	}

	function filterBooks() {
		filteredBooks = books.filter((book) => {
			// Only show books that have meaningful copies (available, borrowed, or reserved > 0)
			const availableCopies = book.availableCopies || 0;
			const borrowedCopies = book.borrowedCopies || 0;
			const reservedCopies = book.reservedCopies || 0;
			const hasMeaningfulCopies = availableCopies > 0 || borrowedCopies > 0 || reservedCopies > 0;
			
			const matchesSearch =
				book.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
				book.author.toLowerCase().includes(searchQuery.toLowerCase()) ||
				book.isbn.includes(searchQuery);
			const matchesCategory = selectedCategory === 'all' || book.category === selectedCategory;
			return hasMeaningfulCopies && matchesSearch && matchesCategory;
		});
	}

	$effect(() => {
		filterBooks();
	});
</script>

<svelte:head>
	<title>Manage Book Copies - Admin Dashboard</title>
</svelte:head>

<div class="min-h-screen bg-gradient-to-br from-gray-50 via-white to-blue-50">
	<!-- Header Section -->
	<div class="border-b bg-white shadow-sm">
		<div class="mx-auto max-w-7xl px-6 py-8">
			<div class="flex flex-col gap-6 lg:flex-row lg:items-center lg:justify-between">
				<div>
					<div class="mb-4 flex items-center gap-4">
						<Button onclick={() => goto('/admin/library')} variant="outline" size="sm">
							<ArrowLeft class="mr-2 h-4 w-4" />
							Back to Library
						</Button>
					</div>
					<h1 class="text-3xl font-bold text-gray-900 sm:text-4xl">Manage Book Copies</h1>
					<p class="mt-2 text-lg text-gray-600">
						Select a book to manage its copies, availability, and status
					</p>
				</div>

				<div class="flex items-center gap-3">
					<div class="rounded-lg border border-blue-200 bg-blue-50 px-3 py-1">
						<span class="text-sm font-medium text-blue-700"> Copy Management </span>
					</div>
				</div>
			</div>
		</div>
	</div>

	<!-- Search and Filter -->
	<div class="mx-auto max-w-7xl px-6 py-8">
		<Card class="mb-8 border-0 bg-white/80 shadow-lg backdrop-blur-sm">
			<CardContent class="p-6">
				<div class="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
					<div>
						<Label for="search" class="mb-2 block text-sm font-medium text-gray-700">
							Search Books
						</Label>
						<div class="relative">
							<Search
								class="absolute top-1/2 left-3 h-4 w-4 -translate-y-1/2 transform text-gray-400"
							/>
							<Input
								id="search"
								bind:value={searchQuery}
								placeholder="Search by title, author, or ISBN..."
								class="pl-10"
							/>
						</div>
					</div>

					<div>
						<Label for="category" class="mb-2 block text-sm font-medium text-gray-700">
							Category
						</Label>
						<select
							id="category"
							bind:value={selectedCategory}
							class="w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:ring-2 focus:ring-blue-500 focus:outline-none"
						>
							{#each categories as category}
								<option value={category}>
									{category === 'all' ? 'All Categories' : category}
								</option>
							{/each}
						</select>
					</div>

					<div class="flex items-end">
						<Button onclick={loadBooks} variant="outline" class="w-full">
							<Filter class="mr-2 h-4 w-4" />
							Refresh
						</Button>
					</div>
				</div>
			</CardContent>
		</Card>

		<!-- Books List -->
		<Card class="border-0 bg-white/80 shadow-lg backdrop-blur-sm">
			<CardHeader>
				<div class="flex items-center justify-between">
					<div>
						<CardTitle class="text-2xl text-gray-900">Select Book to Manage</CardTitle>
						<CardDescription>
							{filteredBooks.length} book{filteredBooks.length !== 1 ? 's' : ''} found
						</CardDescription>
					</div>
				</div>
			</CardHeader>

			<CardContent>
				{#if error}
					<div class="py-12 text-center">
						<div class="mx-auto mb-4 h-16 w-16 rounded-full bg-red-100 flex items-center justify-center">
							<span class="text-2xl text-red-600">⚠️</span>
						</div>
						<h3 class="mb-2 text-lg font-medium text-red-900">Error Loading Books</h3>
						<p class="mb-4 text-red-600">{error}</p>
						<Button onclick={loadBooks} variant="outline" class="px-6 py-2">
							Try Again
						</Button>
					</div>
				{:else if isLoading}
					<div class="py-12 text-center">
						<div
							class="mx-auto mb-4 h-12 w-12 animate-spin rounded-full border-b-2 border-blue-600"
						></div>
						<p class="text-gray-600">Loading books...</p>
					</div>
				{:else if filteredBooks.length === 0}
					<div class="py-16 text-center">
						<BookOpen class="mx-auto mb-4 h-16 w-16 text-gray-400" />
						<h3 class="mb-2 text-lg font-medium text-gray-900">No books found</h3>
						<p class="mb-6 text-gray-600">No books match your search criteria.</p>
						<Button onclick={() => goto('/admin/library/add')} class="px-6 py-3">
							Add New Book
						</Button>
					</div>
				{:else}
					<div class="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
						{#each filteredBooks as book}
							<Card
								class="border border-gray-200 transition-all duration-200 hover:border-blue-300 hover:shadow-md"
							>
								<CardContent class="p-6">
									<div class="mb-4 flex items-start gap-4">
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
										<div class="min-w-0 flex-1">
											<h3 class="mb-2 text-lg leading-tight font-semibold text-gray-900">
												{book.title}
											</h3>
											<p class="mb-1 text-sm text-gray-600">by {book.author}</p>
											<p class="mb-2 text-xs text-gray-500">ISBN: {book.isbn}</p>
											<Badge variant="secondary" class="text-xs">{book.category}</Badge>
										</div>
									</div>

									<Separator class="my-4" />

									<div class="mb-4 space-y-2">
										<div class="flex justify-between text-sm">
											<span class="text-gray-600">Total Copies:</span>
											<span class="font-medium">{book.totalCopies || 0}</span>
										</div>
										<div class="flex justify-between text-sm">
											<span class="text-gray-600">Available:</span>
											<span class="font-medium text-green-600">{book.availableCopies || 0}</span>
										</div>
										<div class="flex justify-between text-sm">
											<span class="text-gray-600">Borrowed:</span>
											<span class="font-medium text-orange-600">{book.borrowedCopies || 0}</span>
										</div>
										<div class="flex justify-between text-sm">
											<span class="text-gray-600">Reserved:</span>
											<span class="font-medium text-blue-600">{book.reservedCopies || 0}</span>
										</div>
									</div>

									<Button
										onclick={() => goto(`/admin/library/manage-copies/${book.id}`)}
										class="w-full"
										variant="outline"
									>
										<Settings class="mr-2 h-4 w-4" />
										Manage Copies
									</Button>
								</CardContent>
							</Card>
						{/each}
					</div>
				{/if}
			</CardContent>
		</Card>
	</div>
</div>
