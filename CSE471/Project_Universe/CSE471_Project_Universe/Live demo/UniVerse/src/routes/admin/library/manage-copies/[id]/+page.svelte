<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { Button } from '$lib/components/ui/button';
	import { Input } from '$lib/components/ui/input';
	import { Label } from '$lib/components/ui/label';
	import {
		Card,
		CardContent,
		CardDescription,
		CardHeader,
		CardTitle
	} from '$lib/components/ui/card';
	import { ArrowLeft, Plus, Edit, Trash2, Save, X } from '@lucide/svelte';
	import type { Book } from '$lib/types/book';

	// Define BookCopy type locally
	interface BookCopy {
		id: string;
		book_id: string;
		status: string;
		is_available: boolean;
		created_at: string;
		updated_at?: string;
	}

	let { data, params } = $props();

	let book = $state<Book | null>(data.book || null);
	let copies = $state<BookCopy[]>(data.copies || []);
	let loading = $state(false);
	let message = $state('');
	let messageType = $state<'success' | 'error'>('success');

	// Copy management states
	let editingCopy = $state<string | null>(null);
	let copyFormData = $state<any>({
		status: 'available',
		is_available: true
	});

	onMount(() => {
		// If server-side data failed, try client-side loading
		if (!book && !data.error) {
			loadBookAndCopies();
		} else if (data.error) {
			showMessage(data.error, 'error');
		}
	});

	async function loadBookAndCopies() {
		loading = true;
		console.log('Loading book and copies for ID:', params.id);

		try {
			// Load book details
			console.log('Fetching book details...');
			const bookResponse = await fetch(`/api/admin/books/${params.id}`);
			console.log('Book response status:', bookResponse.status);

			if (!bookResponse.ok) {
				throw new Error(`HTTP ${bookResponse.status}: ${bookResponse.statusText}`);
			}

			const bookResult = await bookResponse.json();
			console.log('Book result:', bookResult);

			if (bookResult.success) {
				book = bookResult.book;
				console.log('Book loaded successfully:', book);
			} else {
				showMessage('Failed to load book: ' + bookResult.error, 'error');
				return;
			}

			// Load book copies
			console.log('Fetching book copies...');
			const copiesResponse = await fetch(`/api/admin/books/${params.id}/copies`);
			console.log('Copies response status:', copiesResponse.status);

			if (!copiesResponse.ok) {
				throw new Error(`HTTP ${copiesResponse.status}: ${copiesResponse.statusText}`);
			}

			const copiesResult = await copiesResponse.json();
			console.log('Copies result:', copiesResult);

			if (copiesResult.success) {
				copies = copiesResult.copies;
				console.log('Copies loaded successfully:', copies);
			} else {
				showMessage('Failed to load copies: ' + copiesResult.error, 'error');
			}
		} catch (error) {
			console.error('Error loading data:', error);
			showMessage('Error loading data: ' + error, 'error');
		} finally {
			loading = false;
		}
	}

	function startEditCopy(copy: BookCopy) {
		editingCopy = copy.id;
		copyFormData = {
			status: copy.status,
			is_available: copy.is_available
		};
	}

	function cancelEdit() {
		editingCopy = null;
		copyFormData = {
			status: 'available',
			is_available: true
		};
	}

	async function saveCopy(copyId: string) {
		try {
			const response = await fetch(`/api/admin/books/${params.id}/copies/${copyId}`, {
				method: 'PUT',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify(copyFormData)
			});

			const result = await response.json();

			if (result.success) {
				showMessage('Copy updated successfully!', 'success');
				editingCopy = null;
				await loadBookAndCopies(); // Reload data
			} else {
				showMessage('Failed to update copy: ' + result.error, 'error');
			}
		} catch (error) {
			showMessage('Error updating copy: ' + error, 'error');
		}
	}

	async function deleteCopy(copyId: string) {
		if (!confirm('Are you sure you want to delete this copy? This action cannot be undone.')) {
			return;
		}

		try {
			const response = await fetch(`/api/admin/books/${params.id}/copies/${copyId}`, {
				method: 'DELETE'
			});

			const result = await response.json();

			if (result.success) {
				showMessage('Copy deleted successfully!', 'success');
				await loadBookAndCopies(); // Reload data
			} else {
				showMessage('Failed to delete copy: ' + result.error, 'error');
			}
		} catch (error) {
			showMessage('Error deleting copy: ' + error, 'error');
		}
	}

	async function addNewCopy() {
		try {
			const response = await fetch(`/api/admin/books/${params.id}/copies`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					status: 'available',
					is_available: true
				})
			});

			const result = await response.json();

			if (result.success) {
				showMessage('New copy added successfully!', 'success');
				await loadBookAndCopies(); // Reload data
			} else {
				showMessage('Failed to add copy: ' + result.error, 'error');
			}
		} catch (error) {
			showMessage('Error adding copy: ' + error, 'error');
		}
	}

	function showMessage(msg: string, type: 'success' | 'error') {
		message = msg;
		messageType = type;
		setTimeout(() => {
			message = '';
		}, 5000);
	}

	function getStatusColor(status: string) {
		switch (status) {
			case 'available':
				return 'bg-green-100 text-green-800 border-green-200';
			case 'borrowed':
				return 'bg-orange-100 text-orange-800 border-orange-200';
			case 'reserved':
				return 'bg-blue-100 text-blue-800 border-blue-200';
			default:
				return 'bg-gray-100 text-gray-800 border-gray-200';
		}
	}

	function getStatusIcon(status: string) {
		switch (status) {
			case 'available':
				return '✅';
			case 'borrowed':
				return '📖';
			case 'reserved':
				return '🔒';
			default:
				return '❓';
		}
	}
</script>

<div class="container mx-auto max-w-6xl p-6">
	<!-- Header -->
	<div class="mb-8">
		<div class="flex items-center justify-between">
			<div class="flex items-center gap-4">
				<button
					onclick={() => goto('/admin/library')}
					class="flex items-center rounded-md border border-gray-300 px-3 py-2"
				>
					<ArrowLeft class="mr-2 h-4 w-4" />
					Back to Books
				</button>

				<div>
					<h1 class="text-3xl font-bold text-foreground">Manage Book Copies</h1>
					{#if book}
						<p class="mt-2 text-muted-foreground">
							Managing copies for "{book.title}" by {book.author}
						</p>
					{/if}
				</div>
			</div>

			<button
				onclick={addNewCopy}
				class="flex items-center rounded-md bg-green-600 px-4 py-2 text-white hover:bg-green-700"
			>
				<Plus class="mr-2 h-4 w-4" />
				Add New Copy
			</button>
		</div>
	</div>

	<!-- Message Alert -->
	{#if message}
		<div
			class={`mb-6 rounded-md border p-4 ${
				messageType === 'success'
					? 'border-green-500 bg-green-50 text-green-700'
					: 'border-red-500 bg-red-50 text-red-700'
			}`}
		>
			{message}
		</div>
	{/if}

	<!-- Book Summary -->
	{#if book}
		<Card class="mb-6">
			<CardHeader>
				<CardTitle>Book Information</CardTitle>
			</CardHeader>
			<CardContent>
				<div class="flex items-start gap-6">
					<!-- Book Cover -->
					{#if book.image_url}
						<div class="flex-shrink-0">
							<img
								src={book.image_url}
								alt="Cover of {book.title}"
								class="h-40 w-32 rounded-lg border object-cover shadow-sm"
							/>
						</div>
					{:else}
						<div
							class="flex h-40 w-32 flex-shrink-0 items-center justify-center rounded-lg border bg-gray-100"
						>
							<span class="text-4xl text-gray-400">📚</span>
						</div>
					{/if}

					<!-- Book Details -->
					<div class="flex-1">
						<h3 class="mb-2 text-xl font-bold">{book.title}</h3>
						<p class="mb-3 text-muted-foreground">by {book.author}</p>

						<div class="grid grid-cols-2 gap-4 text-sm md:grid-cols-4">
							<div>
								<span class="text-muted-foreground">ISBN:</span>
								<span class="ml-2 font-medium">{book.isbn}</span>
							</div>
							<div>
								<span class="text-muted-foreground">Category:</span>
								<span class="ml-2 font-medium">{book.category}</span>
							</div>
							<div>
								<span class="text-muted-foreground">Year:</span>
								<span class="ml-2 font-medium">{book.published_year}</span>
							</div>
							<div>
								<span class="text-muted-foreground">Location:</span>
								<span class="ml-2 font-medium">{book.location}</span>
							</div>
						</div>
					</div>
				</div>
			</CardContent>
		</Card>
	{/if}

	<!-- Copies Management -->
	<Card>
		<CardHeader>
			<CardTitle>Book Copies ({copies.length})</CardTitle>
			<CardDescription
				>Manage individual copies of this book. You can edit status, availability, or delete copies.</CardDescription
			>
		</CardHeader>
		<CardContent>
			{#if loading}
				<div class="flex items-center justify-center py-12">
					<span class="mr-2 animate-spin text-2xl text-blue-600">⏳</span>
					<span class="text-muted-foreground">Loading copies...</span>
				</div>
			{:else if copies.length === 0}
				<div class="py-12 text-center">
					<span class="mb-4 block text-4xl text-muted-foreground">📚</span>
					<h3 class="mb-2 text-lg font-semibold text-muted-foreground">No copies found</h3>
					<p class="mb-4 text-muted-foreground">This book doesn't have any copies yet.</p>
					<button
						onclick={addNewCopy}
						class="rounded-lg bg-green-600 px-6 py-3 text-white hover:bg-green-700"
					>
						<Plus class="mr-2 inline h-4 w-4" />
						Add First Copy
					</button>
				</div>
			{:else}
				<div class="space-y-4">
					{#each copies as copy, index}
						<div class="rounded-lg border border-gray-200 p-4">
							<div class="flex items-center justify-between">
								<div class="flex items-center gap-4">
									<div class="flex h-12 w-12 items-center justify-center rounded-lg bg-blue-100">
										<span class="text-lg font-bold text-blue-600">{index + 1}</span>
									</div>

									<div class="flex items-center gap-3">
										<div
											class={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${getStatusColor(copy.status)}`}
										>
											{getStatusIcon(copy.status)}
											{copy.status}
										</div>

										<span class="text-sm text-muted-foreground">
											ID: {copy.id.slice(0, 8)}...
										</span>
									</div>
								</div>

								<div class="flex gap-2">
									{#if editingCopy === copy.id}
										<!-- Edit Form -->
										<div class="flex items-center gap-2">
											<select
												bind:value={copyFormData.status}
												class="rounded border border-gray-300 px-3 py-1 text-sm"
											>
												<option value="available">Available</option>
												<option value="borrowed">Borrowed</option>
												<option value="reserved">Reserved</option>
											</select>

											<button
												onclick={() => saveCopy(copy.id)}
												class="rounded bg-green-600 px-3 py-1 text-sm text-white hover:bg-green-700"
											>
												<Save class="h-4 w-4" />
											</button>

											<button
												onclick={cancelEdit}
												class="rounded bg-gray-600 px-3 py-1 text-sm text-white hover:bg-gray-700"
											>
												<X class="h-4 w-4" />
											</button>
										</div>
									{:else}
										<!-- Action Buttons -->
										<button
											onclick={() => startEditCopy(copy)}
											class="rounded border border-blue-600 px-3 py-1.5 text-sm text-blue-600 hover:bg-blue-50"
										>
											<Edit class="mr-1 h-4 w-4" />
											Edit
										</button>

										<button
											onclick={() => deleteCopy(copy.id)}
											class="rounded border border-red-600 px-3 py-1.5 text-sm text-red-600 hover:bg-red-50"
										>
											<Trash2 class="mr-1 h-4 w-4" />
											Delete
										</button>
									{/if}
								</div>
							</div>
						</div>
					{/each}
				</div>
			{/if}
		</CardContent>
	</Card>
</div>
