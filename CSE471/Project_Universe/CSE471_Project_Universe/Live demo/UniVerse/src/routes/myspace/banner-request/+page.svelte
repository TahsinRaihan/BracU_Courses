<script lang="ts">
  import { enhance } from '$app/forms';
  
  let bannerForm = {
    title: '',
    description: '',
    duration_type: 'minutes',
    duration_value: 10,
    schedule_type: 'immediate' as 'immediate' | 'scheduled',
    scheduled_date: '',
    scheduled_time: ''
  };
  
  let isSubmitting = false;
  let successMessage = '';
  let errorMessage = '';
  
  function resetForm() {
    bannerForm = {
      title: '',
      description: '',
      duration_type: 'minutes',
      duration_value: 10,
      schedule_type: 'immediate',
      scheduled_date: '',
      scheduled_time: ''
    };
  }
</script>

<svelte:head>
  <title>Request Advertisement - MySpace</title>
</svelte:head>

<div class="min-h-[100dvh] bg-[hsl(222.2_47.4%_11.2%)] text-white">
  <!-- Universe Link -->
  <a href="/" class="absolute top-4 left-4 z-10 text-sm font-extrabold leading-tight text-white hover:opacity-90 focus:outline-none focus-visible:ring-2 focus-visible:ring-white/60">
    UNI<br/>VERSE
  </a>
  
  <div class="container mx-auto px-4 py-8 pt-16">
    <div class="max-w-2xl mx-auto">
      <!-- Header -->
      <div class="text-center mb-8">
        <h1 class="text-3xl font-bold text-white mb-2">Request Advertisement</h1>
        <p class="text-gray-300">Submit your advertisement request to be displayed in the marquee</p>
      </div>
      
      <!-- Success/Error Messages -->
      {#if successMessage}
        <div class="mb-6 p-4 bg-green-500/20 border border-green-500/50 rounded-lg text-green-200">
          <p>{successMessage}</p>
        </div>
      {:else if errorMessage}
        <div class="mb-6 p-4 bg-red-500/20 border border-red-500/50 rounded-lg text-red-200">
          <p>Error: {errorMessage}</p>
        </div>
      {/if}
      
      <!-- Request Form -->
      <div class="bg-white/5 backdrop-blur-sm rounded-lg p-6 border border-white/10">
        <form 
          method="POST" 
          action="?/createBannerRequest" 
          use:enhance={() => {
            console.log('Form submission started');
            isSubmitting = true;
            return async ({ result }) => {
              console.log('Form submission result:', result);
              isSubmitting = false;
              if (result.type === 'success') {
                console.log('Form submission successful');
                successMessage = 'Your advertisement request has been submitted successfully! An admin will review it soon.';
                errorMessage = ''; // Clear any previous error
                resetForm();
              } else if (result.type === 'failure') {
                console.log('Form submission failed:', result);
                errorMessage = (result.data?.message as string) || 'Error submitting advertisement request.';
                successMessage = ''; // Clear any previous success
              } else {
                console.log('Form submission failed:', result);
                errorMessage = 'Error submitting advertisement request.';
                successMessage = ''; // Clear any previous success
              }
            };
          }}
          class="space-y-6"
        >
          <!-- Title -->
          <div>
            <label for="title" class="block text-sm font-medium text-white mb-2">
              Advertisement Text *
            </label>
            <input
              id="title"
              name="title"
              type="text"
              bind:value={bannerForm.title}
              required
              maxlength="100"
              class="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="Enter the text that will appear in the marquee"
            />
            <p class="text-sm text-gray-400 mt-1">Maximum 100 characters</p>
          </div>
          
          <!-- Description -->
          <div>
            <label for="description" class="block text-sm font-medium text-white mb-2">
              Additional Details
            </label>
            <textarea
              id="description"
              name="description"
              bind:value={bannerForm.description}
              rows="3"
              maxlength="500"
              class="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
              placeholder="Provide additional context for the admin"
            ></textarea>
            <p class="text-sm text-gray-400 mt-1">Maximum 500 characters</p>
          </div>
          
          <!-- Duration -->
          <div>
            <!-- svelte-ignore a11y_label_has_associated_control -->
            <label class="block text-sm font-medium text-white mb-2">
              Display Duration *
            </label>
            <div class="flex gap-3">
              <div class="flex-1">
                <input
                  id="duration_value"
                  name="duration_value"
                  type="number"
                  bind:value={bannerForm.duration_value}
                  min="1"
                  max={bannerForm.duration_type === 'minutes' ? 1440 : bannerForm.duration_type === 'hours' ? 720 : 365}
                  required
                  class="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Enter duration"
                />
              </div>
              <div class="flex-1">
                <select
                  id="duration_type"
                  name="duration_type"
                  bind:value={bannerForm.duration_type}
                  required
                  class="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent [&>option]:bg-gray-800 [&>option]:text-white"
                >
                  <option value="minutes" class="bg-gray-800 text-white">Minutes</option>
                  <option value="hours" class="bg-gray-800 text-white">Hours</option>
                  <option value="days" class="bg-gray-800 text-white">Days</option>
                </select>
              </div>
            </div>
            <p class="text-sm text-gray-400 mt-1">
              {bannerForm.duration_type === 'minutes' 
                ? 'Maximum 1440 minutes (24 hours)' 
                : bannerForm.duration_type === 'hours'
                ? 'Maximum 720 hours (30 days)' 
                : 'Maximum 365 days'
              }
            </p>
          </div>
          
          <!-- Scheduling -->
          <div>
            <!-- svelte-ignore a11y_label_has_associated_control -->
            <label class="block text-sm font-medium text-white mb-2">
              Display Schedule
            </label>
            <div class="space-y-3">
              <div class="flex items-center space-x-3">
                <input
                  id="schedule_type_immediate"
                  name="schedule_type"
                  type="radio"
                  value="immediate"
                  bind:group={bannerForm.schedule_type}
                  class="w-4 h-4 text-blue-600 bg-white/10 border-white/20 focus:ring-blue-500"
                />
                <label for="schedule_type_immediate" class="text-sm text-white">
                  Start immediately when approved
                </label>
              </div>
              <div class="flex items-center space-x-3">
                <input
                  id="schedule_type_scheduled"
                  name="schedule_type"
                  type="radio"
                  value="scheduled"
                  bind:group={bannerForm.schedule_type}
                  class="w-4 h-4 text-blue-600 bg-white/10 border-white/20 focus:ring-blue-500"
                />
                <label for="schedule_type_scheduled" class="text-sm text-white">
                  Schedule for specific date and time
                </label>
              </div>
            </div>
          </div>
          
          <!-- Scheduled Date/Time (conditional) -->
          {#if bannerForm.schedule_type === 'scheduled'}
            <div class="space-y-3">
              <div>
                <label for="scheduled_date" class="block text-sm font-medium text-white mb-2">
                  Start Date *
                </label>
                <input
                  id="scheduled_date"
                  name="scheduled_date"
                  type="date"
                  bind:value={bannerForm.scheduled_date}
                  required
                  min={new Date().toISOString().split('T')[0]}
                  class="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
              <div>
                <label for="scheduled_time" class="block text-sm font-medium text-white mb-2">
                  Start Time *
                </label>
                <input
                  id="scheduled_time"
                  name="scheduled_time"
                  type="time"
                  bind:value={bannerForm.scheduled_time}
                  required
                  class="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
            </div>
          {/if}
          
          <!-- Submit Button -->
          <div class="pt-4">
            <button
              type="submit"
              disabled={isSubmitting}
              class="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-blue-600/50 text-white font-medium py-3 px-4 rounded-lg transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 focus:ring-offset-gray-900"
            >
              {isSubmitting ? 'Submitting...' : 'Submit Request'}
            </button>
          </div>
        </form>
      </div>
      
      <!-- Info Section -->
      <div class="mt-8 bg-blue-500/10 border border-blue-500/30 rounded-lg p-4">
        <h3 class="text-lg font-semibold text-blue-300 mb-2">How it works:</h3>
        <ul class="text-sm text-gray-300 space-y-1">
          <li>• Submit your advertisement request</li>
          <li>• An admin will review and approve/reject it</li>
          <li>• If approved, your ad will appear in the marquee</li>
          <li>• The ad will automatically expire after the selected duration</li>
        </ul>
      </div>
    </div>
  </div>
</div>
