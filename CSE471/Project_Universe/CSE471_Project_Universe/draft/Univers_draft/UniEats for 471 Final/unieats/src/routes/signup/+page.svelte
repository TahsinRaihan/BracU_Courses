<script lang="ts">
  import * as authController from '$lib/controllers/authController';
  let email = '';
  let password = '';
  let nickname = '';

  async function signUp() {
    const { error } = await authController.signupUser(email, password, nickname);
    if (error) return alert(error.message);
    alert('✅ Signed up! Welcome, ' + nickname + '. Please check your email to confirm.');
  }
</script>

<div class="p-8 max-w-md mx-auto bg-white/90 rounded shadow-md">
  <h1 class="text-2xl mb-4">Sign Up for UniEats</h1>
  <input
    type="text"
    bind:value={nickname}
    placeholder="Nickname"
    class="border p-2 w-full mb-2 rounded"
  />
  <input
    type="email"
    bind:value={email}
    placeholder="Email"
    class="border p-2 w-full mb-2 rounded"
  />
  <input
    type="password"
    bind:value={password}
    placeholder="Password"
    class="border p-2 w-full mb-4 rounded"
  />
  <button on:click={signUp} class="w-full bg-green-600 text-white p-2 rounded">
    Sign Up
  </button>
  <p class="mt-4 text-sm">
    Already a member? <a href="/login" class="text-blue-600">Log in</a>
  </p>
</div>
