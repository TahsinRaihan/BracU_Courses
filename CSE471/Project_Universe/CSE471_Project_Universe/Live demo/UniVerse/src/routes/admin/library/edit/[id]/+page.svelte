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
	import { ArrowLeft, Save, X, BookOpen, AlertTriangle, CheckCircle } from '@lucide/svelte';

	let { data, params } = $props();

	let book = $state<any>(null);
	let formData = $state<any>({
		title: '',
		author: '',
		isbn: '',
		category: '',
		published_year: '',
		location: '',
		status: 'available',
		image_url: ''
	});

	let loading = $state(false);
	let saving = $state(false);
	let message = $state('');
	let messageType = $state('success');
	let hasChanges = $state(false);
	let selectedFile = $state<File | null>(null);
	let coverPreview = $state<string>('');

	// Track changes using $effect instead of legacy $:
	$effect(() => {
		if (book) {
			hasChanges =
				JSON.stringify(formData) !==
				JSON.stringify({
					title: book.title,
					author: book.author,
					isbn: book.isbn,
					category: book.category,
					published_year: book.published_year || '',
					location: book.location,
					status: book.status || 'available'
				});
		}
	});

	onMount(() => {
		loadBook();
	});

	async function loadBook() {
		loading = true;
		try {
			const response = await fetch(`/api/admin/books/${params.id}`);
			const result = await response.json();

			if (result.success) {
				book = result.book;
				formData = {
					title: book.title,
					author: book.author,
					isbn: book.isbn,
					category: book.category,
					published_year: book.published_year || '',
					location: book.location,
					status: book.status || 'available',
					image_url: book.image_url || ''
				};
				coverPreview = book.image_url || '';
			} else {
				showMessage('Failed to load book: ' + result.error, 'error');
			}
		} catch (error) {
			showMessage('Error loading book: ' + error, 'error');
		} finally {
			loading = false;
		}
	}

	function handleFileChange(e: Event) {
		const target = e.target as HTMLInputElement;
		if (target.files && target.files[0]) {
			const file = target.files[0];
			selectedFile = file;

			// Create preview
			const reader = new FileReader();
			reader.onload = (e: ProgressEvent<FileReader>) => {
				if (e.target?.result) {
					coverPreview = e.target.result as string;
				}
			};
			reader.readAsDataURL(file);
			hasChanges = true;
		}
	}

	function removeImage() {
		selectedFile = null;
		coverPreview = '';
		formData.image_url = '';
		hasChanges = true;
	}

	async function handleSubmit() {
		if (!validateForm()) return;

		saving = true;
		try {
			// If there's a selected file, convert it to base64
			if (selectedFile) {
				const reader = new FileReader();
				reader.onload = (e: ProgressEvent<FileReader>) => {
					if (e.target?.result) {
						formData.image_url = e.target.result as string;
						submitForm();
					}
				};
				reader.readAsDataURL(selectedFile);
			} else {
				// No new image selected, submit directly
				await submitForm();
			}
		} catch (error) {
			showMessage('Error processing image: ' + error, 'error');
			saving = false;
		}
	}

	async function submitForm() {
		try {
			const response = await fetch(`/api/admin/books/${params.id}`, {
				method: 'PUT',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify(formData)
			});

			const result = await response.json();

			if (result.success) {
				showMessage('Book updated successfully!', 'success');
				hasChanges = false;
				// Reload book data
				await loadBook();
			} else {
				showMessage('Failed to update book: ' + result.error, 'error');
			}
		} catch (error) {
			showMessage('Error updating book: ' + error, 'error');
		} finally {
			saving = false;
		}
	}

	function validateForm() {
		if (!formData.title.trim()) {
			showMessage('Title is required', 'error');
			return false;
		}
		if (!formData.author.trim()) {
			showMessage('Author is required', 'error');
			return false;
		}
		if (!formData.isbn.trim()) {
			showMessage('ISBN is required', 'error');
			return false;
		}
		if (!formData.category.trim()) {
			showMessage('Category is required', 'error');
			return false;
		}
		if (!formData.location.trim()) {
			showMessage('Location is required', 'error');
			return false;
		}
		return true;
	}

	function resetForm() {
		if (book) {
			formData = {
				title: book.title,
				author: book.author,
				isbn: book.isbn,
				category: book.category,
				published_year: book.published_year || '',
				location: book.location,
				status: book.status || 'available'
			};
			hasChanges = false;
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
				<BookOpen class="h-8 w-8 text-blue-500" />
				<h1 class="text-3xl font-bold text-foreground">Edit Book</h1>
			</div>

			<Button variant="outline" onclick={() => goto('/admin/library')}>
				<ArrowLeft class="mr-2 h-4 w-4" />
				Back to Books
			</Button>
		</div>

		{#if book}
			<p class="mt-2 text-muted-foreground">Editing "{book.title}" by {book.author}</p>
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
			<div class="h-8 w-8 animate-spin rounded-full border-b-2 border-blue-600"></div>
			<span class="ml-2 text-muted-foreground">Loading book...</span>
		</div>
	{:else if book}
		<!-- Edit Form -->
		<Card>
			<CardHeader>
				<CardTitle>Book Information</CardTitle>
				<CardDescription>Update the book details below</CardDescription>
			</CardHeader>
			<CardContent>
				<form
					onsubmit={(e: SubmitEvent) => {
						e.preventDefault();
						handleSubmit();
					}}
					class="space-y-6"
				>
					<!-- Image Upload Section -->
					<div class="space-y-4">
						<Label for="cover">Book Cover Image</Label>
						<div class="flex items-center gap-4">
							<div class="flex-1">
								<Input
									id="cover"
									type="file"
									accept="image/*"
									onchange={handleFileChange}
									class="cursor-pointer"
								/>
								<p class="mt-1 text-sm text-muted-foreground">
									Upload a new cover image (JPG, PNG, GIF). Max size: 5MB
								</p>
							</div>

							{#if coverPreview}
								<div class="relative">
									<img
										src={coverPreview}
										alt="Cover preview"
										class="h-28 w-20 rounded border object-cover"
									/>
									<button
										type="button"
										onclick={removeImage}
										class="absolute -top-2 -right-2 flex h-6 w-6 items-center justify-center rounded-full bg-red-500 text-xs text-white hover:bg-red-600"
										title="Remove image"
									>
										×
									</button>
								</div>
							{/if}
						</div>
					</div>

					<div class="grid grid-cols-1 gap-6 md:grid-cols-2">
						<div class="space-y-2">
							<Label for="title">Title *</Label>
							<Input
								id="title"
								bind:value={formData.title}
								placeholder="Enter book title"
								required
							/>
						</div>

						<div class="space-y-2">
							<Label for="author">Author *</Label>
							<Input
								id="author"
								bind:value={formData.author}
								placeholder="Enter author name"
								required
							/>
						</div>

						<div class="space-y-2">
							<Label for="isbn">ISBN *</Label>
							<Input id="isbn" bind:value={formData.isbn} placeholder="Enter ISBN" required />
						</div>

						<div class="space-y-2">
							<Label for="category">Category *</Label>
							<Input
								id="category"
								bind:value={formData.category}
								placeholder="Enter category"
								required
							/>
						</div>

						<div class="space-y-2">
							<Label for="published_year">Published Year</Label>
							<Input
								id="published_year"
								type="number"
								bind:value={formData.published_year}
								placeholder="Enter published year"
								min="1000"
								max="2030"
							/>
						</div>

						<div class="space-y-2">
							<Label for="location">Location *</Label>
							<Input
								id="location"
								bind:value={formData.location}
								placeholder="Enter shelf location"
								required
							/>
						</div>
					</div>

					<div class="space-y-2">
						<Label for="status">Status *</Label>
						<select
							id="status"
							bind:value={formData.status}
							class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 focus-visible:outline-none disabled:cursor-not-allowed disabled:opacity-50"
						>
							<option value="available">Available</option>
							<option value="borrowed">Borrowed</option>
							<option value="reserved">Reserved</option>
						</select>
						<p class="mt-1 text-sm text-amber-600">
							⚠️ Changing status will apply to ALL copies of this book
						</p>
					</div>

					<!-- Form Actions -->
					<div class="flex gap-4 pt-6">
						<Button
							type="submit"
							disabled={saving || !hasChanges}
							class="bg-blue-600 hover:bg-blue-700"
						>
							{#if saving}
								<div class="mr-2 h-4 w-4 animate-spin rounded-full border-b-2 border-white"></div>
							{/if}
							<Save class="mr-2 h-4 w-4" />
							{saving ? 'Saving...' : 'Save Changes'}
						</Button>

						<Button type="button" variant="outline" onclick={resetForm} disabled={!hasChanges}>
							<X class="mr-2 h-4 w-4" />
							Reset
						</Button>

						<Button type="button" variant="outline" onclick={() => goto('/admin/library')}>
							<X class="mr-2 h-4 w-4" />
							Cancel
						</Button>
					</div>
				</form>

				<!-- Status Change Warning -->
				<div class="mt-6 rounded-md border border-amber-200 bg-amber-50 p-4">
					<div class="flex items-start gap-3">
						<AlertTriangle class="mt-0.5 h-5 w-5 text-amber-600" />
						<div>
							<h4 class="mb-1 font-medium text-amber-800">Status Change Affects All Copies</h4>
							<p class="text-sm text-amber-700">
								When you change the book status, it will automatically update ALL copies of this
								book to match the new status. This ensures consistency across your library system.
							</p>
							<ul class="mt-2 list-inside list-disc space-y-1 text-sm text-amber-700">
								<li><strong>Available:</strong> All copies become available for borrowing</li>
								<li><strong>Borrowed:</strong> All copies are marked as borrowed (unavailable)</li>
								<li><strong>Reserved:</strong> All copies are marked as reserved (unavailable)</li>
							</ul>
						</div>
					</div>
				</div>

				<!-- Unsaved Changes Warning -->
				{#if hasChanges}
					<div class="mt-4 rounded-md border border-orange-200 bg-orange-50 p-4">
						<div class="flex items-center gap-2">
							<AlertTriangle class="h-4 w-4 text-orange-600" />
							<span class="text-sm text-orange-800"
								>You have unsaved changes. Make sure to save before leaving this page.</span
							>
						</div>
					</div>
				{/if}
			</CardContent>
		</Card>
	{:else}
		<!-- Book Not Found -->
		<Card>
			<CardContent class="p-12 text-center">
				<BookOpen class="mx-auto mb-4 h-16 w-16 text-muted-foreground" />
				<h3 class="mb-2 text-lg font-semibold text-muted-foreground">Book not found</h3>
				<p class="text-muted-foreground">
					The book you're looking for doesn't exist or has been removed.
				</p>
				<Button onclick={() => goto('/admin/library/edit')} class="mt-4">Back to Books</Button>
			</CardContent>
		</Card>
	{/if}
</div>
