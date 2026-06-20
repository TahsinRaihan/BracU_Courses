<script lang="ts">
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
	import { ArrowLeft, Home } from '@lucide/svelte';
</script>

<svelte:head>
	<title>UniVerse Library - Your Gateway to Knowledge</title>
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
						onclick={() => goto('/myspace')}
						variant="ghost"
						class="flex items-center space-x-2 text-gray-600 hover:bg-gray-100 hover:text-gray-900"
					>
						<Home class="h-4 w-4" />
						<span>Dashboard</span>
					</Button>
				</div>
				<div class="text-sm text-gray-500">UniVerse Library</div>
			</div>
		</div>
	</div>

	<!-- Hero Section -->
	<div class="relative overflow-hidden bg-gradient-to-r from-blue-600 via-purple-600 to-indigo-700">
		<div class="absolute inset-0 bg-black/20"></div>
		<div class="relative mx-auto w-full max-w-7xl px-4 py-16 sm:px-6 sm:py-24 lg:px-8 lg:py-32">
			<div class="text-center">
				<h1 class="text-4xl font-bold tracking-tight text-white sm:text-6xl">
					Welcome to UniVerse Library
				</h1>
				<p class="mx-auto mt-6 max-w-2xl text-xl text-blue-100">
					Discover thousands of books, manage your reading journey, and explore knowledge across all
					disciplines.
				</p>
			</div>
		</div>

		<!-- Decorative elements -->
		<div
			class="absolute top-0 left-0 h-32 w-32 -translate-x-16 -translate-y-16 rounded-full bg-white/10"
		></div>
		<div
			class="absolute right-0 bottom-0 h-40 w-40 translate-x-20 translate-y-20 rounded-full bg-white/10"
		></div>
	</div>

	<!-- Features Section -->
	<div class="mx-auto w-full max-w-7xl px-4 py-16 sm:px-6 sm:py-24 lg:px-8">
		<div class="mb-12 text-center sm:mb-16">
			<h2 class="text-2xl font-bold text-gray-900 sm:text-3xl lg:text-4xl">
				Everything you need for your academic journey
			</h2>
			<p class="mt-4 text-base text-gray-600 sm:text-lg">
				Comprehensive library management system designed for modern education
			</p>
		</div>

		<div class="grid gap-6 sm:gap-8 md:grid-cols-2">
			<!-- Explore Books Feature -->
			<Card
				class="group transform border-0 bg-white/80 backdrop-blur-sm transition-all duration-300 hover:-translate-y-2 hover:shadow-2xl"
			>
				<CardHeader class="pb-4 text-center">
					<div
						class="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-br from-blue-500 to-purple-600 transition-transform duration-300 group-hover:scale-110"
					>
						<span class="text-2xl">📚</span>
					</div>
					<CardTitle class="text-xl text-gray-900">Explore Books</CardTitle>
					<CardDescription class="text-gray-600">
						Explore our extensive collection of books across all subjects and everything
					</CardDescription>
				</CardHeader>
				<CardContent class="text-center">
					<Button
						onclick={() => goto('/library/books')}
						class="w-full border-0 bg-gradient-to-r from-blue-600 to-purple-600 text-white transition-all duration-300 hover:from-blue-700 hover:to-purple-700"
					>
						Start Exploring
					</Button>
				</CardContent>
			</Card>

			<!-- My Library History Feature -->
			<Card
				class="group transform border-0 bg-white/80 backdrop-blur-sm transition-all duration-300 hover:-translate-y-2 hover:shadow-2xl"
			>
				<CardHeader class="pb-4 text-center">
					<div
						class="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-br from-green-500 to-teal-600 transition-transform duration-300 group-hover:scale-110"
					>
						<span class="text-2xl">📋</span>
					</div>
					<CardTitle class="text-xl text-gray-900">My Library History</CardTitle>
					<CardDescription class="text-gray-600">
						Track your borrowings, reservations, and reading progress
					</CardDescription>
				</CardHeader>
				<CardContent class="text-center">
					<Button
						onclick={() => goto('/library/my-account')}
						variant="outline"
						class="w-full border-2 border-green-500 text-green-600 transition-all duration-300 hover:bg-green-500 hover:text-white"
					>
						View History
					</Button>
				</CardContent>
			</Card>
		</div>
	</div>

	<!-- Stats Section -->
	<div class="mx-auto w-full max-w-7xl px-4 py-12 sm:px-6 sm:py-16 lg:px-8">
		<div class="rounded-3xl bg-white p-6 shadow-2xl sm:p-8 lg:p-12">
			<div class="mb-8 text-center sm:mb-12">
				<h2 class="text-2xl font-bold text-gray-900 sm:text-3xl lg:text-4xl">
					Library at a Glance
				</h2>
				<p class="mt-4 text-base text-gray-600 sm:text-lg">
					Discover what makes our library special
				</p>
			</div>

			<div class="grid gap-6 sm:gap-8 md:grid-cols-2 lg:grid-cols-4">
				<div class="text-center">
					<div class="mb-2 text-4xl font-bold text-blue-600">10,000+</div>
					<div class="text-gray-600">Books Available</div>
				</div>
				<div class="text-center">
					<div class="mb-2 text-4xl font-bold text-green-600">24/7</div>
					<div class="text-gray-600">Online Access</div>
				</div>
				<div class="text-center">
					<div class="mb-2 text-4xl font-bold text-purple-600">50+</div>
					<div class="text-gray-600">Subject Categories</div>
				</div>
				<div class="text-center">
					<div class="mb-2 text-4xl font-bold text-orange-600">100%</div>
					<div class="text-gray-600">Digital Ready</div>
				</div>
			</div>
		</div>
	</div>

	<!-- Call to Action -->
	<div class="mx-auto max-w-7xl px-6 py-16">
		<div
			class="rounded-3xl bg-gradient-to-r from-indigo-600 to-purple-600 p-8 text-center text-white md:p-12"
		>
			<h2 class="mb-4 text-3xl font-bold">Ready to start your reading journey?</h2>
			<p class="mb-8 text-xl text-indigo-100">
				Join thousands of students who are already exploring our library
			</p>
			<Button
				onclick={() => goto('/library/books')}
				class="transform bg-white px-8 py-4 text-lg font-semibold text-indigo-600 shadow-xl transition-all duration-300 hover:scale-105 hover:bg-indigo-50"
			>
				Start Reading Today
			</Button>
		</div>
	</div>

	<!-- Footer -->
	<footer class="bg-gray-900 py-12 text-white">
		<div class="mx-auto max-w-7xl px-6">
			<div class="grid gap-8 md:grid-cols-3">
				<div>
					<h3 class="mb-4 text-lg font-semibold">UniVerse Library</h3>
					<p class="text-gray-400">
						Empowering students with knowledge through our comprehensive library system.
					</p>
				</div>
				<div>
					<h3 class="mb-4 text-lg font-semibold">Quick Links</h3>
					<ul class="space-y-2 text-gray-400">
						<li>
							<a href="/library/books" class="transition-colors hover:text-white">Explore Books</a>
						</li>
						<li>
							<a href="/library/my-account" class="transition-colors hover:text-white">My History</a
							>
						</li>
						<li><a href="/library" class="transition-colors hover:text-white">Library Home</a></li>
					</ul>
				</div>
				<div>
					<h3 class="mb-4 text-lg font-semibold">Contact</h3>
					<p class="text-gray-400">Need help? Contact our library staff for assistance.</p>
				</div>
			</div>
			<Separator class="my-8 bg-gray-700" />
			<div class="text-center text-gray-400">
				<p>&copy; 2024 UniVerse Library. All rights reserved.</p>
			</div>
		</div>
	</footer>
</div>
