<script lang="ts">
  import { enhance } from '$app/forms';
  import { page } from '$app/stores';
  import type { PageData } from './$types';
  
  export let data: PageData;
  
  let pendingRequests = data.pendingRequests || [];
  let allRequests = data.allRequests || [];
  let activeTab = 'pending';
  
  function handleApprove(requestId: string) {
    if (confirm('Are you sure you want to approve this banner request?')) {
      const form = new FormData();
      form.append('requestId', requestId);
      
      fetch('?/approveBannerRequest', {
        method: 'POST',
        body: form
      }).then(() => {
        // Refresh the page to update the requests list
        window.location.reload();
      });
    }
  }
  
  function handleReject(requestId: string) {
    const reason = prompt('Please provide a reason for rejection:');
    if (reason !== null) {
      const form = new FormData();
      form.append('requestId', requestId);
      form.append('adminNotes', reason);
      
      fetch('?/rejectBannerRequest', {
        method: 'POST',
        body: form
      }).then(() => {
        // Refresh the page to update the requests list
        window.location.reload();
      });
    }
  }
  
  function handleDelete(requestId: string) {
    if (confirm('Are you sure you want to delete this banner request? This action cannot be undone.')) {
      const form = new FormData();
      form.append('requestId', requestId);
      
      fetch('?/deleteBannerRequest', {
        method: 'POST',
        body: form
      }).then(() => {
        // Refresh the page to update the requests list
        window.location.reload();
      });
    }
  }
  
  function formatDuration(request: any) {
    if (request.duration_minutes) {
      return `${request.duration_minutes} minutes`;
    } else if (request.duration_hours) {
      return `${request.duration_hours} hours`;
    } else {
      return `${request.duration_days} days`;
    }
  }
  
  function formatDate(dateString: string) {
    return new Date(dateString).toLocaleString();
  }
  
  function getStatusColor(status: string) {
    switch (status) {
      case 'pending': return 'bg-yellow-100 text-yellow-800';
      case 'approved': return 'bg-green-100 text-green-800';
      case 'rejected': return 'bg-red-100 text-red-800';
      case 'expired': return 'bg-gray-100 text-gray-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  }

  function formatUserInfo(request: any) {
    return `User ${request.user_id}`;
  }
</script>

<svelte:head>
  <title>Banner Requests - Admin</title>
</svelte:head>

<div class="min-h-screen bg-gray-50">
  <!-- Universe Link -->
  <a href="/" class="absolute top-4 left-4 z-10 text-sm font-extrabold leading-tight text-gray-900 hover:opacity-90 focus:outline-none focus-visible:ring-2 focus-visible:ring-gray-900/60">
    UNI<br/>VERSE
  </a>
  
  <div class="pt-16 px-6 py-8">
    <div class="max-w-7xl mx-auto space-y-6">
      <!-- Header -->
      <div class="bg-white shadow rounded-lg p-6 border border-gray-200">
        <h2 class="text-2xl font-bold text-gray-900 mb-2">Banner Requests Management</h2>
        <p class="text-gray-600">Review and manage advertisement requests from students</p>
      </div>
      
      <!-- Success/Error Messages -->
      {#if data.success}
        <div class="bg-green-50 border border-green-200 rounded-md p-4">
          <p class="text-green-800">{data.success}</p>
        </div>
      {:else if data.error}
        <div class="bg-red-50 border border-red-200 rounded-md p-4">
          <p class="text-red-800">Error: {data.error}</p>
        </div>
      {/if}
      
      <!-- Tabs -->
      <div class="bg-white shadow rounded-lg border border-gray-200">
        <div class="border-b border-gray-200">
          <nav class="-mb-px flex space-x-8 px-6">
            <button
              class="py-4 px-1 border-b-2 font-medium text-sm {activeTab === 'pending' ? 'border-blue-500 text-blue-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'}"
              on:click={() => activeTab = 'pending'}
            >
              Pending Requests ({pendingRequests.length})
            </button>
            <button
              class="py-4 px-1 border-b-2 font-medium text-sm {activeTab === 'all' ? 'border-blue-500 text-blue-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'}"
              on:click={() => activeTab = 'all'}
            >
              All Requests ({allRequests.length})
            </button>
          </nav>
        </div>
        
        <div class="p-6">
          {#if activeTab === 'pending'}
            <!-- Pending Requests -->
            {#if pendingRequests.length === 0}
              <div class="text-center py-8">
                <p class="text-gray-500">No pending banner requests.</p>
              </div>
            {:else}
              <div class="space-y-4">
                {#each pendingRequests as request (request.id)}
                  <div class="border border-gray-200 rounded-lg p-4 bg-gray-50">
                    <div class="flex items-start justify-between">
                      <div class="flex-1">
                        <div class="flex items-center space-x-2 mb-2">
                          <h3 class="font-semibold text-gray-900">{request.title}</h3>
                          <span class="px-2 py-1 text-xs rounded-full bg-yellow-100 text-yellow-800">
                            Pending
                          </span>
                        </div>
                        {#if request.description}
                          <p class="text-gray-600 text-sm mb-2">{request.description}</p>
                        {/if}
                        <div class="text-sm text-gray-500 space-y-1">
                          <p><strong>Duration:</strong> {formatDuration(request)}</p>
                          <p><strong>Schedule:</strong> {request.schedule_type === 'immediate' ? 'Start immediately when approved' : 'Scheduled for specific time'}</p>
                          {#if request.schedule_type === 'scheduled' && request.scheduled_start_date}
                            <p><strong>Scheduled Start:</strong> {formatDate(request.scheduled_start_date)}</p>
                          {/if}
                          <p><strong>Requested by:</strong> {formatUserInfo(request)}</p>
                          <p><strong>Submitted:</strong> {formatDate(request.created_at)}</p>
                        </div>
                      </div>
                      <div class="flex space-x-2 ml-4">
                        <button
                          on:click={() => handleApprove(request.id)}
                          class="px-3 py-1 text-xs rounded border border-green-300 text-green-700 hover:bg-green-50"
                        >
                          Approve
                        </button>
                        <button
                          on:click={() => handleReject(request.id)}
                          class="px-3 py-1 text-xs rounded border border-red-300 text-red-700 hover:bg-red-50"
                        >
                          Reject
                        </button>
                      </div>
                    </div>
                  </div>
                {/each}
              </div>
            {/if}
          {:else}
            <!-- All Requests -->
            {#if allRequests.length === 0}
              <div class="text-center py-8">
                <p class="text-gray-500">No banner requests found.</p>
              </div>
            {:else}
              <div class="space-y-4">
                {#each allRequests as request (request.id)}
                  <div class="border border-gray-200 rounded-lg p-4 bg-white">
                    <div class="flex items-start justify-between">
                      <div class="flex-1">
                        <div class="flex items-center space-x-2 mb-2">
                          <h3 class="font-semibold text-gray-900">{request.title}</h3>
                          <span class="px-2 py-1 text-xs rounded-full {getStatusColor(request.status)}">
                            {request.status.charAt(0).toUpperCase() + request.status.slice(1)}
                          </span>
                        </div>
                        {#if request.description}
                          <p class="text-gray-600 text-sm mb-2">{request.description}</p>
                        {/if}
                        <div class="text-sm text-gray-500 space-y-1">
                          <p><strong>Duration:</strong> {formatDuration(request)}</p>
                          <p><strong>Schedule:</strong> {request.schedule_type === 'immediate' ? 'Start immediately when approved' : 'Scheduled for specific time'}</p>
                          {#if request.schedule_type === 'scheduled' && request.scheduled_start_date}
                            <p><strong>Scheduled Start:</strong> {formatDate(request.scheduled_start_date)}</p>
                          {/if}
                          <p><strong>Requested by:</strong> {formatUserInfo(request)}</p>
                          <p><strong>Submitted:</strong> {formatDate(request.created_at)}</p>
                          {#if request.reviewed_at}
                            <p><strong>Reviewed:</strong> {formatDate(request.reviewed_at)}</p>
                          {/if}
                          {#if request.admin_notes}
                            <p><strong>Admin Notes:</strong> {request.admin_notes}</p>
                          {/if}
                          {#if request.start_date && request.end_date}
                            <p><strong>Active Period:</strong> {formatDate(request.start_date)} - {formatDate(request.end_date)}</p>
                          {/if}
                        </div>
                      </div>
                      <div class="flex space-x-2 ml-4">
                        {#if request.status === 'pending'}
                          <button
                            on:click={() => handleApprove(request.id)}
                            class="px-3 py-1 text-xs rounded border border-green-300 text-green-700 hover:bg-green-50"
                          >
                            Approve
                          </button>
                          <button
                            on:click={() => handleReject(request.id)}
                            class="px-3 py-1 text-xs rounded border border-red-300 text-red-700 hover:bg-red-50"
                          >
                            Reject
                          </button>
                        {/if}
                        <button
                          on:click={() => handleDelete(request.id)}
                          class="px-3 py-1 text-xs rounded border border-gray-300 text-gray-700 hover:bg-gray-50"
                        >
                          Delete
                        </button>
                      </div>
                    </div>
                  </div>
                {/each}
              </div>
            {/if}
          {/if}
        </div>
      </div>
    </div>
  </div>
</div>
