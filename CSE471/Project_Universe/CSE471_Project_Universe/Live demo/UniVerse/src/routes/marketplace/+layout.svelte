<script lang="ts">
  import { page } from '$app/stores';
  import * as Card from "$lib/components/ui/card";
  import { Button } from "$lib/components/ui/button";

  $: isBuyerPage = $page.url.pathname.startsWith('/marketplace/buyer');
  $: isSellerPage = $page.url.pathname.startsWith('/marketplace/seller');
</script>

<div class="container mx-auto p-4 relative">
  <a href="/myspace" title="return to myspace" class="absolute top-8 right-8 z-10 p-1 rounded-md shadow-md" style="background: linear-gradient(to right, rgb(217, 70, 239), rgb(79, 70, 229));">
    <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-white" viewBox="0 0 20 20" fill="currentColor">
      <path fill-rule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd" />
    </svg>
  </a>
  <Card.Root class="mb-4 bg-pink-50 border-pink-200">
    <Card.Header>
			<Card.Title class="text-2xl font-bold text-pink-700">Marketplace</Card.Title>
			<Card.Description class="text-pink-600">Your one-stop shop for university essentials.</Card.Description>
    </Card.Header>
    <Card.Content class="flex justify-between items-center">
      <div class="flex space-x-2">
        <a href="/marketplace/buyer">
          <Button class="bg-pink-500 hover:bg-pink-600 text-white" variant={isBuyerPage ? 'default' : 'outline'}>Buyer</Button>
        </a>
        <a href="/marketplace/seller">
          <Button class="bg-pink-500 hover:bg-pink-600 text-white" variant={isSellerPage ? 'default' : 'outline'}>Seller</Button>
        </a>
      </div>
			<a href="/marketplace/buyer/history">
				<Button class="bg-gradient-to-r from-purple-500 to-pink-500 text-white hover:from-purple-600 hover:to-pink-600">History</Button>
			</a>
    </Card.Content>
  </Card.Root>

  <main>
    <slot />
  </main>
</div>
