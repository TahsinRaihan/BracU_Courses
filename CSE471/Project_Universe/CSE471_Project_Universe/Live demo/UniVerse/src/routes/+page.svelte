<script lang="ts">
	import { Button } from '$lib/components/ui/button';
</script>

<svelte:head>
	<title>UniVerse - Your Complete Student Platform</title>
	<meta
		name="description"
		content="Welcome to UniVerse, your all-in-one student platform featuring library, café, marketplace, and more"
	/>
</svelte:head>

<!-- Hero Section -->
<div
	class="relative flex min-h-screen flex-col overflow-hidden bg-gradient-to-br from-black via-gray-900 to-black text-white"
>
	<!-- Animated Gradient Background -->
	<div
		class="absolute inset-0 animate-pulse bg-gradient-to-br from-black via-purple-900/20 to-blue-900/20"
	></div>
	<div
		class="absolute inset-0 animate-pulse bg-gradient-to-tl from-black via-gray-800/30 to-black delay-1000"
	></div>
	<div
		class="absolute inset-0 animate-pulse bg-gradient-to-r from-transparent via-gray-900/10 to-transparent delay-2000"
	></div>
	<!-- Navigation -->
	<nav class="relative z-10 flex items-center justify-between p-8">
		<a href="/" class="leading-tight font-extrabold text-white transition-opacity hover:opacity-80">
			UNI<br />VERSE
		</a>

		<div class="hidden items-center space-x-8 md:flex">
			<a href="#features" class="text-gray-400 transition-colors hover:text-white">Features</a>
			<a href="#about" class="text-gray-400 transition-colors hover:text-white">About</a>
			<Button href="/auth/login" variant="ghost" class="text-white hover:bg-white/10">
				Sign In
			</Button>
		</div>
	</nav>

	<!-- Main Content -->
	<div class="relative z-10 flex flex-1 items-center justify-center px-8">
		<div class="mx-auto max-w-4xl text-center">
			<!-- Main Heading -->
			<h1 class="mb-8 text-6xl leading-tight font-bold md:text-8xl">
				Your Complete Student
				<span
					class="bg-gradient-to-r from-purple-500 via-pink-500 to-blue-500 bg-clip-text text-transparent"
				>
					UNIVERSE
				</span>
			</h1>

			<!-- Description -->
			<p class="mx-auto mb-12 max-w-3xl text-xl leading-relaxed text-gray-400 md:text-2xl">
				All-in-one student platform featuring library, café, marketplace, and more. Everything you
				need for your academic journey in one place.
			</p>

			<!-- CTA Button -->
			<div class="flex justify-center">
				<Button
					href="/auth/login"
					size="lg"
					class="rounded-lg bg-white px-8 py-4 text-lg font-semibold text-black transition-all duration-300 hover:bg-gray-200"
				>
					Get Started
				</Button>
			</div>
		</div>
	</div>

	<!-- Scroll Indicator -->
	<div class="relative z-10 flex justify-center pb-8">
		<div class="flex h-10 w-6 justify-center rounded-full border-2 border-gray-600">
			<div class="mt-2 h-3 w-1 rounded-full bg-gray-400"></div>
		</div>
	</div>
</div>

<!-- Features Section -->
<section id="features" class="bg-gray-900 py-24">
	<div class="mx-auto max-w-6xl px-8">
		<div class="mb-20 text-center">
			<h2 class="mb-6 text-4xl font-bold text-white md:text-5xl">Everything You Need</h2>
			<p class="mx-auto max-w-2xl text-xl text-gray-400">
				A comprehensive platform designed for modern student life
			</p>
		</div>

		<div class="grid gap-8 md:grid-cols-2 lg:grid-cols-4">
			<!-- Feature 1 -->
			<div class="group rounded-xl bg-gray-800 p-8 transition-all duration-300 hover:bg-gray-700">
				<div class="mb-6 flex h-12 w-12 items-center justify-center rounded-lg bg-purple-500">
					<svg class="h-6 w-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"
						></path>
					</svg>
				</div>
				<h3 class="mb-4 text-xl font-semibold text-white">Digital Library</h3>
				<p class="leading-relaxed text-gray-400">
					Access thousands of books, articles, and educational resources across all subjects.
				</p>
			</div>

			<!-- Feature 2 -->
			<a
				href="/cafeteria"
				class="group block rounded-xl bg-gray-800 p-8 transition-all duration-300 hover:bg-gray-700"
			>
				<div class="mb-6 flex h-12 w-12 items-center justify-center rounded-lg bg-green-500">
					<svg class="h-6 w-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1"
						></path>
					</svg>
				</div>
				<h3 class="mb-4 text-xl font-semibold text-white">Campus Café</h3>
				<p class="leading-relaxed text-gray-400">
					Order food, beverages, and snacks from campus cafés with easy payment.
				</p>
			</a>

			<!-- Feature 3 -->
			<div class="group rounded-xl bg-gray-800 p-8 transition-all duration-300 hover:bg-gray-700">
				<div class="mb-6 flex h-12 w-12 items-center justify-center rounded-lg bg-blue-500">
					<svg class="h-6 w-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"
						></path>
					</svg>
				</div>
				<h3 class="mb-4 text-xl font-semibold text-white">Marketplace</h3>
				<p class="leading-relaxed text-gray-400">
					Buy, sell, and trade textbooks and student essentials with fellow students.
				</p>
			</div>

			<!-- Feature 4 -->
			<div class="group rounded-xl bg-gray-800 p-8 transition-all duration-300 hover:bg-gray-700">
				<div class="mb-6 flex h-12 w-12 items-center justify-center rounded-lg bg-pink-500">
					<svg class="h-6 w-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
						></path>
					</svg>
				</div>
				<h3 class="mb-4 text-xl font-semibold text-white">Smart Features</h3>
				<p class="leading-relaxed text-gray-400">
					Advanced search, notifications, and seamless integration across all services.
				</p>
			</div>
		</div>
	</div>
</section>

<!-- About Section -->
<section id="about" class="bg-black py-24">
	<div class="mx-auto max-w-4xl px-8 text-center">
		<h2 class="mb-8 text-4xl font-bold text-white md:text-5xl">Built for Students</h2>
		<p class="mx-auto max-w-3xl text-xl leading-relaxed text-gray-400">
			Universe is more than just a platform. It's a comprehensive student ecosystem designed to
			empower students with everything they need for their academic journey.
		</p>
	</div>
</section>

<!-- Footer -->
<footer class="bg-gray-900 py-16 text-white">
	<div class="mx-auto max-w-6xl px-8">
		<div class="grid gap-8 md:grid-cols-4">
			<div>
				<div class="mb-4 flex items-center space-x-2">
					<span class="text-xl font-extrabold">UNI<br />VERSE</span>
				</div>
				<p class="text-gray-400">Your comprehensive all-in-one student platform.</p>
			</div>

			<div>
				<h4 class="mb-4 font-semibold">Product</h4>
				<ul class="space-y-2 text-gray-400">
					<li><button class="text-left transition-colors hover:text-white">Features</button></li>
					<li><button class="text-left transition-colors hover:text-white">Library</button></li>
					<li>
						<a href="/cafeteria" class="text-left transition-colors hover:text-white">Café</a>
					</li>
				</ul>
			</div>

			<div>
				<h4 class="mb-4 font-semibold">Company</h4>
				<ul class="space-y-2 text-gray-400">
					<li><button class="text-left transition-colors hover:text-white">About</button></li>
					<li><button class="text-left transition-colors hover:text-white">Contact</button></li>
					<li><button class="text-left transition-colors hover:text-white">Support</button></li>
				</ul>
			</div>

			<div>
				<h4 class="mb-4 font-semibold">Legal</h4>
				<ul class="space-y-2 text-gray-400">
					<li><button class="text-left transition-colors hover:text-white">Privacy</button></li>
					<li><button class="text-left transition-colors hover:text-white">Terms</button></li>
					<li><button class="text-left transition-colors hover:text-white">Cookies</button></li>
				</ul>
			</div>
		</div>

		<div class="mt-12 border-t border-gray-800 pt-8 text-center text-gray-400">
			<p>&copy; 2025 Universe. All rights reserved.</p>
		</div>
	</div>
</footer>
