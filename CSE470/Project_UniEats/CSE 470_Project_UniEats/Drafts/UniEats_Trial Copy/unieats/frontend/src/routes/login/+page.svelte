<!-- src/routes/login/+page.svelte -->
<script>
  import { supabase } from '$lib/supabase';
  let email = '';
  let password = '';

  async function signIn() {
    const { error } = await supabase.auth.signInWithPassword({ email, password });
    if (error) return alert(error.message);
    alert('✅ Logged in!');
  }
</script>

<div class="p-8 max-w-md mx-auto">
  <h1 class="text-2xl mb-4">UniEats Login</h1>
  <input
    type="email"
    bind:value={email}
    placeholder="you@uni.edu"
    class="border p-2 w-full mb-2"
  />
  <input
    type="password"
    bind:value={password}
    placeholder="Your password"
    class="border p-2 w-full mb-4"
  />
  <button on:click={signIn} class="bg-blue-500 text-white px-4 py-2 rounded">
    Log In
  </button>
</div>
