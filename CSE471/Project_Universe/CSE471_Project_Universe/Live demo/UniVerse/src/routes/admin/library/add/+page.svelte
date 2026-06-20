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
	import { BookOpen, Plus, ArrowLeft, Upload, X, CheckCircle, AlertCircle } from '@lucide/svelte';

	let { data } = $props();

	let formData = $state({
		title: '',
		author: '',
		isbn: '',
		category: '',
		published_year: '',
		location: '',
		status: 'available',
		quantity: 1,
		image_url: ''
	});

	let selectedFile = $state<File | null>(null);
	let coverPreview = $state<string>('');
	let loading = $state(false);
	let message = $state('');
	let messageType = $state<'success' | 'error'>('success');

	const categories = [
		'Fiction',
		'Non-Fiction',
		'Science',
		'Technology',
		'History',
		'Philosophy',
		'Literature',
		'Mathematics',
		'Computer Science',
		'Art',
		'Music',
		'Sports',
		'Travel',
		'Biography',
		'Self-Help'
	];

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
		}
	}

	function removeImage() {
		selectedFile = null;
		coverPreview = '';
		formData.image_url = '';
	}

	async function handleSubmit() {
		if (!formData.title || !formData.author || !formData.isbn) {
			showMessage('Please fill in all required fields', 'error');
			return;
		}

		loading = true;
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
				// No image selected, submit directly
				await submitForm();
			}
		} catch (error) {
			showMessage('Error processing image: ' + error, 'error');
			loading = false;
		}
	}

	async function submitForm() {
		try {
			const response = await fetch('/api/admin/books', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify(formData)
			});

			const result = await response.json();

			if (result.success) {
				showMessage(result.message, 'success');
				resetForm();
				setTimeout(() => {
					goto('/admin/library');
				}, 2000);
			} else {
				showMessage('Failed to add book: ' + result.error, 'error');
			}
		} catch (error) {
			showMessage('Error adding book: ' + error, 'error');
		} finally {
			loading = false;
		}
	}

	function resetForm() {
		formData = {
			title: '',
			author: '',
			isbn: '',
			category: '',
			published_year: '',
			location: '',
			status: 'available',
			quantity: 1,
			image_url: ''
		};
		selectedFile = null;
		coverPreview = '';
	}

	function showMessage(msg: string, type: 'success' | 'error') {
		message = msg;
		messageType = type;
		setTimeout(() => {
			message = '';
		}, 5000);
	}
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
				<span class="font-medium text-gray-900">Add New Book</span>
			</div>

			<div class="flex flex-col gap-6 lg:flex-row lg:items-center lg:justify-between">
				<div>
					<div class="mb-4 flex items-center gap-4">
						<Button onclick={() => goto('/admin/library')} variant="outline" size="sm">
							<ArrowLeft class="mr-2 h-4 w-4" />
							Back to Library
						</Button>
					</div>
					<h1 class="text-3xl font-bold text-gray-900 sm:text-4xl">Add New Book</h1>
					<p class="mt-2 text-lg text-gray-600">Expand your library collection with new books</p>
				</div>

				<div class="flex items-center gap-3">
					<div class="rounded-lg border border-blue-200 bg-blue-50 px-3 py-1">
						<span class="text-sm font-medium text-blue-700"> Book Management </span>
					</div>
				</div>
			</div>
		</div>
	</div>

	<!-- Main Content -->
	<div class="mx-auto max-w-4xl px-6 py-8">
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

		<!-- Form Card -->
		<Card class="border-0 bg-white/80 shadow-xl backdrop-blur-sm">
			<CardHeader class="pb-8 text-center">
				<div
					class="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-gradient-to-br from-blue-500 to-indigo-600"
				>
					<Plus class="h-8 w-8 text-white" />
				</div>
				<CardTitle class="text-2xl text-gray-900">Book Information</CardTitle>
				<CardDescription class="text-lg text-gray-600">
					Enter the details for the new book to add to your library
				</CardDescription>
			</CardHeader>

			<CardContent class="p-8">
				<form
					onsubmit={(e: SubmitEvent) => {
						e.preventDefault();
						handleSubmit();
					}}
					class="space-y-8"
				>
					<!-- Image Upload Section -->
					<div class="space-y-4">
						<Label for="cover" class="text-base font-semibold text-gray-700">Book Cover Image</Label
						>
						<div class="flex items-center gap-6">
							<div class="flex-1">
								<div class="relative">
									<Input
										id="cover"
										type="file"
										accept="image/*"
										onchange={handleFileChange}
										class="cursor-pointer border-2 border-dashed border-gray-300 transition-colors hover:border-blue-400"
									/>
									<div
										class="pointer-events-none absolute inset-0 flex items-center justify-center"
									>
										<div class="text-center">
											<Upload class="mx-auto mb-2 h-6 w-6 text-gray-400" />
											<p class="text-sm text-gray-500">Click to upload cover image</p>
										</div>
									</div>
								</div>
								<p class="mt-2 text-sm text-gray-500">
									Upload a cover image (JPG, PNG, GIF). Max size: 5MB
								</p>
							</div>

							{#if coverPreview}
								<div class="relative">
									<img
										src={coverPreview}
										alt="Cover preview"
										class="h-32 w-24 rounded-lg border-2 border-gray-200 object-cover shadow-md"
									/>
									<Button
										type="button"
										onclick={removeImage}
										size="sm"
										variant="outline"
										class="absolute -top-2 -right-2 h-7 w-7 rounded-full border-red-300 bg-white p-0 text-red-600 hover:bg-red-50"
										title="Remove image"
									>
										<X class="h-4 w-4" />
									</Button>
								</div>
							{/if}
						</div>
					</div>

					<Separator />

					<!-- Basic Information -->
					<div class="space-y-6">
						<h3 class="flex items-center gap-2 text-lg font-semibold text-gray-900">
							<BookOpen class="h-5 w-5 text-blue-600" />
							Basic Information
						</h3>

						<div class="grid grid-cols-1 gap-6 md:grid-cols-2">
							<div class="space-y-2">
								<Label for="title" class="text-sm font-medium text-gray-700">Title *</Label>
								<Input
									id="title"
									bind:value={formData.title}
									placeholder="Enter book title"
									required
									class="border-gray-300 focus:border-blue-500 focus:ring-blue-500"
								/>
							</div>

							<div class="space-y-2">
								<Label for="author" class="text-sm font-medium text-gray-700">Author *</Label>
								<Input
									id="author"
									bind:value={formData.author}
									placeholder="Enter author name"
									required
									class="border-gray-300 focus:border-blue-500 focus:ring-blue-500"
								/>
							</div>

							<div class="space-y-2">
								<Label for="isbn" class="text-sm font-medium text-gray-700">ISBN *</Label>
								<Input
									id="isbn"
									bind:value={formData.isbn}
									placeholder="Enter ISBN"
									required
									class="border-gray-300 focus:border-blue-500 focus:ring-blue-500"
								/>
							</div>

							<div class="space-y-2">
								<Label for="category" class="text-sm font-medium text-gray-700">Category</Label>
								<select
									id="category"
									bind:value={formData.category}
									class="w-full rounded-md border border-gray-300 px-3 py-2 focus:border-blue-500 focus:ring-2 focus:ring-blue-500 focus:outline-none"
								>
									<option value="">Select a category</option>
									{#each categories as category}
										<option value={category}>{category}</option>
									{/each}
								</select>
							</div>

							<div class="space-y-2">
								<Label for="published_year" class="text-sm font-medium text-gray-700"
									>Published Year</Label
								>
								<Input
									id="published_year"
									type="number"
									bind:value={formData.published_year}
									placeholder="e.g., 2024"
									min="1800"
									max="2030"
									class="border-gray-300 focus:border-blue-500 focus:ring-blue-500"
								/>
							</div>

							<div class="space-y-2">
								<Label for="location" class="text-sm font-medium text-gray-700">Location</Label>
								<Input
									id="location"
									bind:value={formData.location}
									placeholder="e.g., Shelf A1, Section B"
									class="border-gray-300 focus:border-blue-500 focus:ring-blue-500"
								/>
							</div>

							<div class="space-y-2">
								<Label for="status" class="text-sm font-medium text-gray-700">Status</Label>
								<select
									id="status"
									bind:value={formData.status}
									class="w-full rounded-md border border-gray-300 px-3 py-2 focus:border-blue-500 focus:ring-2 focus:ring-blue-500 focus:outline-none"
								>
									<option value="available">Available</option>
									<option value="borrowed">Borrowed</option>
									<option value="reserved">Reserved</option>
								</select>
								<p class="mt-1 flex items-center gap-1 text-sm text-amber-600">
									<AlertCircle class="h-4 w-4" />
									This status will apply to ALL copies of this book
								</p>
							</div>

							<div class="space-y-2">
								<Label for="quantity" class="text-sm font-medium text-gray-700">Quantity</Label>
								<Input
									id="quantity"
									type="number"
									bind:value={formData.quantity}
									placeholder="Number of copies"
									min="1"
									max="100"
									class="border-gray-300 focus:border-blue-500 focus:ring-blue-500"
								/>
							</div>
						</div>
					</div>

					<Separator />

					<!-- Submit Buttons -->
					<div class="flex flex-col justify-end gap-4 sm:flex-row">
						<Button type="button" onclick={resetForm} variant="outline" class="px-6 py-3">
							Reset Form
						</Button>

						<Button
							type="submit"
							disabled={loading}
							class="bg-gradient-to-r from-blue-600 to-indigo-600 px-8 py-3 text-white shadow-lg hover:from-blue-700 hover:to-indigo-700"
						>
							{#if loading}
								<div class="mr-2 h-4 w-4 animate-spin rounded-full border-b-2 border-white"></div>
							{/if}
							<Plus class="mr-2 h-4 w-4" />
							{loading ? 'Adding Book...' : 'Add Book'}
						</Button>
					</div>
				</form>
			</CardContent>
		</Card>
	</div>
</div>
