
<script lang="ts">
  import { goto } from '$app/navigation';
  import * as authController from '$lib/controllers/authController';
  let email = '';
  let password = '';

  async function signIn() {
    const { error } = await authController.loginUser(email, password);
    if (error) return alert(error.message);
    alert('✅ Logged in!');
    goto('/');
  }
</script>

<div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-orange-300 to-yellow-300 py-12 px-4 sm:px-6 lg:px-8">
  <div class="max-w-md w-full space-y-8 bg-white p-10 rounded-xl shadow-2xl transform transition-all duration-300 hover:scale-105">
    <div>
      <h1 class="mt-6 text-center text-5xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-orange-500 to-yellow-600 drop-shadow-lg">
        Welcome to UniEats
      </h1>
      <p class="mt-2 text-center text-sm text-gray-600">
        Sign in to your account
      </p>
    </div>
    <form class="mt-8 space-y-6" on:submit|preventDefault={signIn}>
      <div class="rounded-md shadow-sm -space-y-px">
        <div>
          <label for="email-address" class="sr-only">Email address</label>
          <input
            id="email-address"
            name="email"
            type="email"
            autocomplete="email"
            required
            bind:value={email}
            class="appearance-none rounded-none relative block w-full px-3 py-3 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-orange-500 focus:z-10 sm:text-sm transition duration-200 ease-in-out transform focus:scale-105"
            placeholder="Email address"
          />
        </div>
        <div>
          <label for="password" class="sr-only">Password</label>
          <input
            id="password"
            name="password"
            type="password"
            autocomplete="current-password"
            required
            bind:value={password}
            class="appearance-none rounded-none relative block w-full px-3 py-3 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-orange-500 focus:z-10 sm:text-sm transition duration-200 ease-in-out transform focus:scale-105"
            placeholder="Password"
          />
        </div>
      </div>

      <div>
        <button
          type="submit"
          class="group relative w-full flex justify-center py-3 px-4 border border-transparent text-lg font-medium rounded-md text-white bg-gradient-to-r from-orange-500 to-yellow-600 hover:from-orange-600 hover:to-yellow-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-orange-500 shadow-lg transform transition-all duration-300 hover:scale-105"
        >
          <span class="absolute left-0 inset-y-0 flex items-center pl-3">
            <svg class="h-6 w-6 text-white group-hover:text-gray-100" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
              <path fill-rule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clip-rule="evenodd" />
            </svg>
          </span>
          Sign in
        </button>
      </div>

      <div class="text-sm text-center">
        Don't have an account? <a href="/signup" class="font-medium text-orange-600 hover:text-orange-500">Sign up</a>
      </div>
    </form>
  </div>
</div>
