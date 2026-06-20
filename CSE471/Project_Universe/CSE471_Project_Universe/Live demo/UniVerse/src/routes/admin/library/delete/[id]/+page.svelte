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
	import { ArrowLeft, Trash2, AlertTriangle } from '@lucide/svelte';
	import type { Book } from '$lib/types/book';
	import type { BookCopy } from '$lib/types/book';

	let { data, params } = $props();

	let book = $state<Book | null>(null);
	let availableCopies = $state<BookCopy[]>([]);
	let copiesToDelete = $state<number>(1);
	let loading = $state(false);
	let deleting = $state(false);
	let message = $state('');
	let messageType = $state<'success' | 'error'>('success');

	onMount(() => {
		loadBookAndCopies();
	});

	// Refresh data when page loads to ensure fresh data
	$effect(() => {
		// This will run when the component mounts or when dependencies change
		if (!book && !loading) {
			loadBookAndCopies();
		}
	});

	async function loadBookAndCopies() {
		loading = true;
		try {
			// Load book details with timestamp to ensure fresh data
			const bookResponse = await fetch(`/api/admin/books/${params.id}?t=${Date.now()}`);
			const bookResult = await bookResponse.json();

			if (bookResult.success) {
				book = bookResult.book;
			} else {
				showMessage('Failed to load book: ' + bookResult.error, 'error');
				return;
			}

			// Load available copies with timestamp to ensure fresh data
			const copiesResponse = await fetch(`/api/admin/books/${params.id}/copies?t=${Date.now()}`);
			const copiesResult = await copiesResponse.json();

			if (copiesResult.success) {
				console.log('All copies loaded:', copiesResult.copies);

				// Filter only available copies
				availableCopies = copiesResult.copies.filter(
					(copy: BookCopy) => copy.status === 'available' && copy.is_available === true
				);

				console.log('Available copies after filter:', availableCopies);
				console.log('Filter criteria: status === "available" && is_available === true');

				// Set default copies to delete (max 5, or all available if less than 5)
				copiesToDelete = Math.min(5, availableCopies.length);
			} else {
				showMessage('Failed to load book copies: ' + copiesResult.error, 'error');
			}
		} catch (error) {
			showMessage('Error loading book data: ' + error, 'error');
		} finally {
			loading = false;
		}
	}

	async function confirmDelete() {
		if (!book || availableCopies.length === 0) return;

		deleting = true;
		try {
			// Delete the specified number of available copies
			const copiesToDeleteArray = availableCopies.slice(0, copiesToDelete);

			for (const copy of copiesToDeleteArray) {
				const response = await fetch(`/api/admin/books/${book.id}/copies/${copy.id}`, {
					method: 'DELETE'
				});

				const result = await response.json();

				if (!result.success) {
					showMessage('Failed to delete copy: ' + result.error, 'error');
					return;
				}
			}

			showMessage(`Successfully deleted ${copiesToDelete} copy(ies)!`, 'success');
			setTimeout(() => {
				goto('/admin/library/delete');
			}, 2000);
		} catch (error) {
			showMessage('Error deleting copies: ' + error, 'error');
		} finally {
			deleting = false;
		}
	}

	function showMessage(msg: string, type: 'success' | 'error') {
		message = msg;
		messageType = type;
		setTimeout(() => {
			message = '';
		}, 5000);
	}
</script>

<div class="container mx-auto max-w-4xl p-6">
	<!-- Header -->
	<div class="mb-8">
		<div class="flex items-center justify-between">
			<div class="flex items-center gap-3">
				<Trash2 class="h-8 w-8 text-red-500" />
				<h1 class="text-3xl font-bold text-foreground">Delete Book Copies</h1>
			</div>

			<Button variant="outline" onclick={() => goto('/admin/library')}>
				<ArrowLeft class="mr-2 h-4 w-4" />
				Back to Books
			</Button>
		</div>

		{#if book}
			<p class="mt-2 text-muted-foreground">
				Select how many available copies of "{book.title}" by {book.author} to delete
			</p>
		{/if}
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

	{#if loading}
		<!-- Loading -->
		<div class="flex items-center justify-center py-12">
			<div class="h-8 w-8 animate-spin rounded-full border-b-2 border-red-600"></div>
			<span class="ml-2 text-muted-foreground">Loading book...</span>
		</div>
	{:else if book}
		<!-- Delete Confirmation -->
		<Card>
			<CardHeader>
				<CardTitle class="text-red-600">⚠️ Delete Book Copies Confirmation</CardTitle>
				<CardDescription
					>Select how many available copies you want to delete. This action cannot be undone.</CardDescription
				>
			</CardHeader>
			<CardContent>
				<!-- Book Information -->
				<div class="mb-6 rounded-lg border border-gray-200 bg-gray-50 p-4">
					<div class="mb-4 flex items-start gap-6">
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
							<h3 class="mb-3 text-xl font-bold">{book.title}</h3>
							<p class="mb-4 text-muted-foreground">by {book.author}</p>

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

					<!-- Copy Information -->
					<div class="mt-4 rounded border border-blue-200 bg-blue-50 p-3">
						<div class="text-center">
							<span class="text-lg font-semibold text-blue-600"
								>{book.totalCopies || 0} Total Copies</span
							>
							<div class="mt-2 grid grid-cols-3 gap-4 text-sm">
								<div>
									<span class="font-semibold text-green-600">{book.availableCopies || 0}</span>
									<p class="text-xs text-muted-foreground">Available</p>
								</div>
								<div>
									<span class="font-semibold text-orange-600">{book.borrowedCopies || 0}</span>
									<p class="text-xs text-muted-foreground">Borrowed</p>
								</div>
								<div>
									<span class="font-semibold text-blue-600">{book.reservedCopies || 0}</span>
									<p class="text-xs text-muted-foreground">Reserved</p>
								</div>
							</div>
						</div>
					</div>

					<!-- Available Copies for Deletion -->
					{#if availableCopies.length > 0}
						<div class="mt-4 rounded border border-green-200 bg-green-50 p-4">
							<h4 class="mb-3 font-semibold text-green-800">📚 Available Copies for Deletion</h4>
							<p class="mb-3 text-sm text-green-700">
								You can delete up to <span class="font-semibold">{availableCopies.length}</span> available
								copies.
							</p>

							<div class="flex items-center gap-3">
								<label for="copiesToDelete" class="text-sm font-medium text-green-800">
									Copies to delete:
								</label>
								<select
									id="copiesToDelete"
									bind:value={copiesToDelete}
									class="rounded border border-green-300 bg-white px-3 py-1 text-sm"
								>
									{#each Array.from({ length: Math.min(availableCopies.length, 10) }, (_, index) => index + 1) as copyNumber}
										<option value={copyNumber}>{copyNumber}</option>
									{/each}
								</select>
								<span class="text-sm text-green-700">
									out of {availableCopies.length} available
								</span>
							</div>

							<div class="mt-3 text-xs text-green-600">
								<p>
									⚠️ Only available copies can be deleted. Borrowed and reserved copies are
									protected.
								</p>
							</div>
						</div>
					{:else}
						<div class="mt-4 rounded border border-red-200 bg-red-50 p-4">
							<h4 class="mb-2 font-semibold text-red-800">❌ No Copies Available for Deletion</h4>
							<p class="text-sm text-red-700">
								All copies are either borrowed or reserved. You cannot delete any copies at this
								time.
							</p>
						</div>
					{/if}
				</div>

				<!-- Warning -->
				<div class="mb-6 rounded-md border border-red-200 bg-red-50 p-4">
					<div class="flex items-center gap-2">
						<AlertTriangle class="h-5 w-5 text-red-600" />
						<span class="text-sm font-medium text-red-800"
							>Warning: This action will permanently delete:</span
						>
					</div>
					<ul class="mt-2 list-inside list-disc space-y-1 text-sm text-red-700">
						<li>{copiesToDelete} available copy(ies) of this book</li>
						<li>The book record will remain intact</li>
						<li>Borrowed and reserved copies are protected and cannot be deleted</li>
					</ul>
				</div>

				<!-- Action Buttons -->
				<div class="flex gap-4 pt-6">
					{#if availableCopies.length > 0}
						<Button onclick={confirmDelete} disabled={deleting} class="bg-red-600 hover:bg-red-700">
							{#if deleting}
								<div class="mr-2 h-4 w-4 animate-spin rounded-full border-b-2 border-white"></div>
							{/if}
							<Trash2 class="mr-2 h-4 w-4" />
							{deleting ? 'Deleting...' : `Delete ${copiesToDelete} Copy(ies)`}
						</Button>
					{/if}

					<Button type="button" variant="outline" onclick={() => goto('/admin/library')}>
						Cancel
					</Button>
				</div>
			</CardContent>
		</Card>
	{:else}
		<!-- Book Not Found -->
		<Card>
			<CardContent class="p-12 text-center">
				<Trash2 class="mx-auto mb-4 h-16 w-16 text-muted-foreground" />
				<h3 class="mb-2 text-lg font-semibold text-muted-foreground">Book not found</h3>
				<p class="text-muted-foreground">
					The book you're trying to delete doesn't exist or has been removed.
				</p>
				<Button onclick={() => goto('/admin/library')} class="mt-4">Back to Books</Button>
			</CardContent>
		</Card>
	{/if}
</div>
